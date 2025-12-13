# dsa/hashing.py

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]  # chaining with lists

    def _hash(self, key: str) -> int:
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def search(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None
