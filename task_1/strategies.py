from abc import ABC, abstractmethod

# Общий интерфейс для всех скидок
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

# Конкретные стратегии
class Save10Strategy(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        return total * 0.9

class Save20Strategy(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        return total * 0.8

class NoDiscountStrategy(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        return total

# Фабрика для удобного выбора стратегии
class DiscountFactory:
    @staticmethod
    def get_strategy(promo_code: str) -> DiscountStrategy:
        strategies = {
            'SAVE10': Save10Strategy(),
            'SAVE20': Save20Strategy()
        }
        return strategies.get(promo_code, NoDiscountStrategy())