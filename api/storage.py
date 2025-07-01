from .models import ProductModel


class InMemoryStorage:
    """インメモリストレージクラス"""

    def __init__(self) -> None:
        self._items: dict[int, ProductModel] = {}
        self._next_id: int = 1

    def create_product(self, product: ProductModel) -> ProductModel:
        """商品を新規作成する（ダミー）"""
        # Task 4で実装
        raise NotImplementedError

    def get_product(self, product_id: int) -> ProductModel | None:
        """商品IDで商品を取得する（ダミー）"""
        # Task 5で実装
        raise NotImplementedError
