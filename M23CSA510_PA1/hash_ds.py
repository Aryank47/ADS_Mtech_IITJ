from typing import Tuple


class HashTable:
    def __init__(
        self,
        initial_size: int = 10,
        load_factor_threshold: float = 0.7,
    ):
        self.size: int = initial_size
        self.load_factor_threshold: float = load_factor_threshold
        self.table: list[Tuple[int, str] | None] = [None] * initial_size
        self.num_elements: int = 0
        self.collision_count: int = 0

    def _hash_function(self, key: int):
        return hash(key) % self.size

    def _probe(self, hash_value, i) -> int:
        return (hash_value + i**2) % self.size

    def _resize(self, new_size: int):
        print(f"Hash table is full. Resizing...{new_size}")
        old_table = self.table
        self.size = new_size
        self.table = [None] * new_size
        self.num_elements = 0

        for item in old_table:
            if item is not None:
                key, value = item
                self.insert(key, value)

    def _check_and_resize(self):
        load_factor = self.num_elements / self.size
        if load_factor > self.load_factor_threshold:
            # Resize the hash table when the load factor exceeds the threshold.
            new_size = self.size * 2
            self._resize(new_size)

    def insert(self, key: int, value: str):
        self._check_and_resize()

        hash_value = self._hash_function(key)
        i = 0

        while i < self.size:
            index = self._probe(hash_value, i)
            if self.table[index] is None:
                self.table[index] = (key, value)
                self.num_elements += 1
                return
            self.collision_count += 1
            i += 1

    def search(self, key: int):
        hash_value = self._hash_function(key)
        i = 0

        while i < self.size:
            index = self._probe(hash_value, i)
            if self.table[index] is None:
                break
            stored_key, value = self.table[index]
            if key == stored_key:
                return value
            i += 1

        return None

    def delete(self, key):
        hash_value = self._hash_function(key)
        i = 0

        while i < self.size:
            index = self._probe(hash_value, i)
            if self.table[index] is None:
                # Key not found
                return

            stored_key, _ = self.table[index]
            if key == stored_key:
                self.table[index] = None
                return

            i += 1

        # Key not found after probing the entire table
        print(f"Key '{key}' not found.")
