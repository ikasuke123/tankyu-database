import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# URLは必ず /edit で終わるもの
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/gviz/tq?tqx=out:csv"

# 接続
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.radio("メニュー", ["データを見る", "新しく登録する"])

if menu == "データを見る":
    st.header("🔍 登録データ一覧")
    try:
        # 閲覧は「公開CSV方式」で行う（これが一番エラーが出ません）
        csv_url = SPREADSHEET_URL.replace("/edit", "/export?format=csv")
        df = pd.read_csv(csv_url)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"読み込みエラー: {e}")

elif menu == "新しく登録する":
    st.header("📝 データの登録")
    with st.form("entry_form", clear_on_submit=True):
        author = st.text_input("筆者名")
        school = st.text_input("学校名")
        title = st.text_input("探究タイトル")
        category = st.selectbox("分野", [
            "保育・教育", "食", "旅行・観光", "国際", "スポーツ・運動", 
            "地理", "歴史", "自然・環境", "動物", "ICT・情報", "芸術", 
            "文化", "ビジネス", "地域", "防災・復興", "科学・理科",
            "工学", "文学", "介護", "看護・医療", "その他"
        ])
        year = st.number_input("年度", value=2026)
        
        submitted = st.form_submit_button("送信")
        
        if submitted:
            if author and title:
                try:
                    # 400エラー対策：スプレッドシートの1行目と「完全に」一致させるデータを作成
                    new_data = pd.DataFrame([{
                        "筆者名": author,
                        "探究タイトル": title,
                        "分野": category,
                        "作成年度": int(year),
                        "学校名": school
                    }])
                    
                    # 書き込み実行（worksheet名は必ず Sheet1）
                    conn.create(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=new_data)
                    st.success("成功しました！")
                    st.balloons()
                except Exception as e:
                    st.error(f"書き込み失敗: {e}")
                    st.info("スプレッドシートの1行目が『筆者名』『探究タイトル』『分野』『作成年度』『学校名』になっているか確認してください。")
