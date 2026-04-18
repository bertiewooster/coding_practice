from base_search import build_index, get_ngrams, search, search_many

SEQS = ["ACGTAC", "CGTACG", "TTACGT"]


def test_get_ngrams_basic():
    assert get_ngrams("ACGT", 2) == ["AC", "CG", "GT"]


def test_get_ngrams_full_string():
    assert get_ngrams("ACGT", 4) == ["ACGT"]


def test_get_ngrams_returns_empty_when_n_too_large():
    assert get_ngrams("AC", 3) == []


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
    for hardcoded_key, hardcoded_value in hardcoded_index.items():
        assert hardcoded_key in index
        assert hardcoded_value == index[hardcoded_key]


def test_build_index_contains_ngram():
    index = build_index(SEQS, 3)
    assert "CGT" in index
    assert "ACGTAC" in index["CGT"]


def test_build_index_does_not_contain_nonexistent():
    index = build_index(SEQS, 3)
    assert "ZZZ" not in index


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


def test_search_mutates_index():
    index = build_index(SEQS, 3)
    before = dict(index)
    search("CGTA", 3, index)
    assert dict(index) == before  # index must not be mutated


def test_search_many():
    index = build_index(SEQS, 3)
    out = search_many(["CGT", "CGTA"], 3, index)
    assert "CGT" in out
    assert "CGTA" in out
    assert "ACGTAC" in out["CGTA"]
