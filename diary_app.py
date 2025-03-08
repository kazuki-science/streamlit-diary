import streamlit as st
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "あなたのスプレッドシートIDをここに入力"

# 🔹 環境変数から Google Cloud の認証情報を取得
json_creds = os.getenv("GCP_SERVICE_ACCOUNT")

# 🔹 JSON 文字列を辞書型に変換
if json_creds:
    creds_dict = json.loads(json_creds)

    # 🔹 `private_key` の改行を修正
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = Credentials.from_service_account_info(creds_dict)
else:
    st.error("認証情報が設定されていません！Streamlit Cloud の Secrets を確認してください。")
    st.stop()

# 🔹 Google Sheets API に接続
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1  # 最初のシートを選択

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

