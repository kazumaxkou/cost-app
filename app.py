import streamlit as st

material_cost = 3000

st.title("製造コスト見積もりツール")

# セッションで履歴保存（重要）
if "results" not in st.session_state:
    st.session_state.results = []
if "total_sum" not in st.session_state:
    st.session_state.total_sum = 0

# 入力
product_type = st.selectbox("製品タイプ", ["A", "B"])
time = st.number_input("加工時間（時間）", min_value=0.0)

# 計算ボタン
if st.button("計算"):
    if product_type == "A":
        cost = 1500
    else:
        cost = 2000

    total = time * cost + material_cost

    discount_flag = False
    if time >= 10:
        total *= 0.9
        discount_flag = True

    total = int(total)

    # CSV保存
     # ここで計算ボタンを押したときにだけ一回だけ保存(入力するたびに保存されないようにするため)
    if "last_saved" not in st.session_state:
        st.session_state.last_saved = None

    current_data = (product_type, time, total)

    if st.session_state.last_saved != current_data:
        with open("result.csv", "a", encoding="utf-8") as f:
            f.write(f"{product_type},{time},{total}\n")

        st.session_state.last_saved = current_data

    # 表示用文字
    output = f"製品タイプ:{product_type} / 加工時間:{time}h"
    if discount_flag:
        output += " → 割引適用！"
    output += f" → {total:,}円"

    # 履歴保存
    st.session_state.results.append(output)
    st.session_state.total_sum += total

# 表示（毎回）
st.write("--- これまでの計算結果 ---")
for r in st.session_state.results:
    st.write(r)

st.write("------------------------")
st.write(f"合計金額: {st.session_state.total_sum:,}円")

import pandas as pd

#グラフ表示
df = pd.read_csv("result.csv", names=["type", "time", "cost"])
st.write("売上推移")
st.line_chart(df["cost"])

#表の表示
st.dataframe(df)

#加工時間グラフ
st.line_chart(df[["time", "cost"]])

#棒グラフ
st.bar_chart(df["cost"])