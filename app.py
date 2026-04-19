import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# 新しいスプレッドシートURL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit"

# 接続
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.radio("メニュー", ["ホーム", "新規登録"])

if menu == "ホーム":
    st.header("🔍 登録データ一覧")
    try:
        # データの読み込み
        df = conn.read(spreadsheet=spreadsheet_url, worksheet="Sheet1")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("データがまだありません。")
    except Exception as e:
        st.error("データの読み込みに失敗しました。スプレッドシートの1行目の項目名とタブ名「Sheet1」を確認してください。")

elif menu == "新規登録":
    st.header("📝 データの登録")
    with st.form("my_form"):
        author = st.text_input("筆者名")
        school = st.text_input("学校名")
        title = st.text_input("探究タイトル")
        category = st.selectbox("分野", ["保育・教育", "食", "旅行・観光", "国際", "スポーツ・運動", "地理", "歴史", "自然・環境", "動物", "ICT・情報", "国際", "芸術", "文化", "ビジネス", "地域", "防災・復興", "科学・理科","工学", "文学", "介護", "看護・医療","その他"])
        year = st.number_input("年度", value=2026)
        
        submitted = st.form_submit_button("送信")
        
        if submitted:
            if author and title:
                # 既存データ読み込み
                existing_data = conn.read(spreadsheet=spreadsheet_url, worksheet="シート1")
                # 新規データ作成
                new_row = pd.DataFrame([{
                    "筆者名": author,
                    "探究タイトル": title,
                    "分野": category,
                    "作成年度": year,
                    "学校名": school
                }])
                # 結合
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                # 書き込み
                conn.update(spreadsheet=spreadsheet_url, worksheet="シート1", data=updated_df)
                st.success("スプレッドシートに保存しました！")
                st.balloons()
            else:
                st.error("必須項目を入力してください。")
