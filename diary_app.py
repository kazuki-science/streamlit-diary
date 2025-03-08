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

# **🔹 Streamlit UI**
st.title("📖 日記入力フォーム")

# **🔹 Google Sheets からデータを取得**
try:
    data = worksheet.get_all_values()
except Exception as e:
    st.error(f"❌ スプレッドシートのデータ取得に失敗しました: {e}")
    data = []

# **🔹 DataFrame のカラムを修正**
columns = ["日付", "満足度", "天気", "外出時間", "入眠時間", "起床時間",
           "睡眠_深い", "睡眠_浅い", "睡眠_レム", "睡眠_覚醒数",
           "ストレスレベル", "食事満足度", "カロリー", "朝ごはん", "昼ごはん", "夜ごはん",
           "和紗の休日フラグ", "運動時間", "歩数", "筋トレフラグ",
           "仕事時間", "勉強時間", "趣味時間", "人と接した時間",
           "SNS利用時間", "YouTube利用時間", "家族といた時間", "友達といた時間",
           "ポジティブ出来事", "ネガティブ出来事", "1日のコメント"]

df = pd.DataFrame(data[1:], columns=columns) if data else pd.DataFrame(columns=columns)

# **🔹 指定した日付の行を削除する機能**
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

# **🔹 過去のデータを表示**
st.write("📜 過去の日記")
st.dataframe(df)

# **🔹 CSV ダウンロード機能**
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV をダウンロード", data=csv, file_name="diary.csv", mime="text/csv")
