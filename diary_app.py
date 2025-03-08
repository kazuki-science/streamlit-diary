import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "あなたのスプレッドシートIDをここに入力"

# 🔹 環境変数から Google Cloud の認証情報を取得
try:
    creds_dict = dict(st.secrets["GCP_SERVICE_ACCOUNT"])  # ✅ dict() でコピー
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")  # 🔹 改行を修正
    creds = Credentials.from_service_account_info(creds_dict)
except Exception as e:
    st.error(f"❌ 認証情報の取得に失敗しました: {e}")
    st.stop()

# 🔹 Google Sheets API に接続
try:
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.sheet1  # 最初のシートを選択
except Exception as e:
    st.error(f"❌ Google Sheets への接続に失敗しました: {e}")
    st.stop()

# Streamlit UI
st.title("日記入力フォーム")

# 入力フォーム
date = st.date_input("日付を選択")
satisfaction = st.slider("満足度 (1〜10)", 1, 10, 5)
weight = st.number_input("体重 (kg)", min_value=30.0, max_value=150.0, step=0.1)
note = st.text_area("自由記述")

# 保存ボタン
if st.button("保存"):
    new_data = [str(date), satisfaction, weight, note]
    try:
        worksheet.append_row(new_data)  # 🔹 Google Sheets にデータを追加
        st.success("✅ 日記を Google Sheets に保存しました！")
    except Exception as e:
        st.error(f"❌ データの保存に失敗しました: {e}")

# Google Sheets からデータを読み込む
try:
    data = worksheet.get_all_values()
except Exception as e:
    st.error(f"❌ スプレッドシートのデータ取得に失敗しました: {e}")
    data = []

# 🔹 **データが空の場合の処理**
if data:
    df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=data[0])
else:
    df = pd.DataFrame(columns=["日付", "満足度", "体重", "自由記述"])

# 過去のデータを表示
st.write("📜 過去の日記")
st.dataframe(df)

# CSV ダウンロード機能
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 CSV をダウンロード",
    data=csv,
    file_name="diary.csv",
    mime="text/csv",
)


