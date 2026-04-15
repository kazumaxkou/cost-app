import streamlit as st
import pandas as pd
import os
import datetime

# =====================
# 定数
# =====================
material_cost = 3000

st.title("製造コスト見積もりツール")
st.caption("製品タイプと加工時間からコストを自動計算します")

# =====================
# セッション初期化
# =====================
if "results" not in st.session_state:
    st.session_state.results = []

if "total_sum" not in st.session_state:
    st.session_state.total_sum = 0

if "last_saved" not in st.session_state:
    st.session_state.last_saved = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =====================
# 入力
# =====================
product_type = st.selectbox("製品タイプ", ["A", "B"])
time = st.number_input("加工時間（時間）※10時間以上で割引", min_value=0.0)

# =====================
# 計算処理（ボタン）
# =====================
if st.button("計算"):
    cost = 1500 if product_type == "A" else 2000

    total = time * cost + material_cost
    discount_flag = False

    if time >= 10:
        total *= 0.9
        discount_flag = True

    total = int(total)

    current_data = (product_type, time, total)

    # CSV保存（重複防止）
    if st.session_state.last_saved != current_data:
        with open("result.csv", "a", encoding="utf-8") as f:
            f.write(f"{product_type},{time},{total}\n")

        st.session_state.last_saved = current_data

    # 結果保存（ここが重要）
    st.session_state.last_result = {
        "type": product_type,
        "time": time,
        "total": total,
        "discount": discount_flag
    }

    # 履歴保存
    text = f"製品タイプ:{product_type} / 加工時間:{time}h"
    if discount_flag:
        text += " → 割引適用！"
    text += f" → {total:,}円"

    st.session_state.results.append(text)
    st.session_state.total_sum += total

# =====================
# 最新結果表示（安全）
# =====================
if st.session_state.last_result:
    r = st.session_state.last_result

    st.subheader("計算結果")
    text = f"製品タイプ:{r['type']} / 加工時間:{r['time']}h"
    if r["discount"]:
        text += " → 割引適用！"
    text += f" → {r['total']:,}円"

    st.success(text)

# =====================
# 履歴表示
# =====================
st.subheader("計算履歴")

if st.session_state.results:
    for r in st.session_state.results:
        st.write(r)
else:
    st.write("まだ履歴がありません")

st.write(f"合計金額: {st.session_state.total_sum:,}円")

# =====================
# データ表示・グラフ
# =====================
st.subheader("売上データ")

if os.path.exists("result.csv"):
    df = pd.read_csv("result.csv", names=["type", "time", "cost"])

    st.dataframe(df)

    st.subheader("売上推移")
    st.line_chart(df["cost"])

    # CSVダウンロード
    csv = df.to_csv(index=False).encode("utf-8")
    file_name = f"result_{datetime.date.today()}.csv"

    st.download_button(
        label="CSVダウンロード",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )
else:
    st.write("まだデータがありません")

# =====================
# リセット機能（確実に表示）
# =====================
st.divider()

if st.button("履歴リセット"):
    st.session_state.results = []
    st.session_state.total_sum = 0
    st.session_state.last_saved = None
    st.session_state.last_result = None

    if os.path.exists("result.csv"):
        os.remove("result.csv")

    st.success("リセットしました")