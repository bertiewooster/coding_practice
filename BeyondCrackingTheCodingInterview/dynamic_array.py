class DynamicArray:
    def __init__(self):
        self.capacity = 2
        self._size = 0
        self.fixed_array = [None] * self.capacity

    def __str__(self):
        return f"{self.fixed_array}"

    def get(self, i):
        if i < 0 or i >= self._size:
            raise IndexError("Index out of bounds")
        else:
            return self.fixed_array[i]

    def set(self, i, x):
        if i < 0 or i >= self._size:
            raise IndexError("Index out of bounds")
        else:
            self.fixed_array[i] = x

    def size(self):
        return self._size
    
    def append(self, x):
        self._size += 1
        if self._size > self.capacity:
            # Double the capacity
            old_capacity = self.capacity
            self.capacity *= 2
            fixed_array_new = [None] * self.capacity
            fixed_array_new[:old_capacity] = self.fixed_array
            self.fixed_array = fixed_array_new
        self.fixed_array[self._size - 1] = x

    def pop_back(self):
        last_element = self.fixed_array[self._size - 1]
        self._size -= 1
        return last_element

    def print_some_values(self):
        for index in [0, -10, 20]:
            try:
                dynamic_array.get(index)
            except IndexError:
                print(f"Index {index} out of range")

dynamic_array = DynamicArray()
print(dynamic_array)

dynamic_array.print_some_values()
print(f"{dynamic_array.size()=}")

dynamic_array.append(2)
dynamic_array.append(4)
dynamic_array.append(6)

dynamic_array.set(0, 0)
# dynamic_array.set(2, 6)
dynamic_array.print_some_values()
print(f"{dynamic_array.size()=}")

print(f"{dynamic_array.pop_back()=}")
print(f"{dynamic_array.size()=}")
