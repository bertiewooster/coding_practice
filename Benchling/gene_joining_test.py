from gene_joining import find_longest_chains


def result_as_dict(results):
    return {gene: (start, end) for gene, start, end in results}


def test_single_segment_not_duplicated():
    segments = [("EGFR", 5, 99)]
    results = find_longest_chains(segments)
    assert len(results) == 1
    assert results[0] == ("EGFR", 5, 99)


def test_two_contiguous_segments_join():
    segments = [
        ("MYC", 1, 10),
        ("MYC", 11, 20),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["MYC"] == (1, 20)


def test_three_contiguous_segments_join():
    segments = [
        ("MYC", 1, 10),
        ("MYC", 11, 20),
        ("MYC", 21, 30),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["MYC"] == (1, 30)


def test_gap_does_not_join():
    segments = [
        ("KRAS", 0, 9),
        ("KRAS", 11, 20),
    ]
    r = result_as_dict(find_longest_chains(segments))
    start, end = r["KRAS"]
    assert end - start == 9


def test_gap_of_many_does_not_join():
    segments = [
        ("PTEN", 0, 49),
        ("PTEN", 100, 149),
    ]
    r = result_as_dict(find_longest_chains(segments))
    start, end = r["PTEN"]
    assert end - start == 49


def test_longest_chain_after_gap():
    segments = [
        ("ARID1A", 0, 10),
        ("ARID1A", 20, 30),
        ("ARID1A", 31, 40),
        ("ARID1A", 41, 50),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["ARID1A"] == (20, 50)


def test_longest_chain_by_span_not_insertion_order():
    segments = [
        ("RB1", 0, 4),
        ("RB1", 10, 19),
        ("RB1", 20, 29),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["RB1"] == (10, 29)


def test_longest_chain_span_beats_segment_count():
    segments = [
        ("TP53", 200, 202),
        ("TP53", 203, 205),
        ("TP53", 206, 208),
        ("TP53", 0, 49),
        ("TP53", 50, 99),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["TP53"] == (0, 99)


def test_basic_two_gene_example():
    segments = [
        ("BRCA1", 100, 200),
        ("BRCA1", 201, 300),
        ("BRCA1", 302, 400),
        ("TP53", 10, 50),
        ("TP53", 51, 90),
        ("TP53", 91, 130),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["BRCA1"] == (100, 300)
    assert r["TP53"] == (10, 130)


def test_input_in_reverse_order():
    segments = [
        ("PTEN", 201, 300),
        ("PTEN", 101, 200),
        ("PTEN", 1, 100),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["PTEN"] == (1, 300)


def test_multiple_genes_independent():
    segments = [
        ("GENE_A", 0, 10),
        ("GENE_B", 0, 10),
        ("GENE_A", 11, 20),
        ("GENE_B", 12, 20),
    ]
    r = result_as_dict(find_longest_chains(segments))
    assert r["GENE_A"] == (0, 20)
    assert r["GENE_B"] in [(0, 10), (12, 20)]
