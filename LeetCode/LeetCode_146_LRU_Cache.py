from collections import deque

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = dict()
        self.lru = deque()
        pass

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.lru.remove(key)
        self.lru.append(key)
        return self.cache[key]
        

    def put(self, key: int, value: int) -> None:
        # print(f"Running put {key=} {value=}; {self.cache=} {self.lru=}")
        if (key not in self.cache) and (len(self.cache) == self.capacity):
            key_evict = self.lru.popleft()
            # print(f"  Evict {key_evict=} from {self.cache=} and {self.lru=}")
            del self.cache[key_evict]
        if key in self.cache:
            self.lru.remove(key)
        self.lru.append(key)
        self.cache[key] = value
        return "null"

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)