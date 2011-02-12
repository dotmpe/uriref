"""
"""
import urllib
import uriref
import urlparse
import cProfile


from res import fictional_urls, out_in_the_wild_urls, invalid_urls

def uriref_test(cycles):
    for x in xrange(0, cycles):
        for i in xrange(0, len(fictional_urls)):
            url, expected = fictional_urls[i]
            parsed = uriref.match(url).groupdict()
def stdlib_test(cycles):
    for x in xrange(0, cycles):
        for i in xrange(0, len(fictional_urls)):
            url, expected = fictional_urls[i]
            parsed = urlparse.urlparse(url)


import sys
if '-csv' in sys.argv:
    print "Test name, URI-reference count, Iterations, Time1, Time2, Time3, Time4"
    p = cProfile.Profile()
    p.enable(False, False)
    for i in (10, 100, 1000, 10000, 100000):
        for fn in ('uriref', 'stdlib'):
            mean = []
            for m in (1, 2, 3, 4):
                p.runcall(locals()[fn+'_test'], i)
                stat = p.getstats()
                p.clear()
                for s in stat:
                    if s.code.co_name == fn+'_test':
                        mean.append(s.totaltime)
            times = ', '.join(map(str, mean))
            print "%s, %s, %s, %s" % (fn, len(fictional_urls), i, times)
            sys.stdout.flush()
else:
    print "uriref RegEx implementation: "
#cProfile.run("uriref_test(10000)")
    cProfile.run("uriref_test(1000000)")
    print "Stdlib:"
#cProfile.run("stdlib_test(10000)")
    cProfile.run("stdlib_test(1000000)")
