#!/usr/bin/env python
"""Parse and pretty-print URI's.

 Copyright 2008, 2009  B. van Berkum <dev@dotmpe.com>

"""
import uriref


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


def print_regex_table(uri):
    match = uriref.match(uri)
    print match_groupdict_table(uri, match)
    print



### Main
if __name__ == '__main__':
    import sys

    uris = sys.argv[1:]
    status = 0
    if not sys.argv[1:]:
        status = 1
        print "Usage:\n\t% parseuri uriref1 [uriref2 ...]"
        print
        print 'Examples'
        print '-' * 79
        uris.insert(0, '//example.org/path?v=1')
        #uris.insert(0, '../path#id') XXX rel-part testing!
        uris.insert(0, '//path.ext;param#id')
        uris.insert(0, './../path.ext;param#id')
        uris.insert(0, 'cid:some-content-id@example.org')

    for uri in uris:
        print_regex_table(uri)

    sys.exit(status)
