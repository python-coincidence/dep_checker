# stdlib
from typing import List

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("coincidence", )


@pytest.fixture()
def imports() -> List[str]:
	return [
			"import collections",
			"import shutil",
			"import pathlib",
			"import os",
			"import pytest",
			"import chemistry_tools",
			"import pathlib2",
			"from typing_extensions import TypedDict",
			"import domdf_python_tools",
			"import consolekit",
			"import click",
			"import pandas",
			"import ruamel.yaml",
			"import sphinx  # nodep",
			"import Bio",
			"from . import foo",
			"if False:",
			"\timport requests",
			'',
			"try:",
			"\timport virtualenv",
			"except ImportError:",
			"\timport venv",
			'',
			"with contextlib.suppress(ImportError):",
			"\timport whey",
			"with suppress(ModuleNotFoundError):",
			"\timport dom_toml",
			"with open('foo.txt'): pass",
			"try:",
			"\timport configconfig",
			"except TypeError:",
			"\tpass",
			"if sys.version_info > (3, 6):",
			"\timport setuptools",
			"import tomllib",
			"from __future__ import annotations",
			'',
			]


@pytest.fixture()
def requirements() -> List[str]:
	return [
			"consolekit",
			"pandas",
			"coincidence",
			"numpy",
			"biopython",
			]


@pytest.fixture()
def single_file_project(tmp_pathplus: PathPlus, imports: List[str], requirements: List[str]) -> PathPlus:
	(tmp_pathplus / "my_project.py").write_lines(imports)
	(tmp_pathplus / "requirements.txt").write_lines(requirements)

	return tmp_pathplus


@pytest.fixture()
def package_project(tmp_pathplus: PathPlus, imports: List[str], requirements: List[str]) -> PathPlus:
	(tmp_pathplus / "my_project").mkdir()
	(tmp_pathplus / "my_project" / "__init__.py").write_lines(imports)
	(tmp_pathplus / "requirements.txt").write_lines(requirements)

	return tmp_pathplus
