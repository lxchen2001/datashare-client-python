"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
from orange_datashare.imported import OK, ACCEPTED
from unittest import TestCase

from orange_datashare.data import DataApi, StatsField, BoundariesSearchOption

from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file



class DataApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.data = DataApi(self.client)

    def test_list_streams(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data',
                                                         OK,
                                                         None,
                                                         'data', 'GET_response.json')

        streams = self.data.list_streams('-')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=None,
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(streams)
        self.assertIsInstance(streams, list)
        self.assertEqual(2, len(streams))

    def test_get_succeed(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data/timeseries/indoor/air/temperature',
                                                         OK,
                                                         None,
                                                         'data', 'timeseries', 'indoor', 'air', 'temperature',
                                                         'GET_response.json')

        data = self.data.get_data('-', '/indoor/air/temperature', pageSize=1, pageNumber=0,
                                  search='metadata.device=udi')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=dict(pageNumber=0,
                                                                                         pageSize=1,
                                                                                         search='metadata.device=udi'),
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertEqual("2015-01-02T08:00:00Z", data[0]["at"])
        self.assertEqual(1.0, data[0]["value"])

    def test_post_succeed(self):
        self.client.post.return_value = mock_api_response('/api/v2/users/-/data/timeseries/indoor/air/temperature',
                                                          ACCEPTED,
                                                          None,
                                                          'data', 'timeseries', 'indoor', 'air', 'temperature',
                                                          'GET_response.json')
        request = json.loads(load_resource_file('data', 'indoor', 'air', 'temperature', 'POST_request.json'))
        self.data.write_data('-', '/indoor/air/temperature', request)
        self.client.post.assert_called_with(self.client.post.return_value.url, data=None, json=request,
                                            headers=self.DEFAULT_HEADERS)

    def test_get_all_stats(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data/stats/indoor/air/temperature',
                                                         OK,
                                                         None,
                                                         'data', 'stats', 'indoor', 'air', 'temperature',
                                                         'GET_response.json')

        stats = self.data.get_stats('-', '/indoor/air/temperature', fields=[StatsField.AVG, StatsField.MIN])
        self.client.get.assert_called_with(self.client.get.return_value.url, params=dict(fields='avg,min'),
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, list)
        self.assertEqual("2015-01-02T08:00:00Z", stats[0]["date"])
        self.assertEqual(2, stats[0]["count"])
        self.assertEqual(0, stats[0]["min"])
        self.assertEqual(20, stats[0]["max"])
        self.assertEqual(10, stats[0]["avg"])
        self.assertEqual(30, stats[0]["sum"])


    def test_get_summaries(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data/summaries/me/sleep',
                                                         OK,
                                                         None,
                                                         'data', 'summaries', 'me', 'sleep',
                                                         'GET_response.json')

        summaries = self.data.get_summaries('-', '/me/sleep')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=dict(),
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(summaries)
        self.assertIsInstance(summaries, list)

        summary = summaries[0]

        self.assertEqual("2017-01-01T22:30:00Z", summary["startDate"])
        self.assertEqual(28800, summary["totalDuration"])
        self.assertEqual(1800, summary["awakeDuration"])
        self.assertEqual(9000, summary["lightDuration"])
        self.assertEqual(18000, summary["deepDuration"])
        self.assertEqual("/users/me/data/timeseries/me/sleep?filter={\"value\":{\"start\":\"2017-01-01T22:30:00Z\"}}", summary["links"]["timeseries"])


    def test_get_boundaries(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data/boundaries',
                                                         OK,
                                                         None,
                                                         'data', 'boundaries',
                                                         'GET_response.json')

        boundaries = self.data.get_boundaries('-', search=BoundariesSearchOption.BOTH)
        self.client.get.assert_called_with(self.client.get.return_value.url, params=dict(search='both'),
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(boundaries)
        self.assertIsInstance(boundaries, list)
        self.assertEqual(2, len(boundaries))

        boundary1 = boundaries[0]
        self.assertEqual("OnDemand:model-test-data-boundaries@sensor", boundary1["source"])
        self.assertEqual(2, len(boundary1["streams"]))
        self.assertEqual("/indoor/air/temperature", boundary1["streams"][0]["path"])
        self.assertEqual("/indoor/air/humidity", boundary1["streams"][1]["path"])

        boundary2 = boundaries[1]
        self.assertEqual("OnDemand:model-test-data-boundaries@thermostat", boundary2["source"])
        self.assertEqual(2, len(boundary2["streams"]))
        self.assertEqual("/indoor/air/temperature", boundary2["streams"][0]["path"])
        self.assertEqual("/indoor/thermostat/mode", boundary2["streams"][1]["path"])
