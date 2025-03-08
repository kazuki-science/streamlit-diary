import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "1PH9nW0Eb46_OF_lEDkmhCYeq7Et2xoSpGKz5lpkjPB4"
JSON_FILE = "/Users/kazukiichikawa/Desktop/diary/orbital-wording-453107-c5-123733762aee.json"

# Google Sheets API の認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(JSON_FILE, scopes=scope)
client = gspread.authorize(creds)

# スプレッドシートを開く
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1  # 最初のシートを選択

# Streamlit UI
st.title("日記入力フォーム")

# 入力フォーム
date = st.date_input("日付を選択")
satisfaction = st.slider("1日の満足度 (1〜5)", 1, 5, 3)
weight = st.number_input("体重 (kg)", min_value=30.0, max_value=150.0, step=0.1)
note = st.text_area("自由記述")

# 保存ボタン
if st.button("保存"):
    new_data = [str(date), satisfaction, weight, note]
    worksheet.append_row(new_data)  # 🔹 Google Sheets にデータを追加
    st.success("日記を Google Sheets に保存しました！")

# Google Sheets からデータを読み込む
data = worksheet.get_all_values()
# 🔹 **データが空の場合の処理**
if not data:  # `data` が空なら
    df = pd.DataFrame(columns=["日付", "満足度", "体重", "自由記述"])  # 空のDataFrameを作成
else:
    df = pd.DataFrame(data[1:], columns=data[0])  # 1行目をヘッダーとして DataFrame を作成

# 過去のデータを表示
st.write("過去の日記")
st.dataframe(df)

# CSV ダウンロード機能
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="CSV をダウンロード",
    data=csv,
    file_name="diary.csv",
    mime="text/csv",
)
