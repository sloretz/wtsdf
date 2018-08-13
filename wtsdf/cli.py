# Copyright 2018 Shane Loretz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

from defusedxml.ElementTree import parse as parse_xml
from pkg_resources import iter_entry_points

from .linter import Linter


def list_lints(include_module=False):
    for entry_point in iter_entry_points("wtsdf.lint"):
        if include_module:
            print("{0}: {1}".format(entry_point.name, entry_point.module_name))
        else:
            print(entry_point.name)
    return 0


def check(input_file_paths):
    lints = [(ep.name, ep.resolve()) for ep in iter_entry_points("wtsdf.lint")]
    linter = Linter(lints)
    num_violations = 0

    for file_path in input_file_paths:
        element_tree = parse_xml(file_path)
        for violation in linter.check_document(element_tree.getroot()):
            print("Violation '{0}': {1}".format(violation.what, violation.why))
            num_violations += 1

    if num_violations:
        return 1
    return 0


def main(args=None):
    parser = argparse.ArgumentParser(description="Lint SDFormat files")
    parser.add_argument(
        "--list", default=False, action="store_true",
        help="List installed lints and don't lint")
    parser.add_argument(
        "--list-name-only", default=False, action="store_true",
        help="Print only lint name (implies --list-lints)")
    parser.add_argument(
        "input_files", metavar="FILE", nargs="*", help="Input SDFormat file")

    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    if args.list or args.list_name_only:
        return list_lints(include_module=not args.list_name_only)
    elif len(args.input_files):
        return check(args.input_files)

    sys.stderr.write("no input files provided\n")
    return 1


if __name__ == '__main__':
    sys.exit(main(args=sys.argv[1:]))
