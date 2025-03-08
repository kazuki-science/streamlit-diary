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
weather_options = weather_options = [
    "晴れ", "曇り", "雨", "雪", "雷雨", "霧", "強風",
    "晴れのち曇り", "晴れのち雨", "晴れのち雪",
    "曇りのち晴れ", "曇りのち雨", "曇りのち雪",
    "雨のち晴れ", "雨のち曇り", "雨のち雪",
    "雪のち晴れ", "雪のち曇り", "雪のち雨"
]

weather = st.selectbox("🌦 天気", weather_options)

# **🔹 時間・活動データ**
outdoor_time = st.number_input("🚶 外出時間 (分)", min_value=0, step=5)
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

# **🔹 運動 & 仕事 & 趣味**
exercise_time = st.number_input("🏋️‍♂️ 運動時間 (分)", min_value=0, step=5)
steps = st.number_input("🚶‍♂️ 歩数", min_value=0, step=100)
workout_flag = st.checkbox("💪 筋トレフラグ")
work_time = st.number_input("💼 仕事時間 (時間)", min_value=0, max_value=24)
study_time = st.number_input("📖 勉強時間 (分)", min_value=0, step=5)
hobby_time = st.number_input("🎨 趣味時間 (分)", min_value=0, step=5)

# **🔹 人との交流 & SNS 利用**
social_time = st.number_input("🧑‍🤝‍🧑 人と接した時間 (分)", min_value=0, step=5)
sns_time = st.number_input("📱 SNS利用時間 (分)", min_value=0, step=5)
youtube_time = st.number_input("▶️ YouTube利用時間 (分)", min_value=0, step=5)
family_time = st.number_input("👨‍👩‍👧‍👦 家族といた時間 (分)", min_value=0, step=5)
friends_time = st.number_input("🎉 友達といた時間 (分)", min_value=0, step=5)

# **🔹 一日の出来事**
positive_event = st.text_area("🌟 ポジティブな出来事")
negative_event = st.text_area("🌧 ネガティブな出来事")
daily_comment = st.text_area("📝 1日のコメント")

# **🔹 保存ボタン**
if st.button("📌 保存"):
    new_data = [
        str(date), satisfaction, weather, outdoor_time, sleep_time, wake_time,
        deep_sleep, light_sleep, rem_sleep, wake_count, stress, meal_satisfaction,
        calories, int(breakfast_flag), int(lunch_flag), int(dinner_flag),
        exercise_time, steps, int(workout_flag), work_time, study_time, hobby_time,
        social_time, sns_time, youtube_time, family_time, friends_time,
        positive_event, negative_event, daily_comment
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
    df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=data[0])
else:
    df = pd.DataFrame(columns=[
        "日付", "満足度", "天気", "外出時間", "入眠時間", "起床時間",
        "睡眠_深い", "睡眠_浅い", "睡眠_レム", "睡眠_覚醒数",
        "ストレスレベル", "食事満足度", "カロリー",
        "朝ごはん", "昼ごはん", "夜ごはん",
        "運動時間", "歩数", "筋トレ", "仕事時間", "勉強時間", "趣味時間",
        "人と接した時間", "SNS利用時間", "YouTube利用時間",
        "家族といた時間", "友達といた時間",
        "ポジティブな出来事", "ネガティブな出来事", "1日のコメント"
    ])

# **🔹 過去のデータを表示**
st.write("📜 過去の日記")
st.dataframe(df)

# **🔹 CSV ダウンロード機能**
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV をダウンロード", data=csv, file_name="diary.csv", mime="text/csv")

