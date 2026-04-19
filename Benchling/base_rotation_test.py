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
    assert count_unique_sequences(["AAG", "GAA", "CAA"]) == 2


def test_all_unique():
    assert count_unique_sequences(["ACTG", "TTTT", "CCCC"]) == 3


def test_all_same_rotation():
    assert count_unique_sequences(["AAG", "GAA", "AGA"]) == 1


def test_empty_input():
    assert count_unique_sequences([]) == 0


def test_single_gene():
    assert count_unique_sequences(["ACTG"]) == 1


def test_duplicates_not_rotations():
    # "AACT" and "ACTA" are rotations; "TTGG" is distinct
    assert count_unique_sequences(["AACT", "ACTA", "TTGG"]) == 2


def test_longer_sequences():
    g1 = "ACTGACTG"
    g2 = "ACTGACTG"[3:] + "ACTGACTG"[:3]  # rotation
    g3 = "TTTTTTTT"
    assert count_unique_sequences([g1, g2, g3]) == 2
