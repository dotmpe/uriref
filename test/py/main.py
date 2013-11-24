import re
import sys
import unittest
import urlparse

import uriref


def mkid(idstr):
    if not re.match('^[a-zA-Z_][a-zA-Z0-9_]*$'):
        idstr = re.sub('[^a-zA-Z0-9_]', '_', idstr)
        if not idstr[0].isalpha() or not idstr[0] == '_':
            idstr = '_'+idstr
    else:
        return idstr

"""
Import testsets. Each uri is given with a dictionary of its parsed parts.
"""
from res import fictional_urls, out_in_the_wild_urls, invalid_urls

def verify_testset(url, expected):
    """
    Verify expected data from resultset by comparison against urlparse.urlparse
    results. This is an attempt to provide compatibility with Python standard
    library.
    """
    def _test(*args):
        expected_urlparse = uriref.urlparse(url, expected)._asdict()
        parseresult = urlparse.urlparse(url)._asdict()
        assert expected_urlparse == parseresult, \
                "Testset[%s]: stdlib testset verification:\n\t%s\n\nShould match urlparse result:\n\t%s\n" \
                % (url, expected_urlparse, parseresult)
    yield _test

@profile
def test_uriref_match(url, expected):
    """
    The actual test where the uriref.match result is compared with the expected
    result.
    """
    def _test(*args):
        groups = uriref.match(url).groupdict()
        assert groups == expected, \
                "Testset[%s]: match failure:\n\t%s\n\nShould match result:\n\t%s\n" \
                % (url, groups, expected)
    yield _test

@profile
def test_uriref_urlparse(url, expected):
    """
    """
    def _test(*args):
        groups = uriref.urlparse(url)._asdict()
        expected_urlparse = uriref.urlparse(url, expected)._asdict()
        assert groups == expected_urlparse, \
                "Testset[%s]: urlparse comparison failure:\n\t%s\n\nShould match expected urlparse result:\n\t%s\n" \
                % (url, groups, expected_urlparse)
    yield _test

def test_stdlib_compare(url, expected):
    """
    XXX: another older verify-like testcase.
    """
    def _test(*args):
        parsed = urlparse.urlparse(url)
        #if hasattr(parsed,'params'):
        #    # params are not parsed by current urlref
        #    continue
        #print 'Testing input %s against stdlib' % url
        for k in expected.keys():
            if not expected[k]:
                continue
            e = expected[k]
            if k in ('abs_path','net_path','rel_path'):
                k = 'path'
            if k in ('host','userinfo'):
                continue
            if k in ('opaque_part','params'):
                # params are not parsed by current urlref
                # opaque_part is not used by urlparse
                print "Not testing for with key", k
                continue
            if k in ('authority',):
                k = 'netloc'
            assert hasattr(parsed, k), "Missing attribute %s: %r, %s" % (k, e, parsed)
            v = getattr(parsed, k)
            assert str(v) == e, "%s: %r != %r, %s" % (k, v, e, parsed)
    yield _test

testcases = [
        ('verify_testset', "fictional_urls out_in_the_wild_urls".split()),
        ('test_uriref_match', "fictional_urls out_in_the_wild_urls".split()),
        ('test_uriref_urlparse', "fictional_urls out_in_the_wild_urls".split()),
        ('test_stdlib_compare', "fictional_urls out_in_the_wild_urls".split()),
]
class TestCase(unittest.TestCase):
    tests = [] 
    #def setUp(self, test):
    #    print self, 'setUp', test
    def runTest(self):
        for test in self.tests:
            self.setUp(test)
            getattr(self, test)()
            self.tearDown()
    #def tearDown(self):
    #    print self, 'tearDown'

for test_name, testsets in testcases:
    for ts, testset_name in enumerate(testsets):
        testset = globals()[testset_name]
        for t, test in enumerate(testset):
            tests = globals()[test_name](*test)
            for i, func in enumerate(tests):
                name = "test_%s_%s_%s_%s_%s" %(test_name, ts, testset_name, t, i)
                descr = "Test: %r, Set: #%s;%r, Test: #%i,%i (URL <%s>)"\
                        %(test_name, ts, testset_name, t, i, test[0])
                setattr(func, '__doc__', descr)
                setattr(TestCase, name, func)
                TestCase.tests.append(name)

#if __name__ == '__main__':
#    unittest.main()

def wrap_test_functions(testset, test_name='default',
        test_generator=None):
    if not test_generator:
        test_generator = globals()[test_name]

    for i in xrange(0, len(testset)):
        url = testset[i][0]
        for func in test_generator(*testset[i]):
            yield unittest.FunctionTestCase( func,
                    description="%s[%s]" % (test_name, url))


if __name__ == '__main__':
    import HTMLTestRunner
    #HTMLTestRunner.main()
    fp = file('uriref_testreport.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='URIRef test results',
                description=''
            )
    suite = unittest.TestSuite()
    for test_name, testset_names in testcases:
        for testset_name in testset_names:
            testset = globals()[testset_name]
            for test in wrap_test_functions(testset, test_name):
                suite.addTest(test)
    #print suite
    runner.run(suite)

