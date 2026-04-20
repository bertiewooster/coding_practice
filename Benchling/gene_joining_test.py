import pytest
from gene_joining import find_longest_chains


def result_as_dict(results):
    """Convert result list to {gene_name: (start, end)} for easy assertion."""
    return {gene: (start, end) for gene, start, end in results}


def test_basic_two_gene_example():
    segments = [
        ("BRCA1", 100, 200),
        ("BRCA1", 201, 300),
        ("BRCA1", 302, 400),
        ("TP53",  10,  50),
        ("TP53",  51,  90),
        ("TP53",  91, 130),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["BRCA1"] == (100, 300)
    assert r["TP53"]  == (10, 130)

def test_basic_two_gene_example_disordered():
    segments = [
        ("BRCA1", 201, 300),
        ("BRCA1", 100, 200),
        ("BRCA1", 302, 400),
        ("TP53",  91, 130),
        ("TP53",  10,  50),
        ("TP53",  51,  90),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["BRCA1"] == (100, 300)
    assert r["TP53"]  == (10, 130)

def test_single_segment_gene():
    segments = [("EGFR", 0, 99)]
    r = result_as_dict(find_longest_chains(segments))
    assert r["EGFR"] == (0, 99)


def test_all_segments_contiguous():
    segments = [
        ("MYC", 1, 10),
        ("MYC", 11, 20),
        ("MYC", 21, 30),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["MYC"] == (1, 30)


def test_no_segments_contiguous():
    segments = [
        ("KRAS", 0,  9),
        ("KRAS", 11, 20),
        ("KRAS", 22, 31),
    ]
    r = result_as_dict(find_longest_chains(segments))
    gene_start, gene_end = r["KRAS"]
    assert gene_end - gene_start == 9


def test_input_given_in_reverse_order():
    segments = [
        ("PTEN", 201, 300),
        ("PTEN", 101, 200),
        ("PTEN", 1,   100),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["PTEN"] == (1, 300)


def test_longest_chain_not_first():
    """The longest chain does not start at the beginning of the segment list."""
    segments = [
        ("ARID1A", 0,  10),
        ("ARID1A", 20, 30),
        ("ARID1A", 31, 40),
        ("ARID1A", 41, 50),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["ARID1A"] == (20, 50)


def test_chain_length_is_span_not_count():
    """
    Two chains: one has 2 segments spanning 100 units,
    one has 3 segments spanning 9 units. The 2-segment chain should win.
    """
    segments = [
        ("RB1", 0,   49),
        ("RB1", 50,  99),
        ("RB1", 200, 202),
        ("RB1", 203, 205),
        ("RB1", 206, 208),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["RB1"] == (0, 99)


def test_multiple_genes_independent():
    segments = [
        ("GENE_A", 0, 10),
        ("GENE_B", 0, 10),
        ("GENE_A", 11, 20),
        ("GENE_B", 12, 20),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["GENE_A"] == (0, 20)
    assert r["GENE_B"] == (0, 10) or r["GENE_B"] == (12, 20)


def test_single_gene_two_equal_chains():
    """When two chains tie, either is acceptable."""
    segments = [
        ("VHL", 0,  9),
        ("VHL", 10, 19),
        ("VHL", 30, 39),
        ("VHL", 40, 49),
    ]
    r = result_as_dict(find_longest_chains(segments))
    gene_start, gene_end = r["VHL"]
    assert (gene_start, gene_end) in [(0, 19), (30, 49)]


def test_zero_based_indexing():
    """Chain starting at index 0 should not be skipped or mishandled."""
    segments = [
        ("FOXP1", 0, 0),
        ("FOXP1", 1, 1),
        ("FOXP1", 2, 2),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["FOXP1"] == (0, 2)


def test_large_indices():
    segments = [
        ("DNMT3A", 999_990, 999_995),
        ("DNMT3A", 999_996, 1_000_000),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["DNMT3A"] == (999_990, 1_000_000)