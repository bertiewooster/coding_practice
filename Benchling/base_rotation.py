from collections import defaultdict


def is_rotation(s1, s2):
    """Return True if s1 is a rotation of s2. Examples:
    "AAG", "GAA" -> True because moving A from front to back of s1 yields s2
    "AAG", "CTT" -> False because s1 cannot be rotated to form s2
    "AAG", "AAGG" -> False because sequences are different lengths
    """
    if len(s1) != len(s2):
        return False
    doubled = s1 + s1
    return s2 in doubled


def canonical(gene):
    """Return the lexicographically smallest rotation of gene. Examples:
    "GAA" -> "AAG"
    "AAG" -> "AAG"
    """
    best = gene
    for i in range(1, len(gene)):
        rotation = gene[i:] + gene[:i]
        if rotation < best:
            best = rotation
    return best


def count_unique_sequences(genes):
    """
    Given a list of gene strings, return the number of unique sequences,
    where two sequences are considered the same if one is a rotation of the other.
    Examples:
    ["AAG", "GAA", "CAA"] -> 2 because AAG and GAA are rotations of each other
    ["ACTG", "TTTT", "CCCC"]) -> 3 because no sequence is a rotation of another
    """
    if not genes:
        return 0, []

    # Deduplicate while preserving order
    genes_dedup = list(dict.fromkeys(genes))

    # Initialize canonical:inputs default(list) dictionary
    canonical_inputs = defaultdict(list)
    for gene in genes_dedup:
        key = canonical(gene)
        # Add input_canonical canonical:gene
        canonical_inputs[key].append(gene)

    # Return groups: A list of lists, where each inner list contains all the input strings that belong to the same rotation equivalence class
    # e.g. ["AAG", "GAA", "AGA", "CAA", "AAC"] ->
    # [["AAG", "GAA", "AGA"], ["CAA", "AAC"]]

    # Initialize groups as empty list
    groups = []
    # Iterate through canonical:inputs dictionary items
    for canonical_gene, inputs in canonical_inputs.items():
        # If len(inputs) > 1
        if len(inputs) > 1:
            # Append inputs (as list) to groups
            groups.append(inputs)

    return len(canonical_inputs), groups
