from infrastructure import DatabaseRepository, EmailNotificationService
from services import UserValidator, InventoryManager
from strategies import DiscountFactory

class OrderManager: # Оставляем имя для совместимости, но теперь это Фасад
    def __init__(self, db_conn, smtp_host, smtp_port, tax_rate, currency):
        self.tax_rate = tax_rate
        self.currency = currency
        self.orders = []
        
        # Общие данные (передаем по ссылке)
        self.users = {}
        self.inventory = {}
        
        # Инициализация выделенных классов
        self.db_repo = DatabaseRepository(db_conn)
        self.notifier = EmailNotificationService(smtp_host, smtp_port)
        self.user_validator = UserValidator(self.users)
        self.inventory_manager = InventoryManager(self.inventory)

    def create_order(self, user_id, items, promo_code=None):
        # 1. Валидация
        user = self.user_validator.get_valid_user(user_id)
        self.inventory_manager.check_stock(items)
        
        # 2. Расчет стоимости и скидок
        base_total = self.inventory_manager.calculate_base_price(items)
        discount_strategy = DiscountFactory.get_strategy(promo_code)
        
        total_after_discount = discount_strategy.apply_discount(base_total)
        final_total = total_after_discount * (1 + self.tax_rate)
        
        # 3. Обновление состояния
        self.inventory_manager.deduct_stock(items)
        
        # 4. Сохранение и уведомление
        order = {'id': len(self.orders)+1, 'user': user_id, 'items': items, 'total': final_total, 'status': 'new'}
        self.orders.append(order)
        
        self.db_repo.save_order(order)
        self.notifier.send_order_confirmation(user['email'], order['id'], final_total)
        
        return order