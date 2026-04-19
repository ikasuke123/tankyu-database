import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# スプレッドシートURL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit"

# 接続設定
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.radio("メニュー", ["データを見る・探す", "新しく登録する"])

if menu == "データを見る・探す":
    st.header("🔍 登録データ一覧")
    try:
        # 読み込みから ttl 設定を削除（最もシンプルな形に戻す）
        csv_url = SPREADSHEET_URL.replace("/edit", "/export?format=csv")
        df = pd.read_csv(csv_url)
        
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("データが空か、読み込めませんでした。1件登録してみてください。")
            
    except Exception as e:
        # 詳細なエラー内容を表示させる（原因特定のため）
        st.error(f"読み込み失敗の理由: {e}")

elif menu == "新しく登録する":
    st.header("📝 探究情報の登録")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            author = st.text_input("筆者名（必須）")
            school = st.text_input("学校名（必須）")
        with col2:
            # 指定のカテゴリー
            category = st.selectbox("分野", [
                "保育・教育", "食", "旅行・観光", "国際", "スポーツ・運動", 
                "地理", "歴史", "自然・環境", "動物", "ICT・情報", "芸術", 
                "文化", "ビジネス", "地域", "防災・復興", "科学・理科",
                "工学", "文学", "介護", "看護・医療", "その他"
            ])
            year = st.number_input("年度", value=2026)
        
        title = st.text_input("探究タイトル（必須）")
        submitted = st.form_submit_button("データベースに登録する")
        
        if submitted:
            if author and title and school:
                try:
                    # 登録時も ttl なしで読み込み
                    existing_data = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1")
                    new_entry = pd.DataFrame([{
                        "筆者名": author, "探究タイトル": title, "分野": category, "作成年度": int(year), "学校名": school
                    }])
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=updated_df)
                    st.success("登録完了！")
                    st.balloons()
                except Exception as e:
                    st.error(f"書き込み失敗: {e}")
