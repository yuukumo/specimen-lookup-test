import streamlit as st
import pandas as pd
import random

st.title("物件關聯性與倉儲查詢工具 (來源與關聯物種顏色標籤)")

# 上傳清單 A：物件關聯性
st.subheader("上傳清單 A（物件關聯性）")
relations_file = st.file_uploader("請上傳 Excel 或 CSV 格式的清單 A", type=["xlsx", "csv"])

# 上傳清單 B：物種與倉儲位置
st.subheader("上傳清單 B（物種與倉儲位置）")
inventory_file = st.file_uploader("請上傳 Excel 或 CSV 格式的清單 B", type=["xlsx", "csv"])

# 產生隨機顏色
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

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
            matched_inventory = inventory_df[inventory_df["vernacularName"].isin(input_list)]

            if not matched_inventory.empty:
                results_all = []

                for _, query_row in matched_inventory.iterrows():
                    query_species = query_row["vernacularName"]
                    
                    related = relations_df[(relations_df["vernacularName"] == query_species) |
                                           (relations_df["relatedVernacularName"] == query_species)]

                    if not related.empty:
                        merged = pd.merge(
                            related,
                            inventory_df.add_suffix("_resource"),
                            left_on="vernacularName",
                            right_on="vernacularName_resource",
                            how="left"
                        )
                        merged = pd.merge(
                            merged,
                            inventory_df.add_suffix("_related"),
                            left_on="relatedVernacularName",
                            right_on="vernacularName_related",
                            how="left"
                        )
                        merged["querySpecies"] = query_species
                        results_all.append(merged)

                if results_all:
                    result = pd.concat(results_all, ignore_index=True)
                    result = result[[
                        "querySpecies",
                        "vernacularName", "storageLocation_resource",
                        "relatedVernacularName", "relationshipOfResource", "storageLocation_related"
                    ]]
                    result.rename(columns={
                        "querySpecies": "查詢物種",
                        "vernacularName": "來源物種",
                        "storageLocation_resource": "來源物種標本與倉儲位置",
                        "relatedVernacularName": "關聯物種",
                        "relationshipOfResource": "關聯性",
                        "storageLocation_related": "關聯物種標本與倉儲位置"
                    }, inplace=True)

                    # 建立顏色映射
                    unique_query = result["查詢物種"].unique()
                    unique_source = result["來源物種"].unique()
                    unique_related = result["關聯物種"].unique()

                    query_color_map = {species: random_color() for species in unique_query}
                    source_color_map = {species: random_color() for species in unique_source}
                    related_color_map = {species: random_color() for species in unique_related}

                    # 套用顏色標籤
                    def highlight_species(row):
                        styles = []
                        for col in row.index:
                            if col == "查詢物種":
                                styles.append(f"background-color: {query_color_map.get(row[col], '#ffffff')}; font-weight: bold;")
                            elif col == "來源物種":
                                styles.append(f"background-color: {source_color_map.get(row[col], '#ffffff')};")
                            elif col == "關聯物種":
                                styles.append(f"background-color: {related_color_map.get(row[col], '#ffffff')};")
                            else:
                                styles.append("")
                        return styles

                    st.success("以下是與輸入物種存在關聯的物件與資訊：")
                    st.dataframe(result.style.apply(highlight_species, axis=1))
                else:
                    st.warning("沒有找到與這些物種相關聯的物件。")
            else:
                st.warning("輸入的物種名稱未在清單 B 中找到。")
    else:
        st.error("請確保已上傳清單 A 和清單 B，並輸入至少一個物種名稱。")
