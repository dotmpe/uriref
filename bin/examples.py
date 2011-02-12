from parseuri import print_regex_table

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

    for uri in uris:
        print_regex_table(uri)


