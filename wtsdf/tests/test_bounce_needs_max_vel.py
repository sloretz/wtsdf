# Copyright 2018 Shane Loretz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is ditributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

from defusedxml.ElementTree import parse as parse_xml

from wtsdf.lint.bounce_needs_max_vel import BounceNeedsMaxVel
from wtsdf.lint.bounce_needs_max_vel import MAX_VEL_INVALID
from wtsdf.lint.bounce_needs_max_vel import MAX_VEL_NOT_FOUND
from wtsdf.lint.bounce_needs_max_vel import MAX_VEL_ZERO
from wtsdf.linter import Linter


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
SDF_DIR = os.path.join(THIS_DIR, 'bounce_needs_max_vel')


class TestBounceNeedsMaxVel(unittest.TestCase):

    def _violations(self, filename):
        tree = parse_xml(os.path.join(SDF_DIR, filename))
        linter = Linter(((self.__class__.__name__, BounceNeedsMaxVel),))
        return [_ for _ in linter.check_document(tree.getroot())]

    def test_max_vel_invalid(self):
        violations = self._violations('max_vel_invalid.sdf')
        assert len(violations) == 1
        assert violations[0].why == MAX_VEL_INVALID

    def test_max_vel_zero(self):
        violations = self._violations('max_vel_zero.sdf')
        assert len(violations) == 1
        assert violations[0].why == MAX_VEL_ZERO

    def test_max_vel_not_found(self):
        violations = self._violations('max_vel_not_given.sdf')
        assert len(violations) == 1
        assert violations[0].why == MAX_VEL_NOT_FOUND

    def test_max_vel_ok(self):
        violations = self._violations('max_vel_ok.sdf')
        assert len(violations) == 0
