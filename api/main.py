from fastapi import FastAPI

from .models import CreateProductRequest, ProductModel
from .storage import InMemoryStorage

app = FastAPI(title="商品管理API")
storage = InMemoryStorage()


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """APIのヘルスチェック"""
    return {"status": "ok"}


@app.post("/items", response_model=ProductModel, status_code=201)
async def create_product(request: CreateProductRequest) -> ProductModel:
    """商品を新規作成する"""
    product = storage.create_product(name=request.name, price=request.price)
    return product
