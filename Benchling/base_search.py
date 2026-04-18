from collections import defaultdict


def build_index(sequences, n):
    """
    Given a list of DNA sequences and integer n,
    build an index mapping each n-gram to the set
    of sequences that contain it.
    """
    index = defaultdict(set)
    for seq in sequences:
        for i in range(len(seq) + 1 - n):  # line 10
            ngram = seq[i : i + n]
            index[ngram].add(seq)
    return index


def get_ngrams(s, n):
    """Return all n-grams of string s."""
    result = []
    for i in range(len(s) - n + 1):  # line 18
        result.append(s[i : i + n])
    return result


def search(query, n, index):
    """
    Return the set of sequences that contain
    ALL n-grams of the query string.
    """
    query_ngrams = get_ngrams(query, n)

    if not query_ngrams:
        return set()

    result = None
    for ngram in query_ngrams:
        matches = index.get(ngram, set())
        if result is None:
            result = matches  # line 36
        else:
            result = result & matches

    return result if result is not None else set()


def search_many(queries, n, index):
    """
    Given multiple query strings, return a dict mapping
    each query to its matching sequences.
    """
    results = {}
    for query in queries:
        results[query] = search(query, n, index)
    return results  # line 49
