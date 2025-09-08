class DynamicArray:
    def __init__(self):
        self.capacity = 10
        self.size = 0
        self.fixed_array = [None] * self.capacity

    def __str__(self):
        return f"{self.fixed_array}"

dynamic_array = DynamicArray()
print(dynamic_array)
