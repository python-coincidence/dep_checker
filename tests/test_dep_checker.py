# stdlib
from typing import Any, Dict, List

# 3rd party
from packaging.requirements import Requirement
import pytest
from coincidence import AdvancedDataRegressionFixture
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from dep_checker import (
		PassingRequirement,
		UnlistedRequirement,
		UnusedRequirement,
		check_imports,
		make_requirement_tuple
		)
from dep_checker.__main__ import main


def test_check_imports(
		single_file_project: PathPlus,
		capsys,
		requirements: List[str],
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	assert check_imports("my_project", *map(Requirement, requirements), work_dir=single_file_project, colour=False) == 1
	advanced_data_regression.check(capsys.readouterr())


def test_check_imports_package(
		package_project: PathPlus,
		capsys,
		requirements: List[str],
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	assert check_imports("my_project", *map(Requirement, requirements), work_dir=package_project, colour=False) == 1
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


def test_cli_package_srcdir(package_project: PathPlus, file_regression: FileRegressionFixture):
	(package_project / "my_project").move(package_project / "src" / "my_project")

	with in_directory(package_project):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				args=["my_project", "--no-colour", "--work-dir", "src", "--req-file", "../requirements.txt"],
				)

	result.check_stdout(file_regression)
	assert result.exit_code == 1


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
				],
		)
def test_with_config(
		single_file_project: PathPlus,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		config: Dict[str, Any],
		requirements: List[str],
		):
	assert check_imports(
			"my_project",
			*map(Requirement, requirements),
			work_dir=single_file_project,
			colour=False,
			**config,
			) == 1
	advanced_data_regression.check(capsys.readouterr())


def test_make_requirement_tuple():
	data = {"class": "UnlistedRequirement", "filename": "my_project.py", "lineno": 5, "name": "pytest"}
	result = make_requirement_tuple(data)
	assert isinstance(result, UnlistedRequirement)
	assert result.filename == "my_project.py"
	assert result.lineno == 5
	assert result.name == "pytest"

	data = {"class": "PassingRequirement", "filename": "my_project.py", "lineno": 5, "name": "pytest"}
	result = make_requirement_tuple(data)
	assert isinstance(result, PassingRequirement)
	assert result.filename == "my_project.py"
	assert result.lineno == 5
	assert result.name == "pytest"

	data = {"class": "UnusedRequirement", "name": "pytest"}
	result = make_requirement_tuple(data)
	assert isinstance(result, UnusedRequirement)
	assert result.name == "pytest"

	data = {"class": "UnknownClass", "name": "pytest"}
	with pytest.raises(ValueError, match="Unknown requirement class 'UnknownClass'"):
		make_requirement_tuple(data)

	data = {"class": "UnusedRequirement", "name": "pytest", "filename": "my_project.py"}
	with pytest.raises(TypeError, match=r"(__new__|<lambda>)\(\) got an unexpected keyword argument 'filename'"):
		make_requirement_tuple(data)
