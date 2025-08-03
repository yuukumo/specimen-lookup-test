# Specimen Relation Lookup App (v10 修正比對邏輯)

此版本功能：
1. 清單 A 使用 `vernacularName`, `relatedVernacularName`, `relationshipOfResource`。
2. 清單 B 使用 `occurrenceID`, `vernacularName`, `storageLocation`。
3. 查詢邏輯：輸入物種 -> 清單 A 的 vernacularName -> 取其 relatedVernacularName -> 清單 B 的 vernacularName -> 顯示標本倉儲位置。

## 安裝與執行
```bash
pip install -r requirements.txt
streamlit run app.py
```
