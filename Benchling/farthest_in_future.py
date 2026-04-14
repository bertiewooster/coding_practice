from collections import defaultdict
from collections.abc import Iterable
from collections import OrderedDict
import math

class FIFCache():
  def __init__(self, capacity: int, sequence: Iterable, data: dict[str, str]):
    self.capacity = capacity
    self.sequence = sequence
    self.data = data
    self.cache:OrderedDict = OrderedDict()
    # Create when_used dictionary of item: [indexA, indexB]
    self.when_used = defaultdict(list)
    # For index, item in sequence
      # append index to self.when_used item
    for index, item in enumerate(self.sequence):
      self.when_used[item].append(index)
    # Set sequence_index to -1 so can advance at start of access()
    self.sequence_index = -1
    self.hit_count = 0
    self.access_count = 0
    self.eviction_log_list = []

  def access(self, item):
    self.access_count += 1
    self.sequence_index += 1
    # Check if item is in cache
    if item in self.cache:
      # If yes, return "hit" and cache as is
      # Move item to end of dictionary to note is as most recently used
      self.cache.move_to_end(item)
      self.hit_count += 1
      return {"result": "Hit", "evicted": None, "cache": dict(self.cache)}

    # If cache isn't at capacity
    if len(self.cache) < self.capacity:
      # Add item to cache, return "miss" and cache
      self.cache[item] = self.data[item]
      return {"result": "Miss", "evicted": None, "cache": dict(self.cache)}
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
    del self.cache[key_to_evict]

    # Add new item
    self.cache[item] = self.data[item]

    return {"result": "Miss", "evicted": key_to_evict, "cache": dict(self.cache)}

  def hit_rate(self):
    if self.access_count == 0:
      return 0.0
    return self.hit_count / self.access_count

  def eviction_log(self):
    return list(self.eviction_log_list)

data = {"A": "geneA", "B": "geneB", "C": "geneC", "D": "geneD", "E": "geneE"}
access_sequence = ["A", "B", "C", "A", "D", "B", "E", "A"]

cache = FIFCache(capacity=3, sequence=access_sequence, data=data)

for index, item in enumerate(access_sequence):
    result = cache.access(item)
    print(index, item, result)  # HIT or MISS, plus current cache state
print(f"{cache.hit_rate()=}")

print("Eviction log:")
for evicted in cache.eviction_log():
  print(evicted)
