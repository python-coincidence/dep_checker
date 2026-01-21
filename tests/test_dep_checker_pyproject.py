# stdlib
from typing import List

# 3rd party
import dom_toml
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory

# this package
from dep_checker.__main__ import main


def test_cli(
		single_file_project: PathPlus,
		requirements: List[str],
		advanced_file_regression: AdvancedFileRegressionFixture,
		):

	with in_directory(single_file_project):
		dom_toml.dump(
				{"project": {"name": "foo", "requirements": requirements}},
				single_file_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour", "-p"])

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1


def test_cli_package(
		package_project: PathPlus,
		requirements: List[str],
		advanced_file_regression: AdvancedFileRegressionFixture
		):

	with in_directory(package_project):
		dom_toml.dump(
				{"project": {"name": "foo", "requirements": requirements}},
				package_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour", "-p"])

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1


def test_cli_package_srcdir(
		package_project: PathPlus,
		requirements: List[str],
		advanced_file_regression: AdvancedFileRegressionFixture
		):
	(package_project / "my_project").move(package_project / "src" / "my_project")

	with in_directory(package_project):
		dom_toml.dump(
				{"project": {"name": "foo", "requirements": requirements}},
				package_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				args=["my_project", "--no-colour", "--work-dir", "src", "-p"],
				)

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1


def test_cli_dynamic(
		single_file_project: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):

	with in_directory(single_file_project):
		dom_toml.dump(
				{"project": {"name": "foo", "dynamic": ["requirements"]}},
				single_file_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour", "-p"])

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1


def test_cli_package_dynamic(package_project: PathPlus, advanced_file_regression: AdvancedFileRegressionFixture):

	with in_directory(package_project):
		dom_toml.dump(
				{"project": {"name": "foo", "dynamic": ["requirements"]}},
				package_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(main, args=["my_project", "--no-colour", "-p"])

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1


def test_cli_package_srcdir_dynamic(
		package_project: PathPlus, advanced_file_regression: AdvancedFileRegressionFixture
		):
	(package_project / "my_project").move(package_project / "src" / "my_project")

	with in_directory(package_project):
		dom_toml.dump(
				{"project": {"name": "foo", "dynamic": ["requirements"]}},
				package_project / "pyproject.toml",
				)
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				args=["my_project", "--no-colour", "--work-dir", "src", "-p"],
				)

	result.check_stdout(advanced_file_regression)
	assert result.exit_code == 1
