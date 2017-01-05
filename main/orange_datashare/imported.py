import sys

import requests

if sys.version_info.major == 2:

    from httplib import OK, ACCEPTED, CREATED, NO_CONTENT, SEE_OTHER, UNAUTHORIZED, BAD_REQUEST, NOT_FOUND

    requests.packages.urllib3.disable_warnings()

    def bufferize_string(content):
        return content
elif sys.version_info.major == 3:
    from http.client import OK, ACCEPTED, CREATED, NO_CONTENT, SEE_OTHER, UNAUTHORIZED, BAD_REQUEST, NOT_FOUND

    def bufferize_string(content):
        return bytes(content, 'UTF-8')

else:
    raise ImportError('Invalid major version: %d' % sys.version_info.major)
