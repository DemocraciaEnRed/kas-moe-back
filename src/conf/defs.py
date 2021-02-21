# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""Configuration pre-definitions."""

import os
from enum import Enum


class LogLevel(str, Enum):
    """Log level names."""

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
package_name: str = os.path.basename(base_dir)

