import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "1PH9nW0Eb46_OF_lEDkmhCYeq7Et2xoSpGKz5lpkjPB4"

# **🔹 保存するカラム（ヘッダー）**
header_row = ["日付", "満足度", "天気", "外出時間", "入眠時間", "起床時間"]

# 🔹 環境変数から Google Cloud の認証情報を取得
try:
    creds_dict = dict(st.secrets["GCP_SERVICE_ACCOUNT"])  
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")  

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
    worksheet = spreadsheet.sheet1  

    # **🔹 ヘッダー行が存在しない場合は追加**
    existing_header = worksheet.row_values(1)  # 1行目を取得
    if not existing_header:  
        worksheet.insert_row(header_row, 1)  # 1行目にヘッダーを追加

except Exception as e:
    st.error(f"❌ Google Sheets への接続に失敗しました: {e}")
    st.stop()

# Streamlit UI
st.title("📖 日記入力フォーム")

# **🔹 入力フォーム**
date = st.date_input("📅 日付を選択")
satisfaction = st.slider("😊 1日の満足度 (1〜5)", 1, 5, 3)

# **🔹 天気の選択**
weather_options = [
    "晴れ", "曇り", "雨", "雪", "雷雨", "霧", "強風",
    "晴れのち曇り", "晴れのち雨", "晴れのち雪",
    "曇りのち晴れ", "曇りのち雨", "曇りのち雪",
    "雨のち晴れ", "雨のち曇り", "雨のち雪",
    "雪のち晴れ", "雪のち曇り", "雪のち雨"
]
weather = st.selectbox("🌦 天気", weather_options)

# **🔹 時間の入力**
outdoor_time = st.number_input("🚶 外出時間 (分)", min_value=0, step=5)
sleep_time = st.time_input("😴 入眠時間")
wake_time = st.time_input("⏰ 起床時間")

# **🔹 保存ボタン**
if st.button("📌 保存"):
    new_data = [
        str(date), satisfaction, weather, outdoor_time,
        sleep_time.strftime("%H:%M"), wake_time.strftime("%H:%M")  
    ]
    
    try:
        worksheet.append_row(new_data)  
        st.success("✅ 日記を Google Sheets に保存しました！")
    except Exception as e:
        st.error(f"❌ データの保存に失敗しました: {e}")

# **🔹 Google Sheets からデータを読み込む**
try:
    data = worksheet.get_all_values()
    data = [row for row in data if any(row)]  # ✅ 空白行を除外

except Exception as e:
    st.error(f"❌ スプレッドシートのデータ取得に失敗しました: {e}")
    data = []

# **🔹 データフレームの作成（ヘッダーがあるか確認）**
if len(data) > 1:
    df = pd.DataFrame(data[1:], columns=data[0])
else:
    df = pd.DataFrame(columns=header_row)  

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
