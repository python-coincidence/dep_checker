#!/usr/bin/env python3
#
#  utils.py
"""
Private utilities
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# 3rd party
from astatine import is_type_checking

__all__ = ["Visitor"]

if sys.version_info < (3, 10):  # pragma: no cover (py310+)
	# 3rd party
	from stdlib_list import stdlib_list  # type: ignore

	libraries = stdlib_list()
else:  # pragma: no cover (<py310)
	libraries = sys.stdlib_module_names


class Visitor(ast.NodeVisitor):

	def __init__(self, pkg_name: str, namespace_packages: Optional[Dict[str, List[str]]] = None):
		self.import_sources: List[Tuple[str, int]] = []
		self.pkg_name = re.sub("[-.]", '_', pkg_name)
		self.namespace_packages = namespace_packages or {}

	def record_import(self, name: str, lineno: int):
		# TODO: handle ``from namespace import package``

		for namespace in self.namespace_packages:
			if namespace in name:
				name = name.replace('.', '_')
				break
		else:
			# Not a namespace package
			name = name.split('.')[0]

		if name not in libraries and name != self.pkg_name:
			self.import_sources.append((name, lineno))

	def visit_Import(self, node: ast.Import) -> None:
		name: ast.alias
		for name in node.names:
			self.record_import(name.name, node.lineno)

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
		if node.level != 0:
			# relative import
			return

		if node.module:
			self.record_import(node.module, node.lineno)

	def visit(self, node: ast.AST) -> List[Tuple[str, int]]:
		super().visit(node)
		return self.import_sources

	def visit_Try(self, node: ast.Try) -> Any:
		for handler in node.handlers:
			if isinstance(handler.type, ast.Name):
				# print(handler.type.id)

				# TODO: check guarded imports

				if handler.type.id not in {"ImportError", "ModuleNotFoundError"}:
					self.generic_visit(node)

	# def visit_Try(self, node: ast.Try) -> Any:
	# 	for handler in node.handlers:
	# 		if isinstance(handler.type, ast.Attribute):
	# 			# print(handler.type.value.id)
	# 			# print(handler.type.attr)
	# 			pass
	# 		elif isinstance(handler.type, ast.Name):
	# 			# print(handler.type.id)
	# 			if handler.type.id in {"ImportError", "ModuleNotFoundError"}:
	# 				# TODO: check guarded imports
	# 				# print("Guarded")
	# 				pass
	# 			else:
	# 				self.generic_visit(node)
	# 		elif handler.type is None:
	# 			# print(None)
	# 			pass
	# 		else:
	# 			# raise NotImplementedError(type(handler.type))
	# 			pass

	def visit_If(self, node: ast.If) -> Any:
		# TODO: check guarded imports

		if not is_type_checking(node.test):
			self.generic_visit(node)
