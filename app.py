import streamlit as st
import pandas as pd

st.title("牠／它會或得與誰打交道？")

# GitHub Repo 原始檔案 URL
url_relations = "https://raw.githubusercontent.com/yuukumo/specimen-lookup-test/main/List_A_Relations.xlsx"
url_inventory = "https://raw.githubusercontent.com/yuukumo/specimen-lookup-test/main/List_B_Inventory.xlsx"

# 自動讀取清單 A 與 B
@st.cache_data
def load_data():
    relations_df = pd.read_excel(url_relations)
    inventory_df = pd.read_excel(url_inventory)
    return relations_df, inventory_df

relations_df, inventory_df = load_data()

# 使用者輸入物種名稱
st.subheader("請告訴我你想多瞭解誰的社交圈")
input_names = st.text_area("請貼上要查詢的物種中名清單（每行一個）：", height=200)

if st.button("比對並查詢"):
    if input_names.strip():
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
                matched_relations = relations_df[relations_df["vernacularName"] == query_species]
                if not matched_relations.empty:
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
        st.error("請輸入至少一個物種名稱。")
