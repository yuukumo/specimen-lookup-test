# Specimen Relation Lookup App (v12 - 移除載入訊息)

此版本功能：
1. 自動從 GitHub Repo 讀取清單 A (`List_A_Relations.xlsx`) 與清單 B (`List_B_Inventory.xlsx`)。
2. 查詢邏輯：輸入物種 -> 清單 A 的 vernacularName -> 取其 relatedVernacularName -> 清單 B 的 vernacularName -> 顯示標本倉儲位置。
3. 簡化介面，省略顯示「已從 GitHub 自動載入清單」訊息。

## 安裝與執行
```bash
pip install -r requirements.txt
streamlit run app.py
```
