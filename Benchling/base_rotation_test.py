from base_rotation import count_unique_sequences, is_rotation, canonical


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
    # All rotations of "AAG": AAG, AGA, GAA -> smallest is AAG
    assert canonical("AAG") == "AAG"

def test_canonical_already_canonical():
    assert canonical("ACTG") == "ACTG"

def test_canonical_single_char():
    assert canonical("T") == "T"

def test_canonical_all_same():
    assert canonical("AAA") == "AAA"


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
