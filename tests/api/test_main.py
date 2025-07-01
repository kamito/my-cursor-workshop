import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.anyio
async def test_health_check_returns_200() -> None:
    """/healthエンドポイントはステータスコード200を返す"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_health_check_returns_ok_status() -> None:
    """/healthエンドポイントは{"status": "ok"}を返す"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_create_product_returns_201() -> None:
    """POST /items はステータスコード 201 を返す"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "テスト商品", "price": 1000})
    assert response.status_code == 201


@pytest.mark.anyio
async def test_create_product_returns_created_product() -> None:
    """POST /items は作成された商品情報を返す"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "テスト商品", "price": 1000})
    data = response.json()
    assert data["name"] == "テスト商品"
    assert data["price"] == 1000
    assert "id" in data
    assert "created_at" in data


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("name", "price"),
    [
        ("", 1000),  # 名前が空
        ("テスト商品", 0),  # 価格が0
        ("テスト商品", -1),  # 価格が負
    ],
)
async def test_create_product_with_invalid_data_returns_422(name: str, price: float) -> None:
    """不正なデータで商品を作成しようとすると422エラーを返す"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": name, "price": price})
    assert response.status_code == 422
