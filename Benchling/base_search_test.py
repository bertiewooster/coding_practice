import copy

from base_search import build_index, get_ngrams, search, search_many

SEQS = ["ACGTAC", "CGTACG", "TTACGT"]

# --- get_ngrams ---


def test_get_ngrams_basic():
    assert get_ngrams("ACGT", 2) == {"AC", "CG", "GT"}


def test_get_ngrams_full_string():
    # when n == len(s), exactly one n-gram: the whole string
    assert get_ngrams("ACGT", 4) == {"ACGT"}


def test_get_ngrams_returns_empty_when_n_too_large():
    assert get_ngrams("AC", 3) == set()


def test_get_ngrams_count():
    # for a string of length L, expect L - n + 1 n-grams
    s, n = "ACGTAC", 3
    assert len(get_ngrams(s, n)) == len(s) - n + 1


# --- build_index ---


def test_build_index_contains_ngram():
    index = build_index(SEQS, 3)
    assert "CGT" in index
    assert "ACGTAC" in index["CGT"]


def test_build_index_all_ngrams_present():
    # every n-gram produced by get_ngrams should appear as a key
    index = build_index(SEQS, 3)
    for seq in SEQS:
        for ng in get_ngrams(seq, 3):
            assert ng in index, f"{ng} missing from index"


def test_build_index_does_not_contain_nonexistent():
    index = build_index(SEQS, 3)
    assert "ZZZ" not in index


# --- search ---


def test_search_single_ngram():
    index = build_index(SEQS, 3)
    result = search("CGT", 3, index)
    assert "ACGTAC" in result
    assert "CGTACG" in result


def test_search_multi_ngram_intersection():
    index = build_index(SEQS, 3)
    result = search("CGTA", 3, index)
    assert result == {"ACGTAC", "CGTACG"}
    assert "TTACGT" not in result


def test_search_no_match():
    index = build_index(SEQS, 3)
    result = search("ZZZ", 3, index)
    assert result == set()


def test_search_returns_a_copy():
    # search() must not return a live reference into the index.
    # Mutating the result must not affect future searches.
    index = build_index(SEQS, 3)
    index_original = copy.deepcopy(index)
    result = search("CGT", 3, index)
    result.clear()  # mutate the returned set
    assert index == index_original  # index must be intact


def test_search_many():
    index = build_index(SEQS, 3)
    out = search_many(["CGT", "CGTA"], 3, index)
    assert "CGT" in out
    assert "CGTA" in out
    assert "ACGTAC" in out["CGTA"]


# I added
def test_build_index():
    index = build_index(SEQS, 3)
    hardcoded_index = {
        "ACG": {"ACGTAC", "CGTACG", "TTACGT"},
        "CGT": {"ACGTAC", "CGTACG", "TTACGT"},
        "GTA": {"ACGTAC", "CGTACG"},
        "TAC": {"ACGTAC", "CGTACG", "TTACGT"},
        "TTA": {"TTACGT"},
    }
    assert index == hardcoded_index


def test_search_single_ngram_wildcard_not_expand_results():
    index = build_index(SEQS, 3)
    result = search("YTA", 3, index)  # CTA, TTA
    assert "TTACGT" in result
    assert "ACGTAC" not in result
    assert "CGTACG" not in result


def test_search_single_ngram_wildcard_expand_results():
    index = build_index(SEQS, 3)
    result = search("NTA", 3, index)
    assert "ACGTAC" in result
    assert "CGTACG" in result
    assert "TTACGT" in result


def test_search_multi_ngram_intersection_wildcard():
    index = build_index(SEQS, 3)
    result = search("YGTA", 3, index)
    assert result == {"ACGTAC", "CGTACG"}
    assert "TTACGT" not in result
