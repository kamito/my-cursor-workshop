import httpx
import streamlit as st

# --- 定数 ---
API_BASE_URL = "http://localhost:8000"

# --- UI描画 ---
st.title("商品管理UI")

# --- タブの作成 ---
tab1, tab2 = st.tabs(["商品登録", "商品検索"])


# --- 商品登録タブ ---
with tab1:
    st.header("商品を登録する")

    with st.form("create_product_form", clear_on_submit=True):
        name = st.text_input("商品名", placeholder="例: 新しいペン")
        price = st.number_input("価格（円）", min_value=1, step=1)
        submitted = st.form_submit_button("商品を登録する")

    if submitted:
        if not name:
            st.error("商品名を入力してください。")
        else:
            request_body = {"name": name, "price": price}
            try:
                response = httpx.post(f"{API_BASE_URL}/items", json=request_body, timeout=5)
                response.raise_for_status()  # HTTPエラーがあれば例外を発生させる

                created_product = response.json()
                st.success(
                    f"**登録完了！**\n\n"
                    f"- 商品「{created_product['name']}」を登録しました。\n"
                    f"- **商品ID:** `{created_product['id']}`"
                )
            except httpx.HTTPStatusError as e:
                # バリデーションエラーなど、APIが返すエラー
                data = e.response.json()
                st.error(f"登録に失敗しました: {data.get('detail', '不明なエラー')}")
            except httpx.RequestError:
                # ネットワークエラーなど
                st.error("APIサーバーに接続できません。サーバーを起動してください。")


# --- 商品検索タブ（プレースホルダー） ---
with tab2:
    st.header("商品を検索する")
    st.info("この機能はTask 7で実装します。")
