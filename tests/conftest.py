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
def single_file_project(tmp_pathplus: PathPlus, imports, requirements: List[str]):
	(tmp_pathplus / "my_project.py").write_lines(imports)
	(tmp_pathplus / "requirements.txt").write_lines(requirements)

	return tmp_pathplus


@pytest.fixture()
def package_project(tmp_pathplus: PathPlus, imports, requirements: List[str]):
	(tmp_pathplus / "my_project").mkdir()
	(tmp_pathplus / "my_project" / "__init__.py").write_lines(imports)
	(tmp_pathplus / "requirements.txt").write_lines(requirements)

	return tmp_pathplus
