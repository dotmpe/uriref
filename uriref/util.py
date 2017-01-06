

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


