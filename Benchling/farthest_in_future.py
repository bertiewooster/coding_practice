from collections import defaultdict
from collections.abc import Iterable
from typing import OrderedDict
import math

class FIFCache():
  def __init__(self, capacity: int, sequence: Iterable, data: dict[str, str]):
    self.capacity = capacity
    self.sequence = sequence
    self.data = data
    self.cache = OrderedDict()
    # Create when_used dictionary of item: [indexA, indexB]
    self.when_used = defaultdict(list)
    # For index, item in sequence
      # append index to self.when_used item
    for index, item in enumerate(self.sequence):
      self.when_used[item].append(index)
    print(f"{self.when_used}")
    self.sequence_index = 0

  def access(self, item):
    # Check if item is in cache
    if item in self.cache:
      # If yes, return "hit" and cache as is
      self.sequence_index += 1
      return "Hit", self.cache
    # If cache isn't at capacity
    if len(self.cache) < self.capacity:
      # Add item to cache, return "miss" and cache
      self.cache[item] = self.data[item]
      self.sequence_index += 1
      return "Miss", self.cache
    # If cache is at capacity
    # Determine which item in cache is used farthest in the future
    # For each item in cache
    next_use = defaultdict(lambda:math.inf)
    for cache_item in self.cache.keys():
      # get its next_use
      future_used = [position for position in self.when_used[cache_item] if position > self.sequence_index]
      try:
        next_used = future_used[0]
      except IndexError:
        next_used = math.inf
      next_use[cache_item] = next_used
    # print(f"{  next_use=}")
    
    # Find which cache_item has the greatest next_used to evict it
    greatest_next_use = -1
    greatest_next_use_key = None
    for next_use_key, next_use_value in next_use.items():
      if next_use_value > greatest_next_use:
        greatest_next_use = next_use_value
        greatest_next_use_key = next_use_key

    # Evict farthest in future key
    del self.cache[greatest_next_use_key]

    # Add new item
    self.cache[item] = data[item]

    self.sequence_index += 1
    return "Miss", greatest_next_use_key, self.cache

data = {"A": "geneA", "B": "geneB", "C": "geneC", "D": "geneD", "E": "geneE"}
access_sequence = ["A", "B", "C", "A", "D", "B", "E", "A"]

cache = FIFCache(capacity=3, sequence=access_sequence, data=data)

for index, item in enumerate(access_sequence):
    result = cache.access(item)
    print(index, item, result)  # HIT or MISS, plus current cache state
