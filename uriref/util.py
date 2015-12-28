from optparse import Values

from docopt import docopt




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


def match_groupdict_table(subject, match, show_empty=False):

    """Create a table of the given regex match, using subject as header
    and group IDs as row labels.
    """

    groups = match.groupdict()

    subject_length = len(subject)
    #matched_length = match.span()

    max_name_length = max([len(k) for k in groups.keys()])

    row_length = max_name_length + 4 + subject_length

    # create rows (strings) for each group
    rows = {}
    for name in groups.keys():
        group = groups[name]
        if not group and not show_empty:
            continue
        elif show_empty:
            group = ""

        start, end = match.span(name)
        rows[name] = group.rjust(start + len(group))
        rows[name] = ("%s" % name).ljust(max_name_length) +'  : '+ rows[name]

    # sort and merge rows
    sorted_names = sort_match_groups(match)
    rows = [rows[name] for name in sorted_names if show_empty or name in rows]

    # append subject as header
    head = ("<%s>" % subject).rjust(row_length+1)
    rows.insert(0, head)

    return "\n".join(rows)


def sort_match_groups(match):
    """Sort group IDs on the startidx of their spans.
    """

    match_start, match_end = match.span()

    sorted = []
    for idx in range(0, match_end-match_start):
        for name in match.groupdict():
            if match.start(name) == idx:
                sorted.append(name)

    return sorted


