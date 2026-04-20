from base_rotation import canonical, count_unique_sequences, is_rotation

# --- is_rotation ---


def test_rotation_basic():
    assert is_rotation("AAG", "GAA")


def test_rotation_same_string():
    assert is_rotation("ACTG", "ACTG")


def test_rotation_different_length():
    assert not is_rotation("AAG", "AAGG")


def test_rotation_not_a_rotation():
    assert is_rotation("AAG", "AGA")  # AGA is a valid rotation of AAG


def test_rotation_single_char():
    assert is_rotation("A", "A")


def test_rotation_completely_different():
    assert not is_rotation("AAG", "CTT")


# --- canonical ---


def test_canonical_basic():
    # rotations: AAG, AGA, GAA -> smallest is AAG
    assert canonical("AAG") == "AAG"


def test_canonical_rotation_is_smaller():
    # rotations: GAA, AAG, AGA -> smallest is AAG
    assert canonical("GAA") == "AAG"


def test_canonical_another_rotation_is_smaller():
    # rotations: AGA, GAA, AAG -> smallest is AAG
    assert canonical("AGA") == "AAG"


def test_canonical_already_canonical():
    # rotations: ACTG, CTGA, TGAC, GACT -> smallest is ACTG
    assert canonical("ACTG") == "ACTG"


def test_canonical_not_already_canonical():
    # rotations: TGAC, GACT, ACTG, CTGA -> smallest is ACTG
    assert canonical("TGAC") == "ACTG"


def test_canonical_single_char():
    assert canonical("T") == "T"


def test_canonical_all_same():
    # all rotations are identical
    assert canonical("AAA") == "AAA"


def test_canonical_two_chars():
    # rotations: TA, AT -> smallest is AT
    assert canonical("TA") == "AT"


def test_canonical_consistent_across_rotations():
    # all rotations of the same string must return the same canonical form
    gene = "GCTA"
    rotations = [gene[i:] + gene[:i] for i in range(len(gene))]
    assert len(set(canonical(r) for r in rotations)) == 1


# --- count_unique_sequences ---


def test_example_from_prompt():
    # AAG, GAA are rotations of each other; CAA is distinct
    length, groups = count_unique_sequences(["AAG", "GAA", "CAA"])
    assert length == 2


def test_all_unique():
    length, groups = count_unique_sequences(["ACTG", "TTTT", "CCCC"])
    assert length == 3


def test_all_same_rotation():
    length, groups = count_unique_sequences(["AAG", "GAA", "AGA"])
    assert length == 1
    assert groups == [["AAG", "GAA", "AGA"]]


def test_empty_input():
    length, groups = count_unique_sequences([])
    assert length == 0
    assert groups == []


def test_single_gene():
    length, groups = count_unique_sequences(["ACTG"])
    assert length == 1
    assert groups == []


def test_duplicates_not_rotations():
    # "AACT" and "ACTA" are rotations; "TTGG" is distinct
    length, groups = count_unique_sequences(["AACT", "ACTA", "TTGG"])
    assert length == 2


def test_longer_sequences():
    g1 = "ACTGACTG"
    g2 = "ACTGACTG"[3:] + "ACTGACTG"[:3]  # rotation
    g3 = "TTTTTTTT"
    length, groups = count_unique_sequences([g1, g2, g3])
    assert length == 2


def test_groups_in_order_already():
    length, groups = count_unique_sequences(["AAG", "GAA", "AGA", "CAA", "AAC"])
    assert length == 2
    assert groups == [["AAG", "GAA", "AGA"], ["CAA", "AAC"]]


def test_groups_not_in_order_already():
    length, groups = count_unique_sequences(["CAA", "AAG", "GAA", "AGA", "AAC"])
    assert length == 2
    assert groups == [["CAA", "AAC"], ["AAG", "GAA", "AGA"]]


def test_all_unique_no_siblings():
    # no rotational relationships at all, groups should be empty
    length, groups = count_unique_sequences(["ACTG", "TTTT", "CCCC"])
    assert length == 3
    assert groups == []


def test_all_in_one_group():
    length, groups = count_unique_sequences(["AAG", "GAA", "AGA"])
    assert length == 1
    assert groups == [["AAG", "GAA", "AGA"]]


def test_exact_duplicates_not_count_as_rotation_siblings():
    # "AAG" and "AAG" are trivially rotations of each other
    length, groups = count_unique_sequences(["AAG", "AAG"])
    assert length == 1
    assert groups == []


def test_exact_duplicates_not_count_as_rotation_siblings_plus_rotation():
    # "AAG" and "AAG" are trivially rotations of each other
    length, groups = count_unique_sequences(["AAG", "AAG", "GAA"])
    assert length == 1
    assert groups == [["AAG", "GAA"]]


def test_exact_duplicates_count_as_rotation_siblings_plus_others():
    # "AAG" and "AAG" are trivially rotations of each other
    length, groups = count_unique_sequences(["AAG", "AAG", "GAA", "CAT", "ATC"])
    assert length == 2
    assert groups == [["AAG", "GAA"], ["CAT", "ATC"]]
