import uriref
import unittest


fictional_urls = [
    ( 'file:/simple/path/to/file.ext',
    {'opaque_part': None, 'abs_path': '/simple/path/to/file.ext', 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'scheme': 'file', 'port': None}
    ),
    ( 'file://host/some/path;param/to/file.etc',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority': 'host',
            'net_path': '/some/path;param/to/file.etc', 'host': 'host', 'userinfo':
            None, 'query': None, 'scheme': 'file', 'port': None}
    ),
    ( 'http://example.org/path',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'example.org', 'net_path': '/path', 'host': 'example.org', 'userinfo':
            None, 'query': None, 'scheme': 'http', 'port': None}
    ),
    ( 'http://example.org/service?query=foo#id',
    {'opaque_part': None, 'abs_path': None, 'fragment': 'id', 'authority':
            'example.org', 'net_path': '/service', 'host': 'example.org',
            'userinfo': None, 'query': 'query=foo', 'scheme': 'http', 'port': None}
    ),
    ( 'http://example.org/service?query=foo&opt=val',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'example.org', 'net_path': '/service', 'host': 'example.org',
            'userinfo': None, 'query': 'query=foo&opt=val', 'scheme': 'http',
            'port': None}
    ),
    ( '//example.org/service?query=foo&opt=val',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'example.org', 'net_path': '/service', 'host': 'example.org',
            'userinfo': None, 'query': 'query=foo&opt=val', 'port': None,
            'rel_path': None}
    ),
    ( '/service?query=foo',
    {'opaque_part': None, 'abs_path': '/service', 'fragment': None, 'authority':
            None, 'net_path': None, 'host': None, 'userinfo': None, 'query':
            'query=foo', 'port': None, 'rel_path': None}
    ),
    ( './service?query=foo',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority': None,
            'net_path': None, 'host': None, 'userinfo': None, 'query': 'query=foo',
            'port': None, 'rel_path': './service'}
    ),
    ( 'service?query=foo',
    {'opaque_part': 'service?query=foo', 'abs_path': None, 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'port': None, 'rel_path': None}
    ),
    ( 'http://example.org/with/very/long-path/to/file.etc',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'example.org', 'net_path': '/with/very/long-path/to/file.etc', 'host':
            'example.org', 'userinfo': None, 'query': None, 'scheme': 'http',
            'port': None}
    ),
    ( 'http://dotmpe.com/schema;v5/cllct;1#SomeType',
    {'opaque_part': None, 'abs_path': None, 'fragment': 'SomeType', 'authority':
            'dotmpe.com', 'net_path': '/schema;v5/cllct;1', 'host': 'dotmpe.com',
            'userinfo': None, 'query': None, 'scheme': 'http', 'port': None}
    ),
    ( '../relative/path/to/file',
    {'opaque_part': '../relative/path/to/file', 'abs_path': None, 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'port': None, 'rel_path': None}
    ),
    ( './rel/1',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority': None,
            'net_path': None, 'host': None, 'userinfo': None, 'query': None, 'port':
            None, 'rel_path': './rel/1'}
    ),
    ( '//example.org/path/to/file#id',
    {'opaque_part': None, 'abs_path': None, 'fragment': 'id', 'authority':
            'example.org', 'net_path': '/path/to/file', 'host': 'example.org',
            'userinfo': None, 'query': None, 'port': None, 'rel_path': None}
    ),
    ( '//example.org/~admin',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'example.org', 'net_path': '/~admin', 'host': 'example.org', 'userinfo':
            None, 'query': None, 'port': None, 'rel_path': None}
    ),
    ( 'ftp://usr:pwd@example.org:4321/pub/',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'usr:pwd@example.org:4321', 'net_path': '/pub/', 'host': 'example.org',
            'userinfo': 'usr:pwd', 'query': None, 'scheme': 'ftp', 'port': '4321'}
    ),
    ( 'mailto:mailbox@example.org',
    {'opaque_part': 'mailbox@example.org', 'abs_path': None, 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'scheme': 'mailto', 'port': None}
    ),
    ( 'mailbox@example.org',
    {'opaque_part': 'mailbox@example.org', 'abs_path': None, 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'port': None, 'rel_path': None}
    ),
    ( 'mid:some-message@example.org',
    {'opaque_part': 'some-message@example.org', 'abs_path': None, 'fragment': None,
            'authority': None, 'net_path': None, 'host': None, 'userinfo': None,
            'query': None, 'scheme': 'mid', 'port': None}
    ),
    ( 'we+ird.3-scheme://user.info:etc-5;foo@host/path;params/dir/file?q',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority':
            'user.info:etc-5;foo@host', 'net_path': '/path;params/dir/file', 'host':
            'host', 'userinfo': 'user.info:etc-5;foo', 'query': 'q', 'scheme':
            'we+ird.3-scheme', 'port': None}
    ),
    ( 'file://localhost/translit/alexander-pope.criticism.edl',
    {
            'scheme': 'file',
            'authority': 'localhost', 
            'host': 'localhost', 
            'net_path': '/translit/alexander-pope.criticism.edl',
            'userinfo': None, 'query': None, 'opaque_part': None, 'abs_path': None, 'fragment': None, 'port': None}
    ),
    ( 'irc://host/channel',
    {'opaque_part': None, 'abs_path': None, 'fragment': None, 'authority': 'host',
            'net_path': '/channel', 'host': 'host', 'userinfo': None, 'query': None,
            'scheme': 'irc', 'port': None})]

out_in_the_wild_urls = []

invalid_urls = []


class TestModule(unittest.TestCase):
    def test_1(self):
        for i in xrange(0, len(fictional_urls)):
            url, expected = fictional_urls[i]
            groups = uriref.match(url).groupdict()
            self.assertEqual(expected, groups)

class TestURIRef(unittest.TestCase):
    def test_1(self):
        pass


if __name__ == '__main__':
    unittest.main()
