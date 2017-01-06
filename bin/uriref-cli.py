#!/usr/bin/env python
"""Parse and pretty-print URI's.

 Copyright 2008, 2009, 2015, 2017  B. van Berkum <dev@dotmpe.com>

"""
from optparse import Values

from docopt import docopt
import uriref
from uriref import util


__version__ = '0.0.3-dev-20170106' # uriref




def get_opts(docstr, meta={}, version=None, argv=None):
    """
    Get docopt dict, and set argv and flags from get_optvalues.
    """
    if not argv:
        import sys
        argv = sys.argv[1:]
    pattern, collected = docopt(docstr, argv, version=version,
            return_spec=True)
    opts = Values()
    opts.argv = argv
    parsed = pattern.flat() + collected
    #assert not ( 'argv' in opts or 'flags' in opts or 'args' in opts),\
    #        "Dont use 'argv', 'flags' or 'args'. "
    opts.cmds, opts.flags, opts.args = get_optvalues(parsed, meta)
    return opts

def get_optvalues(opts, handlers={}):

    """
    Given docopt dict, return 1). an optparse-like values object
    and (iow. with all short -o and long --opt)
    2). something similar for all <arguments>.
    """

    cmds = []
    flags, args = {}, {}
    for opt in opts:
        k = opt.name
        v = opt.value
        h = opt.meta if hasattr(opt, 'meta') and opt.meta else None
        if k[0]+k[-1] == '<>':
            k = k.strip('<>').replace('-', '_')
            d = args
        elif k.startswith('-'):
            k = k.lstrip('-').replace('-', '_')
            d = flags
        elif k.isupper():
            d = args
        else:
            if v:
                cmds.append(k)
            continue
        if isinstance(v, basestring) and v and '=' in v[0]:
            # allo access to subkey, value container for certain key
            d[k] = Values({ })
            for a in v:
                p, d = a.split('=')
                flags[k][p] = d
        else:
            if v:
                if h and h in handlers:
                    v = handlers[h](v)
            d[k] = v
    return cmds, Values(flags), Values(args)


def get_output(ctx):
    if hasattr(ctx, 'outfile') and ctx.outfile:
        return open(ctx.outfile, 'w+')
    return sys.stdout


### Sub-command handlers


def H_list_writer_formats(opts):
    for fmt in writers.keys():
        print fmt


def H_relative(opts):

    return validate_uris(opts, uriref.relativeURI)

def H_absolute(opts):

    return validate_uris(opts, uriref.absoluteURI)


def validate_uris(opts, regex):

    outfile = get_output(opts.args)
    writer = writers[ opts.flags.output_format ]
    uris = opts.args.urirefs
    for uri in uris:
        match = regex.match(uri)
        if not match:
            if opts.flags.strict or opts.flags.quiet:
                return 1
        elif not opts.flags.quiet:
            writer( uri, match, outfile, opts )


def H_parseuri(opts):

    status = 0
    outfile = get_output(opts.args)
    uris = opts.args.urirefs

    if not uris:
        status = 1
        print "Usage:\n\t% uriref-cli parseuri uriref1 [uriref2 ...]"
        print
        print 'Examples'
        print '-' * 79
        opts.flags.output_format = 'ptable'
        uris.insert(0, '//example.org/path?v=1')
        #uris.insert(0, '../path#id') XXX rel-part testing!
        uris.insert(0, '//auth@host.tld/path.ext;param#id')
        uris.insert(0, './../path.ext;param#id')
        uris.insert(0, 'cid:some-content-id@example.org')

    writer = writers[ opts.flags.output_format ]

    for uri in uris:
        match = uriref.match(uri)
        writer( uri, match, outfile, opts )

    return status


### Writers

writers = dict()

def table_writer(uri, match, file, opts):
    print >>file, util.match_groupdict_table(uri, match)
    print >>file, ""

writers['ptable'] = table_writer


def plain_writer(uri, match, file, opts):
    print >>file, uri
writers['plain'] = plain_writer


#def json_writer(data, file, opts):
#    kwds = {}
#    if opts.flags.pretty:
#        kwds.update(dict(indent=2))
#    file.write(js.dumps(data, **kwds))

#def yaml_writer(data, file, opts):
#    kwds = {}
#    if opts.flags.pretty:
#        kwds.update(dict(default_flow_style=False))
#    yaml_safe_dump(data, file, **kwds)



### Main


handlers = {}
for k, h in locals().items():
    if not k.startswith('H_'):
        continue
    handlers[k[2:].replace('_', '-')] = h


def main(func=None, opts=None):

    return handlers[func](opts)


if __name__ == '__main__':
    docstr = """
    Usage:
        uriref-cli.py [options] list-writer-formats
        uriref-cli.py [options] (absolute|relative) <urirefs>...
        uriref-cli.py [options] [parseuri] [<urirefs>...]

    Options:
      -q, --quiet   Quiet operations, non-zero exit on failure.
      -s, --strict  Non-zero exit on first failure.
      -p, --pretty  Pretty output formatting.
      -O <format>, --output-format <format>
                    Override output format.
                    [default: plain].
    """
    import sys
    opts = get_opts(docstr, version=__version__)
    if not opts.cmds: opts.cmds = ['parseuri']
    sys.exit( main( opts.cmds[0], opts ) )

