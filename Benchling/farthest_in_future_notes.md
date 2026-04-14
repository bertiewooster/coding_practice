1. What data structures did you choose for the eviction lookup, and why? What are the tradeoffs?
    - next_use is a dictionary
        - I used a dictionary to store the next use of each item currently in the cache, because it's O(1) for the eviction lookup. Building it is O(k) where k is the cache size; so is finding its maximum across all keys. So each eviction decision is O(k).
        - I used a dictionary to map each cached item to its next use index, which gives O(1) lookup per item. Finding the eviction candidate requires a full O(k) scan of the cache, where k is the number of items currently cached. Since k is bounded by capacity this is acceptable. A max-heap could reduce that scan to O(log k) per eviction, but it adds complexity and since cache sizes are typically small the tradeoff isn't worth it here.
    - when_used is defaultdict(list)
        - It's preprocessed upfront. It costs O(n) space and O(n) to build, but makes the per-eviction "what's the next use?" lookup O(1) amortized via the pointer approach, or O(k) via the list comprehension filter you used. Both are defensible — the list comprehension is simpler to reason about.

1. This algorithm requires knowing the future. How would you adapt it if the sequence were only partially known (streamed in chunks)?
    - If the sequence were streamed in chunks, I would use what's been streamed so far with the algorithm as implemented. That risks excluding something that's coming up soon but we didn't know about in time.
    - If we can get information about the start of the next sequence as we approach the end of the previous sequence, I'd use prefetching to add to the future sequence. 
    - I might also weight least-recently-used more heavily, for example rather than evicting solely based on farthest-in-future (other than for tiebreakers) I might create a score that takes into account both measures. The longer the lookahead window, the more I'd weight the farthest-in-future factor.
    - Also, with some domain knowledge, I might also use for example machine learning to predict the future sequence.

1. How would you unit-test the eviction logic? What edge cases matter?
    - I would create unit tests for various scenarios, for example in the bytes-based cache scenarios where multiple items need to be evicted to make room for the incoming item. It'd structure them so each test handles one edge case.
    - Edge cases include
        - bytes-size an item being larger than the cache capacity
        - where the size of an incoming item exactly fills the cache capacity
        - where multiple keys to be evicted are never used again, so we use the LRU as a tiebreaker
        - a single-element cache so we're always evicting unless an item repeats
        - check that reset and replaying produces the same result as the original run
        - an empty sequence
        - missing data or sizes

1. How does this compare to LRU and LFU? When would each be preferable in a bioinformatics context?

    - LRU: LRU makes sense when recent access is a good predictor of near-future access — for example in interactive workflows where a biologist is actively exploring a region of the genome and keeps returning to nearby sequences. It has no preprocessing requirement and works well when the access pattern isn't known in advance.
    - LFU: Reference sequences like common chromosomes or housekeeping genes get accessed constantly across many different experiments. LFU would naturally keep those resident since their frequency accumulates over time, even if they weren't accessed recently.
    - FIFO (first in first out) is also something to consider: While it rarely performs well in real use cases, it's easy to reason about.

1.  If you had to persist the cache state to disk between pipeline runs, what would you change?

    - Compression: I'd use something like `gzip` because it's a standard and has Python support.
    - I'd use JSON format because it's human-readable, language-agnostic (another pipeline in R or Java could read it), and has mature serialization libraries. There might be slight changes needed, for example JSON doesn't handle `math.inf` so I'd replace it with either `null` or a large sentinel value.
    - What to persist: `self.cache` and `self.bytes_used`. But `self.when_used` can be reconstructed from sequence at startup — no need to persist it. `sequence_index` matters if you want to resume mid-sequence.
    - I'd write a temp file at each step so that if the pipeline crashes, I don't lose any work.
    - Cache invalidation — if `data` or `sizes` changes between runs, the persisted cache could be stale.
