# 3rd party
import pytest
from coincidence import AdvancedDataRegressionFixture
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from dep_checker import check_imports
from dep_checker.__main__ import main


@pytest.fixture()
def single_file_project(tmp_pathplus: PathPlus):
	(tmp_pathplus / "my_project.py").write_lines([
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
			"if False:",
			"\timport requests"
			])
	(tmp_pathplus / "requirements.txt").write_lines([
			"consolekit",
			"pandas",
			"coincidence",
			"numpy",
			"biopython",
			])

	return tmp_pathplus


@pytest.fixture()
def package_project(tmp_pathplus: PathPlus):
	(tmp_pathplus / "my_project").mkdir()
	(tmp_pathplus / "my_project" / "__init__.py").write_lines([
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
			"if False:",
			"\timport requests"
			])
	(tmp_pathplus / "requirements.txt").write_lines([
			"consolekit",
			"pandas",
			"coincidence",
			"numpy",
			"biopython",
			])

	return tmp_pathplus


def test_check_imports(
		single_file_project: PathPlus,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	assert check_imports("my_project", work_dir=single_file_project, colour=False) == 1
	advanced_data_regression.check(capsys.readouterr())


def test_check_imports_package(
		package_project: PathPlus,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	assert check_imports("my_project", work_dir=package_project, colour=False) == 1
	advanced_data_regression.check(capsys.readouterr())


def test_cli(
		single_file_project: PathPlus,
		file_regression: FileRegressionFixture,
		):

	with in_directory(single_file_project):
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour"])

	result.check_stdout(file_regression)
	assert result.exit_code == 1


def test_cli_package(package_project: PathPlus, file_regression: FileRegressionFixture):

	with in_directory(package_project):
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour"])

	result.check_stdout(file_regression)
	assert result.exit_code == 1


# TODO: test with the different config options


@pytest.mark.parametrize(
		"config",
		[
				pytest.param({"allowed_unused": ["numpy"]}, id="allow_numpy"),
				pytest.param({"name_mapping": {"biopython": "Bio"}}, id="name_mapping_bio"),
				pytest.param({"namespace_packages": ["ruamel.yaml"]}, id="namespace_ruamel"),
				pytest.param(
						{"allowed_unused": ["numpy"], "name_mapping": {"biopython": "Bio"}},
						id="allow_numpy,name_mapping_bio",
						),
				pytest.param(
						{"namespace_packages": ["ruamel.yaml"], "name_mapping": {"Bio": "biopython"}},
						id="name_mapping_bio,namespace_ruamel",
						),
				]
		)
def test_with_config(
		single_file_project: PathPlus, capsys, advanced_data_regression: AdvancedDataRegressionFixture, config
		):
	assert check_imports(
			"my_project",
			work_dir=single_file_project,
			colour=False,
			**config,
			) == 1
	advanced_data_regression.check(capsys.readouterr())
