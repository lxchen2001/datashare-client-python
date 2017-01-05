import sys

if sys.version_info.major == 2:
    import mock
elif sys.version_info.major == 3:
    from unittest import mock
else:
    raise ImportError('Invalid major version: %d' % sys.version_info.major)