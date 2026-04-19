import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# スプレッドシートURL（末尾を /export?format=csv に変えるのが安定のコツです）
url = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/export?format=csv"

# 接続（最もシンプルな読み込み方法）
try:
    df = pd.read_csv(url)
    st.subheader("🔍 登録データ一覧")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"接続エラー: {e}")
    st.info("スプレッドシートが『リンクを知っている全員：編集者（または閲覧者）』になっているか再確認してください。")

# 新規登録機能
st.divider()
st.subheader("📝 データの登録")
with st.form("my_form"):
    author = st.text_input("筆者名")
    title = st.text_input("探究タイトル")
    category = st.selectbox("分野",  ["保育・教育", "食", "旅行・観光", "国際", "スポーツ・運動", "地理", "歴史", "自然・環境", "動物", "ICT・情報", "国際", "芸術", "文化", "ビジネス", "地域", "防災・復興", "科学・理科","工学", "文学", "介護", "看護・医療","その他"])
    year = st.number_input("年度", value=2026)
    school = st.text_input("学校名")
    
    submitted = st.form_submit_button("送信")
    
    if submitted:
        if author and title:
            # 書き込み用には GSheetsConnection を使用
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                existing_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit", worksheet="Sheet1")
                new_row = pd.DataFrame([{"筆者名": author, "探究タイトル": title, "分野": category, "作成年度": year, "学校名": school}])
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit", worksheet="Sheet1", data=updated_df)
                st.success("保存完了！ブラウザを更新して確認してください。")
                st.balloons()
            except Exception as e:
                st.error(f"書き込み失敗: {e}")
