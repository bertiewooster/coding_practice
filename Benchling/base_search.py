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

    # Explicit queries resolve wildcards,
    #   e.g. query = YGTA is resolved to explicit_queries = {CGTA, TGTA}
    explicit_queries = set()

    # Create a list of list where each sublist is the options for each position,
    #   e.g. [[C, T], [G], [T], [A]]
    items = [WILDCARDS.get(base, [base]) for base in query]

    # To create list of explicit queries, loop over combinations (products), 
    #   e.g. (C, G, T, A) and (T, G, T, A)
    for item in product(*items):
        # Join tuple into a string
        q = "".join(item)
        # Add this to the set of explicit queries
        explicit_queries.add(q)

    # Loop over explicit queries
    for explicit_query in explicit_queries:
        # Get the ngrams, e.g. explicit_query = CGTA, n = 3 
        #   has ngrams CGT, GTA
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
        # If this explicit query has any result (all ngrams matched)
        if result is not None:
            # Add this explicit query's result to the running set of results
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
