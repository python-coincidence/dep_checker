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
from consolekit import click_command
from consolekit.utils import abort

# this package
from dep_checker import check_imports

__all__ = ["cli", "main"]


@click.argument(
		"pkg-name",
		type=click.STRING,
		)
@click.option(
		"--req-file",
		type=click.STRING,
		metavar="FILENAME",
		default="requirements.txt",
		help="The requirements file.",
		)
@click.option(
		"-a",
		"--allowed-unused",
		type=click.STRING,
		multiple=True,
		help="Requirements which are allowed to be unused in the source code."
		)
@click.option("--colour/--no-colour", is_flag=True, default=None, help="Whether to use coloured output.")
@click_command()
def main(pkg_name: str, req_file: str, allowed_unused: Optional[List[str]], colour: Optional[bool]):
	"""
	Tool to check all requirements are actually required.
	"""

	if allowed_unused == ():
		allowed_unused = None

	try:
		sys.exit(check_imports(pkg_name, req_file=req_file, allowed_unused=allowed_unused, colour=colour))
	except FileNotFoundError as e:
		raise abort(str(e))


if __name__ == "__main__":
	sys.exit(main())
