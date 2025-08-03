import streamlit as st
import pandas as pd

# 模擬清單 A（正式使用時可改成上傳 Excel/CSV 檔案）
data = {
    "Object": ["Specimen1", "Specimen2", "Specimen3", "Specimen4"],
    "Species Name": ["白頭翁", "麻雀", "雀榕", "榕小蜂"],
    "Storage Location": ["A1", "B2", "C3", "D4"]
}
df = pd.DataFrame(data)

st.title("物件名稱比對與倉儲查詢工具")
st.write("請在下方貼上要查詢的一長串名字（每行一個名字）：")

# 使用者輸入物種名稱清單
input_names = st.text_area("輸入物種名稱：", height=200)

if st.button("比對並查詢"):
    if input_names.strip():
        # 將輸入的字串分行轉為清單，並去除空白
        input_list = [name.strip() for name in input_names.splitlines() if name.strip()]

        # 在清單 A 中比對
        matched_df = df[df["Species Name"].isin(input_list)]

        if not matched_df.empty:
            st.success("找到以下符合的物件：")
            st.dataframe(matched_df)
        else:
            st.warning("未找到任何符合的物件名稱。")
    else:
        st.error("請輸入至少一個物種名稱。")
