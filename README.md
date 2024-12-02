# Job Analysis Tool

自動爬取 104 人力銀行職缺資訊並進行分析的工具。

## 功能特點

- 爬取 104 人力銀行職缺資訊
- 使用 OpenAI API 進行職缺內容分析
- 提供技能和工具需求的統計分析
- 網頁化介面展示分析結果

## 安裝說明

1. 克隆專案
```bash
git clone https://github.com/elviawu/crawler_LLM_job_analysis.git
cd crawler_LLM_job_analysis
```

2. 安裝 Poetry（如果尚未安裝）
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. 安裝依賴
```bash
poetry install
```

4. 設置環境變數
```bash
cp .env.example .env
# 編輯 .env 文件，填入您的 OpenAI API 密鑰
```

## 使用方法

1. 啟動 Streamlit 應用：
```bash
poetry run streamlit run src/app.py
```

2. 在瀏覽器中訪問：
```
http://localhost:8501
```

## 開發說明

- Python 版本：3.12
- 主要依賴：
  - Streamlit
  - OpenAI
  - Selenium
  - Pandas
  - Plotly

## 授權

MIT License