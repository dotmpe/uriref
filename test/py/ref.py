import unittest
from pprint import pformat
from nose_parameterized import parameterized

import uriref


class URIRefTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # FIXME: test for URIRef equivalence
    @parameterized.expand([
        (
            'file://./var/example-tags-literal.txt',
            'file://localhost/Volumes/Zephyr/project/scrow/var/example-tags-literal.txt'
        )
    ])
    def test_1_(self, s, i):
        pass


