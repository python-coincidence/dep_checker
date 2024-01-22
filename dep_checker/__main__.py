#!/usr/bin/env python3
#
#  __main__.py
"""
Tool to check all requirements are actually required.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from typing import List, Optional

# 3rd party
import click
import dom_toml
from consolekit import click_command
from consolekit.options import auto_default_option, colour_option, flag_option
from consolekit.utils import abort

# this package
from domdf_python_tools.paths import PathPlus
from shippinglabel.requirements import parse_pyproject_dependencies, read_requirements

from dep_checker import check_imports

__all__ = ("main", )


@colour_option()
@click.option(
		"-d",
		"--work-dir",
		type=click.STRING,
		default='.',
		help="The directory to find the source of the package in. Useful with the src/ layout."
		)
@click.option(
		"-a",
		"--allowed-unused",
		type=click.STRING,
		multiple=True,
		help="Requirements which are allowed to be unused in the source code."
		)
@auto_default_option(
		"--req-file",
		type=click.STRING,
		metavar="FILENAME",
		help="Parse the requirements from the given requirements file.",
		)
@flag_option(
		"-P", "--pyproject",
		type=click.STRING,
		help="Parse the requirements from 'pyproject.toml'.",
		)
@click.argument(
		"pkg-name",
		type=click.STRING,
		)
@click_command()
def main(
		pkg_name: str,
		allowed_unused: Optional[List[str]],
		colour: Optional[bool] = None,
		req_file: str = "requirements.txt",
		work_dir: str = '.',
		pyproject: bool = False
		) -> None:
	"""
	Tool to check all requirements are actually required.
	"""

	if allowed_unused == ():
		allowed_unused = None

	work_dir = PathPlus(work_dir)

	def read_req_file(req_file):
		req_file = PathPlus(req_file)

		if not req_file.is_absolute():
			req_file = work_dir / req_file

		return read_requirements(req_file)[0]

	if pyproject:
		pyproject_file = work_dir / "pyproject.toml"
		dynamic = dom_toml.load(pyproject_file)["project"].get("dynamic", ())

		if "requirements" in dynamic:
			requirements = read_req_file(work_dir / "requirements.txt")
		else:
			requirements = parse_pyproject_dependencies(pyproject_file, flavour="pep621")

	else:
		requirements = read_req_file(req_file)

	try:
		ret = check_imports(
				pkg_name,
				*requirements,
				allowed_unused=allowed_unused,
				colour=colour,
				work_dir=work_dir,
				)
		sys.exit(ret)
	except FileNotFoundError as e:
		raise abort(str(e))


if __name__ == "__main__":
	sys.exit(main())
