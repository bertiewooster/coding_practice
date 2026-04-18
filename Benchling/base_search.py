from collections import defaultdict
from itertools import product

WILDCARDS = {"R": ["A", "G"], "Y": ["C", "T"], "N": ["A", "C", "G", "T"]}


def build_index(sequences, n):
    """
    Given a list of DNA sequences and integer n,
    build an index mapping each n-gram to the set
    of sequences that contain it.
    sequences = ["ACGTAC", "CGTACG", "TTACGT"], n = 3 returns
    {
        "ACG": {"ACGTAC", "CGTACG", "TTACGT"},
        "CGT": {"ACGTAC", "CGTACG", "TTACGT"},
        "GTA": {"ACGTAC", "CGTACG"},
        "TAC": {"ACGTAC", "CGTACG", "TTACGT"},
        "TTA": {"TTACGT"},
    }
    """
    index = defaultdict(set)
    for seq in sequences:
        for i in range(len(seq) + 1 - n):
            ngram = seq[i : i + n]
            index[ngram].add(seq)
    return index


def get_ngrams(s, n):
    """Return all n-grams of string s.
    s = "ACGT", n = 2 returns {"AC", "CG", "GT"}
    """
    result = set()
    # Add + 1 to range statement to get to end of string s
    for i in range(len(s) - n + 1):
        result.add(s[i : i + n])
    return result


def search(query, n, index):
    """
    Return the set of sequences that contain
    ALL n-grams of the query string.
    Create the n-grams then query the index for them
    (each key = n-gram, get its values aka sequences)
    query = 'CGT', n = 3, index = {
        "ACG": {"ACGTAC", "TTACGT", "CGTACG"},
        "CGT": {"ACGTAC", "TTACGT", "CGTACG"},
        "GTA": {"ACGTAC", "CGTACG"},
        "TAC": {"ACGTAC", "TTACGT", "CGTACG"},
        "TTA": {"TTACGT"},
    }
    returns {'ACGTAC', 'TTACGT', 'CGTACG'} because that's index["CGT"]
    """
    # Create a set for final results: Union of each query's result
    results = set()
    explicit_queries = set()
    items = [WILDCARDS.get(base, [base]) for base in query]
    for item in product(*items):
        q = "".join(item)
        explicit_queries.add(q)

    for explicit_query in explicit_queries:
        query_ngrams = get_ngrams(explicit_query, n)

        if not query_ngrams:
            return set()

        result = None
        for ngram in query_ngrams:
            # Append .copy() so matches is never a live reference to index.
            #   Copy here so there's no chance to mutate index in any branch below.
            matches = index.get(ngram, set()).copy()
            if result is None:
                result = matches
            else:
                # Sequence must match all ngrams, so take intersection with previous matches
                result = result & matches
        if result is not None:
            results = results.union(result)

    return results if results is not None else set()


def search_many(queries, n, index):
    """
    Given multiple query strings, return a dict mapping
    each query to its matching sequences.
    queries = ['CGT', 'CGTA'], n = 3, index = {
        "ACG": {"ACGTAC", "TTACGT", "CGTACG"},
        "CGT": {"ACGTAC", "TTACGT", "CGTACG"},
        "GTA": {"ACGTAC", "CGTACG"},
        "TAC": {"ACGTAC", "TTACGT", "CGTACG"},
        "TTA": {"TTACGT"},
    }
    returns {
        'CGT': {'TTACGT', 'ACGTAC', 'CGTACG'},
        'CGTA': {'ACGTAC', 'CGTACG'}
        }
    """
    results = {}
    for query in queries:
        results[query] = search(query, n, index)
    return results
