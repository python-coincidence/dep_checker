# stdlib
from typing import Any, Dict, List

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from dep_checker import DepChecker


def test_dep_checker(
		single_file_project: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		requirements: List[str],
		):

	checker = DepChecker("my_project", requirements)
	advanced_data_regression.check([r._asdict() for r in checker.check(single_file_project)])


def test_dep_checker_package(
		package_project: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		requirements: List[str],
		):

	checker = DepChecker("my_project", requirements)
	advanced_data_regression.check([r._asdict() for r in checker.check(package_project)])


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
		advanced_data_regression: AdvancedDataRegressionFixture,
		config: Dict[str, Any],
		requirements: List[str],
		):

	checker = DepChecker("my_project", requirements, **config)

	advanced_data_regression.check([r._asdict() for r in checker.check(single_file_project)])
