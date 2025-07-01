import httpx
import streamlit as st
from pydantic import BaseModel, Field

# --- 定数 ---
API_BASE_URL = "http://localhost:8000"


# --- Pydanticモデル ---
class ProductCreate(BaseModel):
    """商品作成APIリクエスト用のデータモデル"""

    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")


# --- APIクライアント ---
def handle_api_error(e: httpx.HTTPError, context: str) -> None:
    """APIエラーを処理し、Streamlitにメッセージを表示する"""
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            st.warning(f"⚠️ {context} は見つかりませんでした。")
        else:
            data = e.response.json()
            st.error(f"処理に失敗しました: {data.get('detail', '不明なエラー')}")
    elif isinstance(e, httpx.RequestError):
        st.error("APIサーバーに接続できません。サーバーを起動してください。")


def register_product(product: ProductCreate) -> None:
    """商品をAPIに登録する"""
    try:
        response = httpx.post(f"{API_BASE_URL}/items", json=product.model_dump(), timeout=5)
        response.raise_for_status()
        st.success(f"商品 `{product.name}` を登録しました。")
        st.json(response.json())
    except httpx.HTTPError as e:
        handle_api_error(e, f"商品 {product.name}")


def search_product(product_id: int) -> None:
    """商品をIDでAPIから検索する"""
    try:
        response = httpx.get(f"{API_BASE_URL}/items/{product_id}", timeout=5)
        response.raise_for_status()
        product = response.json()
        st.success(f"商品ID `{product['id']}` の情報が見つかりました。")
        st.json(product)
    except httpx.HTTPError as e:
        handle_api_error(e, f"商品ID {product_id}")


# --- UIコンポーネント ---
def product_registration_tab() -> None:
    """商品登録タブのUI"""
    st.header("商品を登録する")
    with st.form("product_registration_form", clear_on_submit=True):
        name = st.text_input("商品名", key="product_name")
        price = st.number_input("価格（円）", min_value=0.0, step=100.0, key="product_price")
        submitted = st.form_submit_button("商品を登録する")

        if submitted:
            try:
                product_data = ProductCreate(name=name, price=price)
                register_product(product_data)
            except ValueError as e:
                st.error(f"入力値が無効です: {e}")


def product_search_tab() -> None:
    """商品検索タブのUI"""
    st.header("商品を検索する")
    product_id_input = st.number_input("商品ID", min_value=1, step=1, key="search_product_id")
    if st.button("商品を検索する"):
        search_product(int(product_id_input))


# --- メインアプリケーション ---
def main() -> None:
    """Streamlitアプリケーションのメイン関数"""
    st.title("商品管理アプリ")

    tab1, tab2 = st.tabs(["商品登録", "商品検索"])

    with tab1:
        product_registration_tab()

    with tab2:
        product_search_tab()


if __name__ == "__main__":
    main()
