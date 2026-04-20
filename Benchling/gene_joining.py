from collections import defaultdict


def find_longest_chains(segments):
    """
    Given a list of (gene_name, start, end) tuples, find the longest
    contiguous chain of segments for each gene name.

    Two segments are contiguous if next.start == prev.end + 1.

    Returns a list of (gene_name, chain_start, chain_end), one per gene.
    """
    grouped = defaultdict(list)
    for gene, start, end in segments:
        grouped[gene].append((start, end))

    results = []

    for gene, segs in grouped.items():
        segs.sort(key=lambda x: x[0])

        chains = []
        chain_start, chain_end = segs[0]

        for i in range(1, len(segs)):
            start, end = segs[i]
            if start == chain_end + 1:
                chain_end = end
            else:
                chains.append((chain_start, chain_end))
                chain_start, chain_end = start, end

        chains.append((chain_start, chain_end))

        longest = max(chains, key=lambda x: x[1] - x[0])
        results.append((gene, longest[0], longest[1]))

    return results
