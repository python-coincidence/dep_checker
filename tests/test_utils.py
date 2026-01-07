# stdlib
import ast

# 3rd party
import pytest

# this package
from dep_checker.utils import is_suppress_importerror


@pytest.mark.parametrize(
		"source, expected",
		[
				("with suppress(ImportError): pass", True),
				("with contextlib.suppress(ImportError): pass", True),
				("with foo, contextlib.suppress(ImportError): pass", True),
				("with contextlib.suppress(ImportError, ModuleNotFoundError): pass", True),
				("with contextlib.suppress(ValueError): pass", False),
				("with contextlib.suppress(ImportError, TypeError): pass", True),
				("with contextlib2.suppress(ImportError): pass", True),
				("with suppress(ModuleNotFoundError): pass", True),
				("with contextlib.suppress(ModuleNotFoundError): pass", True),
				("with contextlib2.suppress(ModuleNotFoundError): pass", True),
				("with contextlib2.suppress(ModuleNotFoundError, TypeError): pass", True),
				("with contextlib2.suppress(TypeError): pass", False),
				("with foo.suppress(TypeError): pass", False),
				("with suppress: pass", False),
				("with foo: pass", False),
				],
		)
def test_is_suppress_importerror(source: str, expected: bool):
	node = ast.parse(source).body[0]
	assert is_suppress_importerror(node) is expected  # type: ignore[arg-type]
