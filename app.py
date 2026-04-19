import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# URL設定（末尾を /edit から /export?format=csv に置換して通信します）
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit"
CSV_URL = SPREADSHEET_URL.replace("/edit", "/export?format=csv")

# 接続（書き込み用）
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.radio("メニュー", ["データを見る", "新しく登録する"])

if menu == "データを見る":
    st.header("🔍 登録データ一覧")
    try:
        # 【重要】ライブラリを使わず、直接CSVとして読み込む
        df = pd.read_csv(CSV_URL)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("データがまだありません。")
    except Exception as e:
        st.error(f"読み込み失敗: {e}")
        st.info("スプレッドシートが『共有：リンクを知っている全員（閲覧者以上）』になっているか確認してください。")

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
                    # 書き込み用のデータ作成
                    new_entry = pd.DataFrame([{
                        "筆者名": author,
                        "探究タイトル": title,
                        "分野": category,
                        "作成年度": int(year),
                        "学校名": school
                    }])
                    
                    # 既存データを読み込んで結合（ここでもCSV方式を使うと安定します）
                    existing_data = pd.read_csv(CSV_URL)
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    
                    # 書き込み実行（ここだけライブラリを使用）
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=updated_df)
                    st.success("登録に成功しました！")
                    st.balloons()
                except Exception as e:
                    st.error(f"書き込み失敗: {e}")
