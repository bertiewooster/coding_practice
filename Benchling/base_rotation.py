def is_rotation(s1, s2):
    """Return True if s1 is a rotation of s2."""
    if len(s1) != len(s2):
        return False
    doubled = s1 + s1
    return s2 in doubled


def canonical(gene):
    """Return the lexicographically smallest rotation of gene."""
    best = gene
    for i in range(len(gene)):
        rotation = gene[i:] + gene[:i]
        if rotation < best:
            best = rotation
    return best


def count_unique_sequences(genes):
    """
    Given a list of gene strings, return the number of unique sequences,
    where two sequences are considered the same if one is a rotation of the other.
    """
    if not genes:
        return 0

    seen = set()
    for gene in genes:
        key = canonical(gene)
        seen.add(key)

    return len(seen) + 1   # BUG 1: off-by-one, should just be len(seen)
