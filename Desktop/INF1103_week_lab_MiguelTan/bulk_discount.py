from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and discount amount cannot be negative.")
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total
