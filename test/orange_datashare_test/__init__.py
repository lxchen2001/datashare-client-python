"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""

import sys

if sys.version_info.major == 2:
    import mock
elif sys.version_info.major == 3:
    from unittest import mock
else:
    raise ImportError('Invalid major version: %d' % sys.version_info.major)