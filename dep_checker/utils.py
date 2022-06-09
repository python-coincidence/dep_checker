#!/usr/bin/env python3
#
#  utils.py
"""
Private utilities.
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
from astatine import get_attribute_name, is_type_checking

__all__ = ["Visitor", "is_suppress_importerror"]

if sys.version_info < (3, 10):  # pragma: no cover (py310+)
	# 3rd party
	from stdlib_list import stdlib_list  # type: ignore[import]

	libraries = stdlib_list()
else:  # pragma: no cover (<py310)
	libraries = sys.stdlib_module_names


class Visitor(ast.NodeVisitor):
	"""
	:class:`ast.NodeVisitor` to identify imports in a module.
	"""

	def __init__(self, pkg_name: str, namespace_packages: Optional[Dict[str, List[str]]] = None):
		self.import_sources: List[Tuple[str, int]] = []
		self.pkg_name = re.sub(r"[-/\\]", '_', pkg_name.rstrip(r"\/"))
		self.namespace_packages = namespace_packages or {}

	def record_import(self, name: str, lineno: int) -> None:
		"""
		Record an import.

		:param name: The name of the module being imported.
		:param lineno:

		.. TODO:: handle ``from namespace import package``
		"""

		for namespace, children in self.namespace_packages.items():
			name_elements = name.split('.')
			if name_elements[0] == namespace:
				if len(name_elements) > 1 and name_elements[1] in children:
					name = '.'.join(name_elements[:2])
					break
		else:
			# Not a namespace package
			name = name.split('.')[0]

		if name not in libraries and name != self.pkg_name:
			self.import_sources.append((name, lineno))

	def visit_Import(self, node: ast.Import) -> None:  # noqa: D102
		name: ast.alias
		for name in node.names:
			self.record_import(name.name, node.lineno)

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: D102
		if node.level != 0:
			# relative import
			return

		if node.module:
			self.record_import(node.module, node.lineno)

	def visit(self, node: ast.AST) -> List[Tuple[str, int]]:
		"""
		Traverse the AST.

		:param node:

		:returns: A list of imports and their locations (as two-element ``(name, lineno)`` tuples).
		"""

		super().visit(node)
		return self.import_sources

	def visit_Try(self, node: ast.Try) -> Any:  # noqa: D102
		for handler in node.handlers:
			if isinstance(handler.type, ast.Name):
				# print(handler.type.id)

				# TODO: check guarded imports

				if handler.type.id not in {"ImportError", "ModuleNotFoundError"}:
					self.generic_visit(node)

	def visit_With(self, node: ast.With) -> Any:  # noqa: D102
		if not is_suppress_importerror(node):
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

	def visit_If(self, node: ast.If) -> Any:  # noqa: D102
		# TODO: check guarded imports

		if not is_type_checking(node.test):
			self.generic_visit(node)


def is_suppress_importerror(node: ast.With) -> bool:
	"""
	Returns whether the given ``with`` block contains a
	:func:`contextlib.suppress(ImportError) <contextlib.suppress>` contextmanager.

	.. versionadded:: 0.5.0 (private)

	:param node:
	"""  # noqa: D400

	item: ast.withitem
	for item in node.items:
		if not isinstance(item.context_expr, ast.Call):
			continue

		try:
			name = '.'.join(get_attribute_name(item.context_expr.func))
		except NotImplementedError:  # pragma: no cover
			continue

		if name not in {"suppress", "contextlib.suppress", "contextlib2.suppress"}:
			continue

		for arg in item.context_expr.args:
			try:
				arg_name = '.'.join(get_attribute_name(arg))
			except NotImplementedError:  # pragma: no cover
				continue

			if arg_name in {"ImportError", "ModuleNotFoundError"}:
				return True

	return False
