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

# **🔹 時間・活動データ**
outdoor_time = st.number_input("🚶 外出時間 (分)", min_value=0, step=5)

# **🔹 time_input() で時:分を入力**
sleep_time = st.time_input("😴 入眠時間")
wake_time = st.time_input("⏰ 起床時間")

deep_sleep = st.number_input("💤 睡眠_深い (分)", min_value=0, step=5)
light_sleep = st.number_input("💤 睡眠_浅い (分)", min_value=0, step=5)
rem_sleep = st.number_input("💭 睡眠_レム (分)", min_value=0, step=5)
wake_count = st.number_input("🌙 睡眠_覚醒数 (回)", min_value=0, step=1)

# **🔹 健康 & 生活習慣**
stress = st.slider("⚡ ストレスレベル (1〜5)", 1, 5, 3)
meal_satisfaction = st.slider("🍽 食事満足度 (1〜5)", 1, 5, 3)
calories = st.number_input("🔥 カロリー", min_value=0, step=50)
breakfast_flag = st.checkbox("🍳 朝ごはんフラグ")
lunch_flag = st.checkbox("🥗 昼ごはんフラグ")
dinner_flag = st.checkbox("🍛 夜ごはんフラグ")

# **🔹 保存ボタン**
if st.button("📌 保存"):
    new_data = [
        str(date), satisfaction, weather, outdoor_time, 
        sleep_time.strftime("%H:%M"), wake_time.strftime("%H:%M"),  # ✅ strftime で時間フォーマット
        deep_sleep, light_sleep, rem_sleep, wake_count, stress, meal_satisfaction,
        calories, int(breakfast_flag), int(lunch_flag), int(dinner_flag)
    ]
    
    try:
        worksheet.append_row(new_data)  # 🔹 Google Sheets にデータを追加
        st.success("✅ 日記を Google Sheets に保存しました！")
    except Exception as e:
        st.error(f"❌ データの保存に失敗しました: {e}")

# **🔹 Google Sheets からデータを読み込む**
try:
    data = worksheet.get_all_values()
except Exception as e:
    st.error(f"❌ スプレッドシートのデータ取得に失敗しました: {e}")
    data = []

# **🔹 データが空の場合の処理**
if data:
    # ✅ 1行目をヘッダーとして DataFrame を作成
    df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=data[0])
else:
    df = pd.DataFrame(columns=["日付", "満足度", "天気", "外出時間", "入眠時間", "起床時間",
                               "睡眠_深い", "睡眠_浅い", "睡眠_レム", "睡眠_覚醒数",
                               "ストレスレベル", "食事満足度", "カロリー", "朝ごはん", "昼ごはん", "夜ごはん"])

# **🔹 過去のデータを表示（エラー回避のため df.empty をチェック）**
st.write("📜 過去の日記")
if not df.empty:
    st.dataframe(df)
else:
    st.write("📭 過去のデータがありません")

# **🔹 CSV ダウンロード機能**
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV をダウンロード", data=csv, file_name="diary.csv", mime="text/csv")



