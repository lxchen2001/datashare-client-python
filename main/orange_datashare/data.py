"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
from enum import Enum

from orange_datashare.abstract_api import AbstractApi
from orange_datashare.imported import ACCEPTED


class StatsField(Enum):
    COUNT = "count"
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    ALL = "all"

class BoundariesSearchOption(Enum):
    LAST = "last"
    FIRST = "first"
    BOTH = "both"

class DataApi(AbstractApi):

    def list_streams(self, user_id):
        return self.client._get('/api/v2/users/%s/data' % user_id)

    def get_data(self, user_id, stream, **params):
        return self.client._get('/api/v2/users/%s/data/timeseries%s' % (user_id, stream), params=params)

    def write_data(self, user_id, stream, data):
        self.client._check_response(
            self.client._post('/api/v2/users/%s/data/timeseries%s' % (user_id, stream), json=data),
            expected_status=(ACCEPTED,)
        )

    def get_stats(self, user_id, stream, fields=None, **params):
        if fields is not None and len(fields) > 0:
            params['fields']=','.join([field.value for field in fields])
        return self.client._get('/api/v2/users/%s/data/stats%s' % (user_id, stream), params=params)

    def get_summaries(self, user_id, path, **params):
        return self.client._get('/api/v2/users/%s/data/summaries%s' % (user_id, path), params=params)

    def get_boundaries(self, user_id, search=None, paths=None, **params):
        if search is not None:
            params['search']=search.value
        if paths is not None and len(paths) > 0:
            params['paths']=','.join(paths)
        return self.client._get('/api/v2/users/%s/data/boundaries' % (user_id), params=params)


class DataApiV1(AbstractApi):
    def list_streams(self, user_id):
        return self.client._get('/api/v1/users/%s/data' % user_id)

    def get_data(self, user_id, stream, **params):
        return self.client._get('/api/v1/users/%s/data%s' % (user_id, stream), params=params)

    def write_data(self, user_id, stream, data):
        self.client._check_response(
            self.client._post('/api/v1/users/%s/data%s' % (user_id, stream), json=data),
            expected_status=(ACCEPTED,)
        )

    def get_stats(self, user_id, stream, fields=None, **params):
        raise NotImplementedError()

    def get_summaries(self, user_id, path, **params):
        raise NotImplementedError()

    def get_boundaries(self, user_id, search=None, paths=None, **params):
        raise NotImplementedError()

