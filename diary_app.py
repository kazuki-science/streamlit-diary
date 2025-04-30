import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets の設定
SHEET_ID = "1PH9nW0Eb46_OF_lEDkmhCYeq7Et2xoSpGKz5lpkjPB4"

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

# **🔹 DataFrame のカラムを定義**
columns = [
    "日付",
    "朝満足度",
    "昼満足度",
    "夜満足度",
    "情緒",
    "ストレス",
    "休日フラグ",
    "天気",
    "外出時間","体重",
    "入眠時間", "起床時間",
    "深い眠り", "浅い眠り", "レム睡眠", "覚醒回数",
    "食事満足度", "摂取カロリー",
    "朝ごはんフラグ", "昼ごはんフラグ", "夜ごはんフラグ",
    "午前カフェインフラグ", "午後カフェインフラグ",
    "飲酒フラグ", "和紗休日フラグ", "出勤フラグ",
    "有酸素運動時間", "無酸素運動時間", "歩数",
    "仕事の忙しさ", "仕事満足感",
    "スクリーンタイム", "エンタメタイム", "ゲームタイム", "SNSタイム",
    "家族といた時間", "親戚といた時間", "友達といた時間",
    "喧嘩フラグ",
    "朝の流れ", "昼の流れ", "夜の流れ"
]


df = pd.DataFrame(data[1:], columns=columns) if data else pd.DataFrame(columns=columns)

# **🔹 Streamlit UI**
# 🔹 日記入力フォーム
st.title("日記入力フォーム")

# 日付
date = st.date_input("日付")

# 朝・昼・夜の満足度・ストレス
morning_satisfaction = st.slider("朝満足度", 0, 10, 5)
morning_stress = st.slider("朝ストレス", 0, 10, 5)
noon_satisfaction = st.slider("昼満足度", 0, 10, 5)
noon_stress = st.slider("昼ストレス", 0, 10, 5)
night_satisfaction = st.slider("夜満足度", 0, 10, 5)
night_stress = st.slider("夜ストレス", 0, 10, 5)

# 情緒
emotion = st.selectbox("情緒", ["快適", "普通", "不快"])

# 総合ストレス
stress = st.number_input("ストレス（整数）", min_value=0, step=1)

# 休日・天気
holiday_flag = st.checkbox("休日フラグ")
weather = st.selectbox("天気", [
    "晴れ", "曇り", "雨", 
    "晴れのち曇り", "晴れのち雨", 
    "曇りのち晴れ", "曇りのち雨", 
    "雨のち晴れ", "雨のち曇り"
])

# 外出
outdoor_time = st.number_input("外出時間（分）", min_value=0, step=5)

# 体重
weight = st.number_input("体重（kg）", min_value=0, step=0.1)

# 睡眠
sleep_time = st.time_input("入眠時間")
wake_time = st.time_input("起床時間")
deep_sleep = st.number_input("深い眠り（分）", min_value=0, step=5)
light_sleep = st.number_input("浅い眠り（分）", min_value=0, step=5)
rem_sleep = st.number_input("レム睡眠（分）", min_value=0, step=5)
wake_count = st.number_input("覚醒回数", min_value=0, step=1)

# 食事
meal_satisfaction = st.slider("食事満足度", 1, 5, 3)
calories = st.number_input("摂取カロリー（kcal）", min_value=0, step=50)
breakfast_flag = st.checkbox("朝ごはんフラグ")
lunch_flag = st.checkbox("昼ごはんフラグ")
dinner_flag = st.checkbox("夜ごはんフラグ")
am_caffeine_flag = st.checkbox("午前カフェインフラグ")
pm_caffeine_flag = st.checkbox("午後カフェインフラグ")
alcohol_flag = st.checkbox("飲酒フラグ")

# その他生活フラグ
kazusa_holiday_flag = st.checkbox("和紗休日フラグ")
work_flag = st.checkbox("出勤フラグ")

# 運動
aerobic_time = st.number_input("有酸素運動時間（分）", min_value=0, step=5)
anaerobic_time = st.number_input("無酸素運動時間（分）", min_value=0, step=5)
steps = st.number_input("歩数", min_value=0, step=100)

# 仕事
work_busy = st.slider("仕事の忙しさ", 1, 5, 3)
work_satisfaction = st.slider("仕事満足感", 1, 5, 3)

# スクリーン・趣味
screen_time = st.number_input("スクリーンタイム（分）", min_value=0, step=5)
entertainment_time = st.number_input("エンタメタイム（分）", min_value=0, step=5)
creativity_time = st.number_input("ゲームタイム（分）", min_value=0, step=5)
sns_time = st.number_input("SNSタイム（分）", min_value=0, step=5)

# 対人
family_time = st.number_input("家族といた時間（分）", min_value=0, step=5)
relative_time = st.number_input("親戚といた時間（分）", min_value=0, step=5)
friend_time = st.number_input("友達といた時間（分）", min_value=0, step=5)

# イベント
quarrel_flag = st.checkbox("喧嘩フラグ")

# 朝昼夜の流れ
morning_flow = st.text_area("朝の流れ")
noon_flow = st.text_area("昼の流れ")
night_flow = st.text_area("夜の流れ")

# 🔹 保存ボタン
if st.button("日記を保存"):
    new_data = [
        str(date),
        morning_satisfaction, 
        noon_satisfaction, 
        night_satisfaction, 
        emotion,
        stress,
        int(holiday_flag),
        weather,
        outdoor_time, weight,
        sleep_time.strftime("%H:%M"), wake_time.strftime("%H:%M"),
        deep_sleep, light_sleep, rem_sleep, wake_count,
        meal_satisfaction, calories,
        int(breakfast_flag), int(lunch_flag), int(dinner_flag),
        int(am_caffeine_flag), int(pm_caffeine_flag),
        int(alcohol_flag), int(kazusa_holiday_flag), int(work_flag),
        aerobic_time, anaerobic_time, steps,
        work_busy, work_satisfaction,
        screen_time, entertainment_time, creativity_time, sns_time,
        family_time, relative_time, friend_time,
        int(quarrel_flag),
        morning_flow, noon_flow, night_flow
    ]
    
    try:
        worksheet.append_row(new_data)
        st.success("✅ 新しいフォーマットで日記を保存しました！")
    except Exception as e:
        st.error(f"❌ 保存に失敗しました: {e}")



# **🔹 日記の削除機能**
st.subheader("🗑 指定した日付のデータを削除")
delete_date = st.date_input("📅 削除したい日付を選択")

if st.button("🚮 指定日付のデータを削除"):
    if not df.empty:
        original_length = len(df)
        df = df[df["日付"] != str(delete_date)]  # 指定した日付を削除
        if len(df) < original_length:
            try:
                worksheet.clear()  # シートをクリア
                worksheet.append_row(columns)  # ヘッダーを再追加
                for row in df.values.tolist():
                    worksheet.append_row(row)  # 更新後のデータを追加
                st.success(f"✅ {delete_date} のデータを削除しました！")
            except Exception as e:
                st.error(f"❌ データの削除に失敗しました: {e}")
        else:
            st.warning(f"⚠ 指定した日付 {delete_date} のデータが見つかりませんでした。")
    else:
        st.warning("📭 データがありません。")
        
# **🔹 過去の日記を表示**
st.write("📜 過去の日記")
st.dataframe(df)

# **🔹 CSV ダウンロード機能**
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV をダウンロード", data=csv, file_name="diary.csv", mime="text/csv")

