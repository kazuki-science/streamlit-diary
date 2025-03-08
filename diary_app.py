import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "1PH9nW0Eb46_OF_lEDkmhCYeq7Et2xoSpGKz5lpkjPB4"

# 🔹 環境変数から Google Cloud の認証情報を取得
try:
    creds_dict = dict(st.secrets["GCP_SERVICE_ACCOUNT"])  # ✅ dict() でコピー
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")  # 🔹 改行を修正

    # ✅ スコープを明示的に指定
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

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

# **🔹 Google Sheets からデータを取得**
try:
    data = worksheet.get_all_values()
except Exception as e:
    st.error(f"❌ スプレッドシートのデータ取得に失敗しました: {e}")
    data = []

# **🔹 データの整形**
if data:
    # ✅ 1行目をヘッダーとして DataFrame を作成
    df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=data[0])

    # 🔹 数値データの変換（エラーを避けるため `errors='coerce'` を使用）
    numeric_cols = ["満足度", "外出時間", "睡眠_深い", "睡眠_浅い", "睡眠_レム", "睡眠_覚醒数",
                    "ストレスレベル", "食事満足度", "カロリー", "朝ごはん", "昼ごはん", "夜ごはん"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")  # 文字列が混ざっていても `NaN` に変換

    # 🔹 Boolean フラグを整数に変換
    bool_cols = ["朝ごはん", "昼ごはん", "夜ごはん"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)  # 欠損値を 0 にして整数型に変換

else:
    # 🔹 空の DataFrame を作成
    df = pd.DataFrame(columns=["日付", "満足度", "天気", "外出時間", "入眠時間", "起床時間",
                               "睡眠_深い", "睡眠_浅い", "睡眠_レム", "睡眠_覚醒数",
                               "ストレスレベル", "食事満足度", "カロリー", "朝ごはん", "昼ごはん", "夜ごはん"])

# **🔹 過去のデータを表示**
st.write("📜 過去の日記")
if not df.empty:
    st.dataframe(df)
else:
    st.write("📭 過去のデータがありません")

# **🔹 CSV ダウンロード機能**
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV をダウンロード", data=csv, file_name="diary.csv", mime="text/csv")


