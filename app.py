import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. ページ全体の初期設定
st.set_page_config(page_title="探究学習DB", layout="wide")

# 2. スプレッドシート情報の定義
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_GJVkAjsXGl7oojSVX31l49sJDkalMUPOnx8Xhxw_SQ/edit"

# 3. タイトル表示
st.title("🎓 探究情報データベース")
st.write("全国の探究学習を共有するプラットフォーム")

# 4. Googleスプレッドシートへの接続設定
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. サイドバーメニュー
menu = st.sidebar.radio("メニュー", ["データを見る・探す", "新しく登録する"])

# ---------------------------------------------------------
# A. データ表示ページ
# ---------------------------------------------------------
if menu == "データを見る・探す":
    st.header("🔍 登録データ一覧")
    
    try:
        # スプレッドシートを読み込む（最新の状態を取得するためキャッシュは短めに設定）
        df = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1")
        
        if df.empty:
            st.info("まだデータが登録されていません。最初の1件を登録してみましょう！")
        else:
            # 検索機能
            search_query = st.text_input("キーワード検索（筆者、タイトル、学校名など）")
            if search_query:
                # 検索にヒットする行だけ抽出
                df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
            
            # データテーブルの表示
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"データの読み込みに失敗しました。")
        st.info("【確認事項】スプレッドシートのタブ名が 'Sheet1' になっていますか？ 共有設定は '編集者' ですか？")

# ---------------------------------------------------------
# B. データ登録ページ
# ---------------------------------------------------------
elif menu == "新しく登録する":
    st.header("📝 探究情報の登録")
    st.write("以下の項目を入力して送信してください。")

    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            author = st.text_input("筆者名（必須）")
            school = st.text_input("学校名（必須）")
        with col2:
            # 指定されたカテゴリーを反映
            category = st.selectbox("分野", [
                "保育・教育", "食", "旅行・観光", "国際", "スポーツ・運動", 
                "地理", "歴史", "自然・環境", "動物", "ICT・情報", "芸術", 
                "文化", "ビジネス", "地域", "防災・復興", "科学・理科",
                "工学", "文学", "介護", "看護・医療", "その他"
            ])
            # 指定されたデフォルト年度（2026年）を反映
            year = st.number_input("作成年度", value=2026, min_value=2020, max_value=2030)
        
        title = st.text_input("探究タイトル（必須）")
        
        submitted = st.form_submit_button("データベースに登録する")
        
        if submitted:
            if not author or not title or not school:
                st.warning("「筆者名」「学校名」「タイトル」は必ず入力してください。")
            else:
                try:
                    # 最新のデータを取得
                    existing_data = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1")
                    
                    # 新しい行の作成
                    new_entry = pd.DataFrame([{
                        "筆者名": author,
                        "探究タイトル": title,
                        "分野": category,
                        "作成年度": int(year),
                        "学校名": school
                    }])
                    
                    # データを結合（既存データが空の場合も考慮）
                    if existing_data.empty:
                        updated_df = new_entry
                    else:
                        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    
                    # スプレッドシートを更新
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=updated_df)
                    
                    st.success("無事に登録されました！「データを見る」メニューから確認してください。")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"登録に失敗しました: {e}")
