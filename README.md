# Specimen Relation Lookup App (v9 簡化結果)

此版本功能：
1. 清單 A 使用 `vernacularName`, `relatedVernacularName`, `relationshipOfResource`。
2. 清單 B 使用 `occurrenceID`, `vernacularName`, `storageLocation`。
3. 查詢結果僅顯示「查詢物種」「關聯物種」「標本倉儲位置」，並取消顏色標示。

## 安裝與執行
```bash
pip install -r requirements.txt
streamlit run app.py
```
