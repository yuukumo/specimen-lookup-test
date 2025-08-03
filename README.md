# Specimen Lookup App

這是一個使用 [Streamlit](https://streamlit.io) 開發的簡易線上工具，用於比對物件所屬物種名稱與清單 A，並回傳符合名稱的物件及其倉儲位址。

## 功能
- 使用者貼上要查詢的一長串物種名稱（每行一個名稱）。
- 系統比對清單 A 中的名稱，並顯示符合的物件與倉儲位置。

## 安裝與執行
1. 安裝必要套件：
   ```bash
   pip install -r requirements.txt
   ```

2. 啟動應用程式：
   ```bash
   streamlit run app.py
   ```

## 部署到 Streamlit Cloud
1. 將本專案推送到 GitHub。
2. 登入 [Streamlit Cloud](https://streamlit.io/cloud)。
3. 建立新應用程式，連結到此 Repo 並指定 `app.py` 為主要檔案。
4. 完成後取得公開網址即可使用。
