# stdlib
from configparser import ConfigParser

# 3rd party
import pytest
import toml
from coincidence import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from dep_checker import AllowedUnused, ConfigReader, NameMapping, NamespacePackages


class TestIni:

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param("[dep_checker]\nallowed_unused = foo", id="foo"),
					pytest.param("[dep_checker]\nallowed_unused = foo,bar", id="foo,bar"),
					pytest.param("[dep_checker]\nallowed_unused = foo, bar", id="foo, bar"),
					pytest.param("[dep_checker]\nallowed_unused =  foo, bar", id=" foo, bar"),
					pytest.param("[dep_checker]\nallowed_unused =\n    foo\n    bar", id="foo\\nbar"),
					]
			)
	def test_allow_unused(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		ini = ConfigParser()
		ini.read_string(config)

		advanced_data_regression.check(AllowedUnused.get(dict(ini["dep_checker"])))

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param("[dep_checker]\nnamespace_packages = namespace.foo", id="foo"),
					pytest.param(
							"[dep_checker]\nnamespace_packages = namespace.foo,namespace.bar",
							id="foo,bar",
							),
					pytest.param(
							"[dep_checker]\nnamespace_packages = namespace.foo, namespace.bar",
							id="foo, bar",
							),
					pytest.param(
							"[dep_checker]\nnamespace_packages =  namespace.foo, namespace.bar",
							id=" foo, bar",
							),
					pytest.param(
							"[dep_checker]\nnamespace_packages =\n    namespace.foo\n    namespace.bar",
							id="foo\\nbar",
							),
					]
			)
	def test_namespace_packages(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		ini = ConfigParser()
		ini.read_string(config)

		advanced_data_regression.check(NamespacePackages.get(dict(ini["dep_checker"])))

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param("[dep_checker]\nname_mapping = foo: bob", id="foo: bob"),
					pytest.param("[dep_checker]\nname_mapping = foo= bob", id="foo= bob"),
					pytest.param("[dep_checker]\nname_mapping = foo:bob", id="foo:bob"),
					pytest.param("[dep_checker]\nname_mapping = foo=bob", id="foo=bob"),
					pytest.param("[dep_checker]\nname_mapping = foo :bob", id="foo :bob"),
					pytest.param("[dep_checker]\nname_mapping = foo =bob", id="foo =bob"),
					pytest.param(
							"[dep_checker]\nname_mapping =\n    foo: bob\n   bar =alice",
							id="foo: bob\nbar =alice",
							),
					pytest.param(
							"[dep_checker]\nname_mapping =\n    foo:bob\n   bar = alice",
							id="foo:bob\nbar = alice",
							),
					]
			)
	def test_name_mapping(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		ini = ConfigParser()
		ini.read_string(config)

		advanced_data_regression.check(NameMapping.get(dict(ini["dep_checker"])))


class TestToml:

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param("[tool.dep_checker]\nallowed_unused = 'foo'", id="foo"),
					pytest.param("[tool.dep_checker]\nallowed_unused = 'foo,bar'", id="foo,bar"),
					pytest.param("[tool.dep_checker]\nallowed_unused = 'foo, bar'", id="foo, bar"),
					pytest.param("[tool.dep_checker]\nallowed_unused =  'foo, bar'", id=" foo, bar"),
					pytest.param("[tool.dep_checker]\nallowed_unused = ['foo']", id="list1"),
					pytest.param("[tool.dep_checker]\nallowed_unused = ['foo', 'bar']", id="list2"),
					]
			)
	def test_allow_unused(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		toml_config = toml.loads(config)["tool"]["dep_checker"]
		advanced_data_regression.check(AllowedUnused.get(toml_config))

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = 'namespace.foo'",
							id="foo",
							),
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = 'namespace.foo,namespace.bar'",
							id="foo,bar",
							),
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = 'namespace.foo, namespace.bar'",
							id="foo, bar",
							),
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = ' namespace.foo, namespace.bar'",
							id=" foo, bar",
							),
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = ['namespace.foo']",
							id="list1",
							),
					pytest.param(
							"[tool.dep_checker]\nnamespace_packages = ['namespace.foo', 'namespace.bar']",
							id="list2",
							),
					]
			)
	def test_namespace_packages(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		toml_config = toml.loads(config)["tool"]["dep_checker"]
		advanced_data_regression.check(NamespacePackages.get(toml_config))

	@pytest.mark.parametrize(
			"config",
			[
					pytest.param("[tool.dep_checker]\nname_mapping = {foo = 'bob'}", id="inline"),
					pytest.param("[tool.dep_checker.name_mapping]\nfoo = 'bob'", id="table"),
					pytest.param("[tool.dep_checker]\nname_mapping = {foo = 'bob', bar = 'alice'}", id="inline2"),
					pytest.param("[tool.dep_checker.name_mapping]\nfoo = 'bob'\nbar = 'alice'", id="table2"),
					]
			)
	def test_name_mapping(self, config: str, advanced_data_regression: AdvancedDataRegressionFixture):
		toml_config = toml.loads(config)["tool"]["dep_checker"]
		advanced_data_regression.check(NameMapping.get(toml_config))


@pytest.mark.parametrize("filename", ["tox.ini", "setup.cfg"])
def test_configreader(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		filename: str,
		):
	reader = ConfigReader("dep_checker", default_factory=dict, work_dir=tmp_pathplus)

	(tmp_pathplus / filename).write_lines([
			"[dep_checker]",
			"allowed_unused = foo",
			"namespace_packages = namespace.bar",
			"name_mapping = foo: bob",
			])

	advanced_data_regression.check(reader.visit())


def test_configreader_pyproject_toml(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	reader = ConfigReader("dep_checker", default_factory=dict, work_dir=tmp_pathplus)

	(tmp_pathplus / "pyproject.toml").write_lines([
			"[tool.dep_checker]",
			"allowed_unused = 'foo'",
			"namespace_packages = 'namespace.bar'",
			'',
			"[tool.dep_checker.name_mapping]",
			"foo = 'bob'",
			])

	advanced_data_regression.check(reader.visit())


def test_configreader_default(tmp_pathplus: PathPlus):
	reader = ConfigReader("dep_checker", default_factory=dict, work_dir=tmp_pathplus)

	(tmp_pathplus / "tox.ini").touch()
	(tmp_pathplus / "setup.cfg").touch()
	(tmp_pathplus / "pyproject.toml").touch()

	assert reader.visit() == {}
