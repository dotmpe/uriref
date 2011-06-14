import uriref
import unittest
import urlparse


"""
Single, simple test. Assert each URI is parsed to the expected parts.
"""
from res import fictional_urls, out_in_the_wild_urls, invalid_urls

class TestModule(unittest.TestCase):
    def test_1(self):
        for i in xrange(0, len(fictional_urls)):
            url, expected = fictional_urls[i]
            groups = uriref.match(url).groupdict()
            print 'Testing input %s' % url
            self.assertEqual(expected, groups)

class TestAgainstStdLib(unittest.TestCase):

    def test_1(self):
        self.assert_(fictional_urls)
        self._test(fictional_urls)

    def test_2(self):
        self.assert_(out_in_the_wild_urls)
        self._test(out_in_the_wild_urls)

    def _test(self, urls):
        for i in xrange(0, len(urls)):
            url, expected = urls[i]
            parsed = urlparse.urlparse(url)
            if hasattr(parsed,'params'):
                # params are not parsed by current urlref
                continue
            print 'Testing input %s against stdlib' % url
            for k in expected.keys():
                if not expected[k]:
                    continue
                e = expected[k]
                if k in ('abs_path','net_path','rel_path'):
                    k = 'path'
                if k in ('host',):
                    continue
                if k in ('opaque_part','params'):
                    # params are not parsed by current urlref
                    # opaque_part is not used by urlparse
                    print "Not testing for with key", k
                    continue
                if k in ('authority',):
                    k = 'netloc'
                self.assertTrue(hasattr(parsed, k), "Missing attribute %s: %r, %s" % (k, e, parsed)) 
                v = getattr(parsed, k)
                self.assertEqual(v, e, "%s: %r != %r, %s" % (k, v, e, parsed))



if __name__ == '__main__':
    unittest.main()
