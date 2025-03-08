import streamlit as st
import pandas as pd
import os

# CSV ファイルの保存先
CSV_FILE = "/Users/kazukiichikawa/Desktop/diary/diary.csv"

# CSV の初期化（ファイルがない場合のみ）
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["日付", "満足度", "体重", "自由記述"])
    df.to_csv(CSV_FILE, index=False)

# Streamlit UI
st.title("日記入力フォーム")

# 入力フォーム
date = st.date_input("日付を選択")
satisfaction = st.slider("1日の満足度 (1〜5)", 1, 5, 3)
weight = st.number_input("体重 (kg)", min_value=30.0, max_value=150.0, step=0.1)
note = st.text_area("自由記述")

if st.button("保存"):
    # 新しいデータを DataFrame に変換
    new_data = pd.DataFrame([[date, satisfaction, weight, note]], columns=["日付", "満足度", "体重", "自由記述"])
    
    # 既存の CSV に追記
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    
    st.success("日記を保存しました！")


