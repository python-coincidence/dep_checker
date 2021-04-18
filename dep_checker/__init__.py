#!/usr/bin/env python3
#
#  __init__.py
"""
Tool to check all requirements are actually required.
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
from collections import defaultdict
from operator import attrgetter
from typing import Any, Dict, Iterable, Iterator, List, Mapping, NamedTuple, Optional, Set, Type, Union

# 3rd party
import click
from consolekit.terminal_colours import Fore, resolve_color_default
from domdf_python_tools.paths import PathPlus, in_directory
from domdf_python_tools.typing import PathLike
from packaging.requirements import Requirement
from shippinglabel.requirements import read_requirements

# this package
from dep_checker.config import AllowedUnused, ConfigReader, NameMapping, NamespacePackages
from dep_checker.utils import Visitor

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.9.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = (
		"template",
		"check_imports",
		"DepChecker",
		"PassingRequirement",
		"UnlistedRequirement",
		"UnusedRequirement",
		"make_requirement_tuple",
		)

#: The template to use when printing output.
template = "{name} imported at {filename}:{lineno}"

reader = ConfigReader("dep_checker", default_factory=dict)

NODEP = re.compile(r".*#\s*nodep.*")

_nt_types = Union[Type["PassingRequirement"], Type["UnlistedRequirement"], Type["UnusedRequirement"]]


def _nt_asdict_class_deco(nt: _nt_types) -> _nt_types:
	original_asdict = nt._asdict

	def _asdict(self) -> Dict[str, Any]:
		"""
		Return dictionary which maps field names to their corresponding values.

		.. seealso:: :func:`~.make_requirement_tuple`
		"""

		base_dict = dict(original_asdict(self))
		base_dict["class"] = self.__class__.__name__
		return base_dict

	_asdict.__module__ = nt.__module__
	_asdict.__qualname__ = f"{nt.__name__}._asdict"
	nt._asdict = _asdict  # type: ignore[assignment]

	return nt


def make_requirement_tuple(data: Dict[str, Any]) -> _nt_types:
	"""
	Construct either a :class:`~.PassingRequirement`,
	or :class:`~.UnlistedRequirement`, or :class:`~.UnusedRequirement`,
	depending on the value of the ``class`` key.

	Typically used to reconstruct an object from the dictionary produced by the
	``_asdict()`` method of those classes.

	.. versionadded:: 0.6.0

	:param data:
	"""  # noqa: D400

	class_name = data.pop("class")

	for class_obj in [
			PassingRequirement,
			UnlistedRequirement,
			UnusedRequirement,
			]:
		if class_name == class_obj.__name__:
			cls = class_obj
			break
	else:
		raise ValueError(f"Unknown requirement class {class_name!r}")  # pylint: disable=loop-invariant-statement

	return cls(**data)


@_nt_asdict_class_deco
class PassingRequirement(NamedTuple):
	"""
	Represents a requirement which is listed in the requirements file and imported.

	.. versionadded:: 0.6.0
	"""

	#: The name of the requirement.
	name: str
	#: The line number where the requirement is imported.
	lineno: int
	#: The file where the requirement is imported.
	filename: str

	def format_error(self) -> str:
		"""
		Format the error (or, in this case, success) message.
		"""

		return f"✔ {template.format_map(self._asdict())}"


@_nt_asdict_class_deco
class UnlistedRequirement(NamedTuple):
	"""
	Represents a requirement which is imported but not listed in the requirements file.

	.. versionadded:: 0.6.0
	"""

	#: The name of the requirement.
	name: str
	#: The line number where the requirement is imported.
	lineno: int
	#: The file where the requirement is imported.
	filename: str

	def format_error(self) -> str:
		"""
		Format the error message.
		"""

		return f"✘ {template.format_map(self._asdict())} but not listed as a requirement"


@_nt_asdict_class_deco
class UnusedRequirement(NamedTuple):
	"""
	Represents a requirement which is listed in the requirements file but never imported.

	.. versionadded:: 0.6.0
	"""

	#: The name of the requirement.
	name: str

	def format_error(self) -> str:
		"""
		Format the error message.
		"""

		return f"✘ {self.name} never imported"


class DepChecker:
	"""
	Check imports for the given package, against the given requirements.

	This class can be used to integrate ``dep_checker`` into other applications.

	.. versionadded:: 0.6.0

	:param pkg_name:
	:param requirements: The package's (supposed) requirements.
	:param allowed_unused: List of requirements which are allowed to be unused in the source code.
	:default allowed_unused: ``[]``
	:param name_mapping: Optional mapping of requirement names to import names, if they differ.
	:no-default name_mapping:
	:param namespace_packages: List of namespace packages, e.g. ``ruamel.yaml``.
	:no-default namespace_packages:
	"""

	def __init__(
			self,
			pkg_name: str,
			requirements: Iterable[str],
			*,
			allowed_unused: Optional[Iterable[str]] = None,
			name_mapping: Optional[Mapping[str, str]] = None,
			namespace_packages: Optional[Iterable[str]] = None,
			):

		self.pkg_name: str = str(pkg_name).rstrip(r"\/")
		self.requirements: Set[str] = set()
		self.allowed_unused: List[str] = list(allowed_unused or ())

		name_mapping = dict(name_mapping or {})

		for req in requirements:
			req = req.replace('-', '_')

			if req in name_mapping:
				# replace names in req_names with the name of the package the requirement provides
				req = name_mapping[req]

			self.requirements.add(req)

		self.namespace_packages: Dict[str, List[str]] = defaultdict(list)

		for name in namespace_packages or ():
			namespace, pkg = name.rsplit('.')
			self.namespace_packages[namespace].append(pkg)  # pylint: disable=loop-invariant-statement

	def check(
			self,
			work_dir: PathLike,
			) -> Iterable[Union[UnlistedRequirement, PassingRequirement, UnusedRequirement]]:
		"""
		Perform the check itself.

		:param work_dir: The directory to find the source of the package in.
			Useful with the ``src/`` layout.
		"""

		imports: Dict[str, Dict[PathPlus, int]] = defaultdict(dict)

		with in_directory(work_dir):
			for filename in iter_files_to_check(work_dir, self.pkg_name):

				visitor = Visitor(self.pkg_name.replace('/', '.'), self.namespace_packages)
				file_content = filename.read_text()

				for import_name, lineno in visitor.visit(ast.parse(file_content)):

					if import_name in self.requirements:
						min_lineno = min((imports[import_name].get(filename, lineno), lineno))
						imports[import_name][filename] = min_lineno
						continue

					# Not listed as requirement

					if NODEP.match(file_content.splitlines()[lineno - 1]):
						# Marked with "# nodep", so the user wants to ignore this
						continue

					yield UnlistedRequirement(name=import_name, lineno=lineno, filename=filename.as_posix())

		for req_name in sorted(self.requirements):
			for filename, lineno in imports[req_name].items():
				# Imported and listed as requirement
				yield PassingRequirement(name=req_name, lineno=lineno, filename=filename.as_posix())
				break
			else:
				if req_name not in self.allowed_unused:
					# not imported
					yield UnusedRequirement(name=req_name)


def iter_files_to_check(basepath: PathLike, pkg_name: str) -> Iterator[PathPlus]:
	"""
	Returns an iterator over all files in ``pkg_name``.

	If ``pkg_name`` resolves to a single-file module, that is the only element of the iterator.

	.. versionadded:: 0.6.0

	:param basepath:
	:param pkg_name:

	:raises FileNotFoundError: If neither :file:`{<pkg_name>}.py` or the directory ``pkg_name`` is found.
	"""

	basepath = PathPlus(basepath)

	if (basepath / f"{pkg_name}.py").is_file():
		yield PathPlus(f"{pkg_name}.py")
		return

	if not (basepath / pkg_name).exists():
		raise FileNotFoundError(f"Can't find a package called {pkg_name!r} in {basepath.as_posix()!r}")

	for filename in (basepath / pkg_name.replace('.', '/')).rglob("*.py"):
		filename = filename.relative_to(basepath)

		if filename.parts[0] in {".tox", "venv", ".venv"}:  # pragma: no cover
			continue

		yield filename


def check_imports(
		pkg_name: str,
		*requirements: Requirement,
		allowed_unused: Optional[List[str]] = None,
		colour: Optional[bool] = None,
		name_mapping: Optional[Dict[str, str]] = None,
		namespace_packages: Optional[List[str]] = None,
		work_dir: PathLike = '.',
		) -> int:
	r"""
	Check imports for the given package, against the given requirements file.

	:param pkg_name:
	:param \*requirements:
	:param allowed_unused: List of requirements which are allowed to be unused in the source code.
	:default allowed_unused: ``[]``
	:param colour: Whether to use coloured output.
	:no-default colour:
	:param name_mapping: Optional mapping of requirement names to import names, if they differ.
	:no-default name_mapping:
	:param namespace_packages: List of namespace packages, e.g. ``ruamel.yaml``.
	:no-default namespace_packages:
	:param work_dir: The directory to find the source of the package in. Useful with the src/ layout.

	:rtype:

	* Returns ``0`` if all requirements are used and listed as requirements.
	* Returns ``1`` is a requirement is unused, or if a package is imported but not listed as a requirement.

	.. versionchanged:: 0.4.1

		* Added the ``name_mapping`` option.
		* Added the ``work_dir`` option.

	.. versionchanged:: 0.7.0 Replaced the ``req_file`` argument with the ``*requirements`` argument.
		Use :func:`shippinglabel.requirements.read_requirements(req_file)[0] <shippinglabel.requirements.read_requirements>`
		 to get the original bevhaviour.
	"""

	ret = 0
	config = reader.visit()
	colour = resolve_color_default(colour)

	if allowed_unused is None:
		allowed_unused = AllowedUnused.get(config)

	if name_mapping is None:
		name_mapping = NameMapping.get(config)

	if namespace_packages is None:
		namespace_packages = NamespacePackages.get(config)

	work_dir = PathPlus(work_dir)
	work_dir = work_dir.abspath()

	checker = DepChecker(
			pkg_name,
			requirements=map(attrgetter("name"), requirements),
			allowed_unused=allowed_unused,
			name_mapping=name_mapping,
			namespace_packages=namespace_packages,
			)

	def echo(text: str) -> None:
		text = text.encode(sys.stdout.encoding, errors="ignore").decode(sys.stdout.encoding)
		click.echo(text, color=colour)

	for item in checker.check(work_dir):
		if isinstance(item, PassingRequirement):
			echo(Fore.GREEN(item.format_error()))
		elif isinstance(item, UnusedRequirement):
			echo(Fore.YELLOW(item.format_error()))
			ret |= 1
		elif isinstance(item, UnlistedRequirement):
			echo(Fore.RED(item.format_error()))
			ret |= 1

	return ret
