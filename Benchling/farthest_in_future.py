from collections import defaultdict
from collections.abc import Iterable
from collections import OrderedDict
import math

class FIFCache():
  def reset(self):
    self.cache:OrderedDict = OrderedDict()
    # Set sequence_index to -1 so can advance at start of access()
    self.sequence_index = -1
    self.hit_count = 0
    self.access_count = 0
    self.eviction_log_list = []
    self.bytes_used = 0

  def __init__(self, capacity: int, sequence: Iterable, data: dict[str, str], sizes: dict[str, int]):
    # Capacity in bytes, not number of items (keys) in cache
    self.capacity = capacity
    self.sequence = sequence
    self.data = data
    self.sizes = sizes
    # Create when_used dictionary of item: [indexA, indexB]
    self.when_used = defaultdict(list)
    # For index, item in sequence
      # append index to self.when_used item
    for index, item in enumerate(self.sequence):
      self.when_used[item].append(index)
    self.reset()

  def access(self, item):
    self.access_count += 1
    self.sequence_index += 1
    # Check if item is in cache
    if item in self.cache:
      # If yes, return "hit" and cache as is
      # Move item to end of dictionary to note is as most recently used
      self.cache.move_to_end(item)
      self.hit_count += 1
      return {"result": "Hit", "evicted": [], "cache": dict(self.cache)}

    # Will need to check if adding new item to cache will exceed cache capacity
    # Specifically, check if self.bytes_used + item size > self.capacity

    evicted_list = []
    # If capacity will be exceeded,

    keys_to_evict = []
    post_add_bytes_used = self.bytes_used + self.sizes[item]
    # While capacity will be exceeded
    # print(f"  {self.bytes_used=} {self.sizes[item]=} {post_add_bytes_used=}")
    while post_add_bytes_used > self.capacity:
      # Remove the farthest in future item from cache

      # If cache is at capacity
      # determine which item in cache is used farthest in the future
      # by creating a dictionary of item:next_use
      next_use = defaultdict(lambda:math.inf)
      # For each item in cache
      for cache_item in self.cache.keys():
        # get its next_use
        future_used = [position for position in self.when_used[cache_item] if position > self.sequence_index]
        next_used = next(iter(future_used), math.inf)
        next_use[cache_item] = next_used
      
      # Find which cache_item has the greatest next_used to evict it
      greatest_next_use = -math.inf
      greatest_next_use_keys = []
      for next_use_key, next_use_value in next_use.items():
        if next_use_value > greatest_next_use:
          greatest_next_use = next_use_value
          greatest_next_use_keys = [next_use_key]
        elif next_use_value == greatest_next_use:
          greatest_next_use_keys.append(next_use_key)

      # If there's just one greatest_next_use_key, evict it; default.
      key_to_evict = greatest_next_use_keys[0]
      # If there's more than one greatest_next_use_key, make decision based on LRU
      if len(greatest_next_use_keys) > 1:
        # Evict leftmost key in cache that's in greatest_next_use_keys
        for evict_candidate in self.cache.keys():
          if evict_candidate in greatest_next_use_keys:
            key_to_evict = evict_candidate
            break
      reason = "never_used_again" if greatest_next_use == math.inf else "farthest_next_use"
      self.eviction_log_list.append((self.sequence_index, key_to_evict, reason))
      keys_to_evict.append(key_to_evict)
      del self.cache[key_to_evict]

      # Update self.bytes_used
      self.bytes_used -= self.sizes[key_to_evict]

    # Add item to cache
    self.cache[item] = self.data[item]

    # Return "Miss", evicted_list, cache
    return {"result": "Miss", "evicted": keys_to_evict, "cache": dict(self.cache)}

  def hit_rate(self):
    if self.access_count == 0:
      return 0.0
    return self.hit_count / self.access_count

  def eviction_log(self):
    return list(self.eviction_log_list)




data = {
    "A": "geneA",
    "B": "geneB",
    "C": "geneC",
    "D": "geneD",
    "E": "geneE",
}

sizes = {
    "A": 40,
    "B": 35,
    "C": 20,
    "D": 25,
    "E": 40,
}
access_sequence = ["A", "B", "C", "A", "D", "B", "E", "A"]
# capacity = 3
capacity = 100

cache = FIFCache(capacity=capacity, sequence=access_sequence, data=data, sizes=sizes)

for index, item in enumerate(access_sequence):
    result = cache.access(item)
    print(index, item, result)  # HIT or MISS, plus current cache state
print(f"{cache.hit_rate()=}")

print("Eviction log:")
for evicted in cache.eviction_log():
  print(evicted)

cache.reset()

for index, item in enumerate(access_sequence):
    outcome = cache.access(item)
    result = outcome["result"]
    evicted = outcome["evicted"]
    result_cache = outcome["cache"]
    print(index, item, result, evicted, result_cache.keys())  # HIT or MISS, plus current cache state
print(f"{cache.hit_rate()=}")

print("Eviction log:")
for evicted in cache.eviction_log():
  print(evicted)
