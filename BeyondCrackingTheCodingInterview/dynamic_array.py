class DynamicArray:
    def __init__(self):
        self.capacity = 10
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

    def print_some_values(self):
        for index in [1, -10, 20]:
            try:
                dynamic_array.get(index)
            except IndexError:
                print(f"Index {index} out of range")

dynamic_array = DynamicArray()
print(dynamic_array)

dynamic_array.print_some_values()
print(f"{dynamic_array.size()=}")

dynamic_array.set(0, 2)
dynamic_array.set(2, 6)
dynamic_array.print_some_values()
print(f"{dynamic_array.size()=}")
