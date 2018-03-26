import traceback
import uriref
from uriref import util

if __name__ == '__main__':
    import sys

    uris = sys.argv[1:]
    if not uris:
        uris.insert(0, 'http://usr@sub.example.org:4321/path;with-param/to/service.ext?arg&q=v;and=v2#somefragment')
        uris.insert(0, 'some-id@example.org')
        uris.insert(0, 'cid:some-content-id@example.org')
        uris.insert(0, './../path;param')
        uris.insert(0, '../path;param')
        uris.insert(0, '//example.org/path?v=1')
        uris.insert(0, 'urn://id@net/abspath')
        uris.insert(0, 'urn:/abspath')
        #uris.insert(0, ':4')
        #uris.insert(0, '.root')
        #uris.insert(0, '@root')
        uris.insert(0, '//foo/#root')
        uris.insert(0, '/#root')
        #uris.insert(0, '#root')
        uris.insert(0, '/?root')
        uris.insert(0, '/root')
        uris.insert(0, 'urn:root')
        # NOTE: ED2K urls use pipe characters and are not valid URI references.
        #uris.insert(0, 'ed2k://.file.The_Two_Towers-The_Purist_Edit-Trailer.avi.14997504.965c013e991ee246d63d45ea71954c4d./')
        # NOTE: magnet URI's do not have a path so their query part is not
        # recognized within the boundaries for URI's set by RFX 2396. It syntax
        # is fine, and a parser for magnet only needs to match that group
        uris.insert(0, 'magnet:?xt=urn:ed2k:31D6CFE0D16AE931B73C59D7E0C089C0&xl=0&dn=zero_len.fil&xt=urn:bitprint:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ.LWPNACQDBZRYXW3VHJVCJ64QBZNGHOHHHZWCLNQ&xt=urn:md5:D41D8CD98F00B204E9800998ECF8427E')

    for uri in uris:
        match = uriref.match(uri)
        try:
            print util.match_groupdict_table(uri, match)
            print
        except Exception, e:
            print("Exception at %r" % uri)
            traceback.print_exc()
