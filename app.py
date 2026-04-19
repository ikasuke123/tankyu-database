import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページ設定
st.set_page_config(page_title="探究DB", layout="wide")

st.title("🎓 探究情報データベース")

# URL設定
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit"

# 接続
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.radio("メニュー", ["データを見る", "新しく登録する"])

if menu == "データを見る":
    st.header("🔍 登録データ一覧")
    try:
        # 読み込み
        df = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("データがまだありません。")
    except Exception as e:
        st.error(f"読み込み失敗: {e}")

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
                    # 1. 既存データを読み込む
                    existing_data = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1")
                    
                    # 2. 新しい行を作成（ここでの名前がスプレッドシートの1行目になります）
                    new_entry = pd.DataFrame([{
                        "筆者名": author,
                        "探究タイトル": title,
                        "分野": category,
                        "作成年度": int(year),
                        "学校名": school
                    }])
                    
                    # 3. データを結合（既存が空なら新規のみ、あれば連結）
                    if existing_data is not None and not existing_data.empty:
                        # 既存データの列名を強制的に新データに合わせる（400エラー対策）
                        existing_data.columns = ["筆者名", "探究タイトル", "分野", "作成年度", "学校名"]
                        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    else:
                        updated_df = new_entry
                    
                    # 4. 書き込み実行
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=updated_df)
                    st.success("登録に成功しました！")
                    st.balloons()
                except Exception as e:
                    st.error(f"書き込み失敗: {e}")
