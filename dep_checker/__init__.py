#!/usr/bin/env python3
#
#  __init__.py
"""
Tool to check all requirements are actually required.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from collections import defaultdict
from configparser import ConfigParser
from typing import Any, Callable, Dict, List, Optional, Tuple

# 3rd party
import click
from configconfig.configvar import ConfigVar
from consolekit.terminal_colours import Fore, resolve_color_default
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from shippinglabel.requirements import read_requirements
from stdlib_list import stdlib_list

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["AllowedUnused", "ConfigReader", "Visitor", "check_imports"]

libraries = stdlib_list()
template = "{name} imported on line {lineno} of {filename}"


class AllowedUnused(ConfigVar):
	dtype = List[str]
	default = []
	__name__ = "allowed_unused"

	@classmethod
	def validate(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:

		if cls.__name__ in raw_config_vars:
			value = raw_config_vars[cls.__name__]
			if isinstance(value, str):
				value = list(filter(lambda x: bool(x), value.splitlines()))

			if isinstance(value, list):
				for element in value:
					if not isinstance(element, str):
						raise ValueError(f"'{cls.__name__}' must be a list of strings") from None

			return value

		return cls.default[:]


class ConfigReader:

	def __init__(self, section_name: str, default_factory: Callable = dict, work_dir: PathLike = "."):
		self.section_name = section_name
		self.work_dir = PathPlus(work_dir)
		self.default_factory = default_factory

	def visit_tox_ini(self) -> Optional[Dict]:
		if (self.work_dir / "tox.ini").is_file():
			tox_ini = ConfigParser()
			tox_ini.read(self.work_dir / "tox.ini")

			if self.section_name in tox_ini:
				return dict(tox_ini[self.section_name])

		return None

	def visit_setup_cfg(self) -> Optional[Dict]:
		if (self.work_dir / "setup.cfg").is_file():
			tox_ini = ConfigParser()
			tox_ini.read(self.work_dir / "setup.cfg")

			if self.section_name in tox_ini:
				return dict(tox_ini[self.section_name])

		return None

	# TODO: pyproject.toml, repo_helper.yml

	def visit(self) -> Any:
		for file in [
				self.visit_tox_ini,
				]:
			ret = file()
			if ret is not None:
				return ret

		return self.default_factory()


class Visitor(ast.NodeVisitor):

	def __init__(self, pkg_name: str):
		self.import_sources = []
		self.pkg_name = pkg_name

	def visit_Import(self, node: ast.Import) -> None:
		for name in node.names:
			name: ast.alias
			if name.name not in libraries and name.name != self.pkg_name:
				self.import_sources.append((name.name.split(".")[0], node.lineno))

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
		name = node.module.split(".")[0]
		if name not in libraries and name != self.pkg_name:
			self.import_sources.append((name, node.lineno))

	def visit(self, node: ast.AST) -> List[Tuple[str, int]]:
		super().visit(node)
		return self.import_sources

	def visit_Try(self, node: ast.Try) -> Any:
		for handler in node.handlers:
			if isinstance(handler.type, ast.Attribute):
				# print(handler.type.value.id)
				# print(handler.type.attr)
				pass
			elif isinstance(handler.type, ast.Name):
				# print(handler.type.id)
				if handler.type.id in {"ImportError", "ModuleNotFoundError"}:
					# TODO: check guarded imports
					# print("Guarded")
					pass
				else:
					self.generic_visit(node)
			elif handler.type is None:
				# print(None)
				pass
			else:
				# raise NotImplementedError(type(handler.type))
				pass


reader = ConfigReader("dep_checker", default_factory=dict)


def check_imports(
		pkg_name: str, req_file: PathLike = "requirements.txt", allowed_unused: Optional[List[str]] = None
		):

	colour = resolve_color_default()
	cwd = PathPlus.cwd()
	config = reader.visit()

	if allowed_unused is None:
		allowed_unused = AllowedUnused.get(config)

	req_file = PathPlus(req_file)

	if not req_file.is_absolute():
		req_file = cwd / req_file

	req_names = sorted(req.name.replace("-", "_") for req in read_requirements(req_file)[0])
	imports: Dict[str, Dict[PathPlus, int]] = defaultdict(dict)
	# mapping of import name to mapping of filename to lineno where imported

	for filename in (cwd / pkg_name).rglob("*.py"):
		if filename.relative_to(cwd).parts[0] in {".tox", "venv", ".venv"}:
			continue

		visitor = Visitor(pkg_name)
		for name, lineno in visitor.visit(ast.parse(filename.read_text())):
			imports[name][filename.relative_to(cwd)] = min(
					(imports[name].get(filename.relative_to(cwd), lineno), lineno)
					)

	for req in req_names:
		for filename, lineno in imports[req].items():
			msg = template.format(name=req, lineno=lineno, filename=filename)
			click.echo(Fore.GREEN(f"✔ {msg}"), color=colour)
			break
		else:
			if req not in allowed_unused:
				click.echo(Fore.YELLOW(f"✘ {req} never imported"), color=colour)

	for import_name, locations in imports.items():
		if import_name not in req_names:
			for filename, lineno in locations.items():
				msg = template.format(name=import_name, lineno=lineno, filename=filename)
				click.echo(Fore.RED(f"✘ {msg} but not listed as a requirement"), color=colour)
