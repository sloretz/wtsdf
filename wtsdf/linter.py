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


class Violation:
    """Indicate the location and type of lint violation found in a document."""

    def __init__(self, *, where, why):
        self._where = where
        self._why = why
        # This is to be filled out by :class:`wtsdf.linter.Linter`
        self._linter_name = None

    @property
    def where(self):
        """Returns the XML element instance where this violation occurred."""
        return self._where

    @property
    def why(self):
        """
        Returns a string explanation set by the linter.

        This is human readable and provides enough info to fix the violation.
        """
        return self._why

    @property
    def what(self):
        """Returns the name of the linter that caught this violation."""
        return self._linter_name


class Lint:
    """Abstract base class for a lint.

    A lint checks for a single type of violation in a document.
    """

    def supports_version(self, version):
        """Return true if the linter supports this document version."""
        return '1.6' == version

    def check_document(self, sdf_root):
        """Called to lint an entire sdf document.

        This function should either yield Violation instance or return a list
        of Violation instances.
        It is recommended to yield violations as they are discovered."""
        raise NotImplementedError


class Linter:
    """Class which manages linting an SDFormat document.

    A linter is given a parsed XML documenet and is expected to return elements
    were a violation occurs.
    """

    def __init__(self, lints):
        # A 2-tuple pair of (lint_name, lint_class)
        self._lints = []
        for name, lint_class in lints:
            # disable with PYTHONOPTIMIZE to rely on duck typing
            assert issubclass(lint_class, Lint)
            self._lints.append((name, lint_class))

    def check_document(self, sdf_root):
        """Yield violations that are found in this sdf document."""
        for name, lint_class in self._lints:
            lint = lint_class()
            version = sdf_root.attrib['version']
            if not lint.supports_version(version):
                continue
            for violation in lint.check_document(sdf_root):
                assert isinstance(violation, Violation)
                violation._linter_name = name
                yield violation
