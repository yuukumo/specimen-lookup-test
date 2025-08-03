import streamlit as st
import pandas as pd

st.title("物件關聯性與倉儲查詢工具 (修正比對邏輯)")

# 上傳清單 A：物件關聯性
st.subheader("上傳清單 A（物件關聯性）")
relations_file = st.file_uploader("請上傳 Excel 或 CSV 格式的清單 A", type=["xlsx", "csv"])

# 上傳清單 B：物種與倉儲位置
st.subheader("上傳清單 B（物種與倉儲位置）")
inventory_file = st.file_uploader("請上傳 Excel 或 CSV 格式的清單 B", type=["xlsx", "csv"])

# 輸入物種名稱
st.subheader("輸入物種名稱")
input_names = st.text_area("請貼上要查詢的物種名稱（每行一個）：", height=200)

def load_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if st.button("比對並查詢"):
    if relations_file and inventory_file and input_names.strip():
        relations_df = load_file(relations_file)
        inventory_df = load_file(inventory_file)

        required_relations_cols = {"vernacularName", "relatedVernacularName", "relationshipOfResource"}
        required_inventory_cols = {"occurrenceID", "vernacularName", "storageLocation"}

        if not required_relations_cols.issubset(relations_df.columns):
            st.error(f"清單 A 缺少必要欄位: {required_relations_cols}")
        elif not required_inventory_cols.issubset(inventory_df.columns):
            st.error(f"清單 B 缺少必要欄位: {required_inventory_cols}")
        else:
            input_list = [name.strip() for name in input_names.splitlines() if name.strip()]
            results_all = []

            for query_species in input_list:
                # 在清單 A 的 vernacularName 中尋找匹配的 query_species
                matched_relations = relations_df[relations_df["vernacularName"] == query_species]

                if not matched_relations.empty:
                    # 找到的 relatedVernacularName 再去清單 B 比對
                    merged = pd.merge(
                        matched_relations,
                        inventory_df,
                        left_on="relatedVernacularName",
                        right_on="vernacularName",
                        how="inner"
                    )

                    if not merged.empty:
                        merged["查詢物種"] = query_species
                        merged = merged[[
                            "查詢物種",
                            "relatedVernacularName",
                            "storageLocation"
                        ]]
                        merged.rename(columns={
                            "relatedVernacularName": "關聯物種",
                            "storageLocation": "標本倉儲位置"
                        }, inplace=True)
                        results_all.append(merged)

            if results_all:
                result = pd.concat(results_all, ignore_index=True)
                st.success("以下是與輸入物種存在關聯的標本及倉儲位置：")
                st.dataframe(result)
            else:
                st.warning("沒有找到與這些物種相關聯的物件或標本位置。")
    else:
        st.error("請確保已上傳清單 A 和清單 B，並輸入至少一個物種名稱。")
