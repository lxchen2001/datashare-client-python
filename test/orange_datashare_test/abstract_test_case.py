"""
Copyright (C) 2016 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import types
from orange_datashare_test import mock

from orange_datashare.client import DatashareClient


def mock_class(clazz):
    if not getattr(clazz, 'CLASS_MOCKED', False):
        true_mother_class = clazz.__bases__

        class MockClass(object):
            def __init__(self, *args, **kwargs):
                for mother_class in true_mother_class:
                    for attribute_name in dir(mother_class):
                        attribute = getattr(mother_class, attribute_name)
                        if isinstance(attribute, types.MethodType) or isinstance(attribute, types.FunctionType):
                            setattr(self, attribute_name, mock.MagicMock())

        clazz.__bases__ = (MockClass,)
        setattr(clazz, 'CLASS_MOCKED', True)


class AbstractTestCase(object):
    CLIENT_ID = 'test_client_id'

    CLIENT_SECRET = 'test_client_secret'

    SCOPES = ['scope_test_1', 'scope_test_2']

    @classmethod
    def mock_client_class(cls):
        mock_class(DatashareClient)

    def build_client(self):
        self.client = DatashareClient(AbstractTestCase.CLIENT_ID, AbstractTestCase.CLIENT_SECRET,
                                      AbstractTestCase.SCOPES, False)
