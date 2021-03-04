#!/usr/bin/env python3
#
#  config.py
"""
Functions to read configuration.
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
import re
from collections import defaultdict
from configparser import ConfigParser
from typing import Any, Callable, Dict, List, Optional

# 3rd party
import toml
from configconfig.configvar import ConfigVar
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

__all__ = ["AllowedUnused", "NameMapping", "ConfigReader", "NamespacePackages"]


def list_from_string(string: str) -> List[str]:
	"""
	Parse a string containing multiple values (separated by newlines or commas) into a list of values.

	:param string:
	"""

	return list(filter(bool, map(str.strip, re.split("[\n,]", string))))


class AllowedUnused(ConfigVar):
	"""
	List of requirements which are allowed to be unused in the source code.
	"""

	dtype = List[str]
	default: List[str] = []
	__name__ = "allowed_unused"

	@classmethod
	def validate(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:  # noqa: D102
		if raw_config_vars is None:
			raw_config_vars = {}

		if cls.rtype is None:
			cls.rtype = cls.dtype

		if cls.__name__ in raw_config_vars:
			value = raw_config_vars[cls.__name__]
			if isinstance(value, str):
				value = list_from_string(value)

			if isinstance(value, list):
				for element in value:
					if not isinstance(element, str):
						raise ValueError(f"'{cls.__name__}' must be a list of strings") from None

			return value

		return cls.default[:]


class NamespacePackages(ConfigVar):
	"""
	List of namespace packages, e.g. ``ruamel.yaml``.

	This currently only handles imports in the form ``import namespace.package`` or
	``from namespace.package import object``, but not ``from namespace import package``.

	.. versionadded:: 0.4.1

	**Example:**

	.. code-block:: ini

		[dep_checker]
		namespace_packages =
			ruamel.yaml
	"""

	dtype = List[str]
	rtype = dict
	default: Dict[str, List[str]] = {}
	__name__ = "namespace_packages"

	@classmethod
	def validate(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:  # noqa: D102
		if raw_config_vars is None:
			raw_config_vars = {}

		if cls.rtype is None:
			cls.rtype = cls.dtype

		if cls.__name__ in raw_config_vars:
			value = raw_config_vars[cls.__name__]
			if isinstance(value, str):
				value = list_from_string(value)

			if isinstance(value, list):
				for element in value:
					if not isinstance(element, str):
						raise ValueError(f"'{cls.__name__}' must be a list of strings") from None

			namespaces = defaultdict(list)

			for name in value:
				namespace, pkg = name.rsplit('.')
				namespaces[namespace].append(pkg)

			return value

		return cls.default.copy()


class NameMapping(ConfigVar):
	"""
	Mapping of requirement names (e.g. "biopython") to the names of packages they provide (e.g. "Bio").

	.. versionadded:: 0.4.1

	**Example:**

	.. code-block:: ini

		[dep_checker]
		name_mapping =
			biopython = Bio
	"""

	dtype = List[str]
	default: List[str] = []
	__name__ = "name_mapping"

	@classmethod
	def validate(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:  # noqa: D102
		if raw_config_vars is None:
			raw_config_vars = {}

		if cls.rtype is None:
			cls.rtype = cls.dtype

		if cls.__name__ in raw_config_vars:
			value = raw_config_vars[cls.__name__]
			if isinstance(value, str):
				tmp_dict = {}

				for line in value.splitlines():
					if line:
						key, val, *_ = re.split("[=:]", line)
						tmp_dict[key.strip()] = val.strip()

				value = tmp_dict

			if not isinstance(value, dict):
				raise ValueError(f"'{cls.__name__}' must be a dictionary") from None

			return {str(k): str(v) for k, v in value.items()}

		return cls.default[:]


class ConfigReader:
	"""
	Read and parse configuration files.

	:param section_name:
	:param default_factory:
	:param work_dir:
	"""

	def __init__(self, section_name: str, default_factory: Callable = dict, work_dir: PathLike = '.'):
		self.section_name = section_name
		self.work_dir = PathPlus(work_dir)
		self.default_factory = default_factory

	def visit_tox_ini(self) -> Optional[Dict]:
		"""
		Visit ``tox.ini`` and parse the configuration from it.

		Returns :py:obj:`None` if the file doesn't exist, or if it doesn't have a ``dep_checker`` section.
		"""

		if (self.work_dir / "tox.ini").is_file():
			tox_ini = ConfigParser()
			tox_ini.read(self.work_dir / "tox.ini")

			if self.section_name in tox_ini:
				return dict(tox_ini[self.section_name])

		return None

	def visit_setup_cfg(self) -> Optional[Dict]:
		"""
		Visit ``setup.cfg`` and parse the configuration from it.

		Returns :py:obj:`None` if the file doesn't exist, or if it doesn't have a ``dep_checker`` section.
		"""

		if (self.work_dir / "setup.cfg").is_file():
			tox_ini = ConfigParser()
			tox_ini.read(self.work_dir / "setup.cfg")

			if self.section_name in tox_ini:
				return dict(tox_ini[self.section_name])

		return None

	def visit_pyproject_toml(self) -> Optional[Dict]:
		"""
		Visit ``pyproject.toml`` and parse the configuration from it.

		Returns :py:obj:`None` if the file doesn't exist, or if it doesn't have a ``dep_checker`` section.
		"""

		if (self.work_dir / "pyproject.toml").is_file():
			config = toml.loads((self.work_dir / "pyproject.toml").read_text())

			if "tool" in config and self.section_name in config["tool"]:
				return config["tool"][self.section_name]

		return None

	def visit(self) -> Any:
		"""
		Visit all config files and parse the configuration from the first one containing the ``dep_checker`` section.
		"""

		for file in [
				self.visit_pyproject_toml,
				self.visit_tox_ini,
				self.visit_setup_cfg,
				]:
			ret = file()
			if ret is not None:
				return ret

		return self.default_factory()
