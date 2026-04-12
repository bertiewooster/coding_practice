from collections import deque

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = dict()
        self.lru:deque = deque()
        pass

    def get(self, key: int) -> int:
        print(f"Running get {key=}; {self.cache=} {self.lru=}")
        if key not in self.cache:
            return -1
        # Remove key from lru dq
        self.lru.remove(key)
        self.lru.append(key)
        return self.cache[key]
        

    def put(self, key: int, value: int) -> None:
        print(f"Running put {key=} {value=}; {self.cache=} {self.lru=}")
        if key in self.cache:
            pass
        else:
            if len(self.lru) == self.capacity:
                key_evict = self.lru.popleft()
                del self.cache[key_evict]
        # If key already exists in lru, remove it
        try:
            self.lru.remove(key)
        except ValueError:
            pass

        self.lru.append(key)
        self.cache[key] = value
        print(f"  After: {self.cache=} {self.lru=}")
        return "null"

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)