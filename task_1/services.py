class UserValidator:
    def __init__(self, users_data: dict):
        self.users = users_data

    def get_valid_user(self, user_id: int) -> dict:
        if user_id not in self.users:
            raise Exception('User not found')
        if self.users[user_id]['banned']:
            raise Exception('User is banned')
        return self.users[user_id]

class InventoryManager:
    def __init__(self, inventory_data: dict):
        self.inventory = inventory_data

    def check_stock(self, items: dict) -> None:
        for item_id, qty in items.items():
            if item_id not in self.inventory:
                raise Exception(f'Item {item_id} not found')
            if self.inventory[item_id]['stock'] < qty:
                raise Exception(f'Insufficient stock for {item_id}')

    def calculate_base_price(self, items: dict) -> float:
        total = 0
        for item_id, qty in items.items():
            total += self.inventory[item_id]['price'] * qty
        return total

    def deduct_stock(self, items: dict) -> None:
        for item_id, qty in items.items():
            self.inventory[item_id]['stock'] -= qty