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
                    # ライブラリを介さず直接Googleのフォーム形式で送るか、
                    # あるいは一旦、読み込み表示ができることだけ確認しましょう。
                    st.warning("Googleのセキュリティ制限により、この方法での書き込みには『鍵ファイル』の設定が必要です。")
                    st.info("まずは『データを見る』が正常に動くか確認してください。")
                except Exception as e:
                    st.error(f"エラー: {e}")
