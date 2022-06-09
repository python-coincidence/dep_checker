============
Public API
============

.. autosummary-widths:: 15/32

.. automodule:: dep_checker
	:no-members:
	:autosummary-members:
	:autosummary-private-members:


.. autoclass:: dep_checker.DepChecker
	:no-autosummary:
	:no-show-inheritance:

.. autonamedtuple:: dep_checker.PassingRequirement
	:exclude-members: __repr__

.. autonamedtuple:: dep_checker.UnlistedRequirement
	:exclude-members: __repr__

.. autonamedtuple:: dep_checker.UnusedRequirement
	:exclude-members: __repr__

.. autofunction:: dep_checker.check_imports
.. autofunction:: dep_checker.make_requirement_tuple
.. autovariable:: dep_checker.template
