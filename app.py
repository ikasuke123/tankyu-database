import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページの設定
st.set_page_config(page_title="探究DBポータル", layout="wide")

st.title("🎓 探究情報データベース")
st.write("全国の生徒がつながる探究学習のプラットフォーム")

# スプレッドシート接続（URLは後で設定ファイルに書くこともできますが、まずは直書き）
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1d9JMHPDDbXdfF45-C-QCbrN6cqSJhZyAAlKahma7NVE/edit"
conn = st.connection("gsheets", type=GSheetsConnection)

# サイドバーメニュー
menu = st.sidebar.radio("メニュー", ["ホーム・検索", "新規登録"])

if menu == "ホーム・検索":
    st.header("🔍 探究論文を検索する")
    
    # データの読み込み
    try:
        df = conn.read(spreadsheet=spreadsheet_url, worksheet="シート1")
        
        # 簡易検索機能
        search_query = st.text_input("キーワード検索（タイトルや筆者名）")
        if search_query:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
        
        # フィルター表示
        col1, col2 = st.columns(2)
        with col1:
            selected_cat = st.multiselect("分野で絞り込み", options=df["分野"].unique())
        with col2:
            selected_school = st.multiselect("学校で絞り込み", options=df["学校名"].unique())

        if selected_cat:
            df = df[df["分野"].isin(selected_cat)]
        if selected_school:
            df = df[df["学校名"].isin(selected_school)]

        st.dataframe(df, use_container_width=True)
        
        # 統計グラフ
        st.subheader("📊 分野別レポート")
        st.bar_chart(df["分野"].value_counts())

    except Exception as e:
        st.error(f"データの読み込みに失敗しました。シート名が「シート1」になっているか確認してください。")

elif menu == "新規登録":
    st.header("📝 あなたの探究を登録する")
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            author = st.text_input("筆者名")
            school = st.text_input("学校名")
        with col2:
            category = st.selectbox("分野", ["人文", "情報", "国際", "地域", "歴史", "自然科学", "その他"])
            year = st.number_input("作成年度", value=2024)
        
        title = st.text_input("探究タイトル")
        
        submitted = st.form_submit_button("データベースに送信")
        
        if submitted:
            if author and title and school:
                # 最新データの取得
                existing_data = conn.read(spreadsheet=spreadsheet_url, worksheet="シート1")
                # 新データ追加
                new_row = pd.DataFrame([{
                    "筆者名": author,
                    "探究タイトル": title,
                    "分野": category,
                    "作成年度": year,
                    "学校名": school
                }])
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                # 書き込み
                conn.update(spreadsheet=spreadsheet_url, worksheet="シート1", data=updated_df)
                st.success("登録に成功しました！反映には数十秒かかる場合があります。")
                st.balloons()
            else:
                st.warning("必須項目（名前・学校・タイトル）を入力してください。")