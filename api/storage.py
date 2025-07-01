from datetime import datetime

from .models import ProductModel


class InMemoryStorage:
    """インメモリストレージクラス"""

    def __init__(self) -> None:
        self._items: dict[int, ProductModel] = {}
        self._next_id: int = 1

    def create_product(self, name: str, price: float) -> ProductModel:
        """商品を新規作成する"""
        product = ProductModel(id=self._next_id, name=name, price=price, created_at=datetime.now())
        self._items[product.id] = product
        self._next_id += 1
        return product

    def get_product(self, product_id: int) -> ProductModel | None:
        """商品IDで商品を取得する"""
        return self._items.get(product_id)
