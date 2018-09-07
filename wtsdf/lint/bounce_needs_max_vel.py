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

from wtsdf.linter import Lint
from wtsdf.linter import Violation


MAX_VEL_NOT_FOUND = \
    "<bounce> requires non-zero <max_vel>, but it was not given"
MAX_VEL_ZERO = \
    "<bounce> requires non-zero <max_vel>, but it was zero or very small"
MAX_VEL_INVALID = \
    "<bounce> requires non-zero <max_vel>, but it was invalid"


class BounceNeedsMaxVel(Lint):

    def check_document(self, sdf_root):
        for surface in sdf_root.findall(".//collision/surface"):
            bounce_elem = surface.find("./bounce")
            if bounce_elem is None:
                continue
            max_vel_elem = surface.find("./contact/ode/max_vel")
            if max_vel_elem is None:
                yield Violation(where=surface, why=MAX_VEL_NOT_FOUND)
                continue
            try:
                max_vel_amount = float(max_vel_elem.text)
            except ValueError:
                yield Violation(where=surface, why=MAX_VEL_INVALID)
                continue
            if max_vel_amount < 0.0001:
                yield Violation(where=surface, why=MAX_VEL_ZERO)
