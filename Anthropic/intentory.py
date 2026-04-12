import logging
from collections import defaultdict
from typing import List

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(name)s: %(message)s",
)

# Get a logger for this module
logger = logging.getLogger(__name__)

class InventorySystem:
    def __init__(self):
        self.inventory = defaultdict(lambda: defaultdict(int))
    
    def add_item(self, item: str, batch_id: str, quantity: int) -> bool:
        self.inventory[item][batch_id] += quantity
        return True

    def remove_item(self, item: str, quantity: int) -> bool:
        if item not in self.inventory:
            return False
        # pre_count = self.inventory[item]
        pre_count = self.get_quantity(item)
        if pre_count < quantity:
            return False
        # Remove from batches until have exhausted `quantity`
        for batch_id, batch_quantity in self.inventory[item].items():
            quantity_still_to_remove = quantity
            while quantity_still_to_remove > 0:
                # If this batch satisfies quantity still to remove, decrement batch_quantity by quantity_still_to_remove
                if batch_quantity >= quantity_still_to_remove:
                    self.inventory[item][batch_id] -= quantity_still_to_remove
                    quantity_still_to_remove -= batch_quantity
                # If this batch doesn't have enough, take all its qty
                else:
                    quantity_still_to_remove -= batch_quantity
                    self.inventory[item][batch_id] = 0
                # If batch has no qty left, delete it
                if self.inventory[item][batch_id] == 0:
                    del self.inventory[item][batch_id]
                    
            # If this depletes batch, remove it
        self.inventory[item] -= quantity
        post_count = self.inventory[item]
        if post_count <= 0:
            del self.inventory[item]
        return True
    
    def get_quantity(self, item: str) -> int:
        if item in self.inventory:
            total_quantity = 0
            for batch_id, quantity in self.inventory[item].items():
                total_quantity += quantity
            return total_quantity
        return 0
        
    def get_batches(self, item) -> List:
        # Return [("b1",5),("b2",3)]
        list_batches = []
        for batch_id, quantity in self.inventory[item].items():
            list_batches.append((batch_id, quantity))
        return list_batches

def test_level_2():
    inv = InventorySystem()

    inv.add_item("apple", "b1", 5)
    inv.add_item("apple", "b2", 3)

    logger.info(f"{inv.inventory=}")

    assert inv.get_quantity("apple") == 8
    
    logger.info(inv.get_batches("apple"))
    assert inv.get_batches("apple") == [("b1",5),("b2",3)]

    inv.remove_item("apple", 6)

    assert inv.get_batches("apple") == [("b2",2)]
    assert inv.get_quantity("apple") == 2

    assert inv.remove_item("apple", 5) == False

    print("Level 2 passed")
    
test_level_2()
    
# def test_level_1():
#     inv = InventorySystem()

#     assert inv.add_item("apple", 10) == True
#     assert inv.get_quantity("apple") == 10

#     assert inv.add_item("apple", 5) == True
#     assert inv.get_quantity("apple") == 15

#     assert inv.remove_item("apple", 8) == True
#     assert inv.get_quantity("apple") == 7

#     assert inv.remove_item("apple", 10) == False
#     assert inv.get_quantity("apple") == 7

#     assert inv.remove_item("apple", 7) == True
#     assert inv.get_quantity("apple") == 0

#     print("Level 1 passed")
    
# test_level_1()
