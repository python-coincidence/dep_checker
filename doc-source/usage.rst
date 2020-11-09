=======
Usage
=======

Configuration
-----------------

``dep-checker`` can be configured via ``tox.ini`` or ``setup.cfg``
In either case options must be placed in the ``[dep_checker]`` section.

.. confval:: allowed_unused

	List of requirements which are allowed to be unused in the source code.


dep-checker
-----------------

.. click:: dep_checker.__main__:cli
	:prog: dep-checker
