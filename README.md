# 🇧🇷 Brazil Healthcare Capacity Analytics Engine

A data analytics pipeline that processes Brazilian public healthcare datasets to generate actionable insights about hospital capacity, ICU availability, and population-based healthcare metrics.

This project simulates a real-world **data engineering + analytics workflow**, transforming raw government data into structured, analysis-ready outputs.

---

## 🚀 Overview

Healthcare capacity is a critical factor in public policy and emergency response. This project focuses on:

* Aggregating hospital infrastructure data
* Integrating population estimates
* Computing **per capita healthcare metrics**
* Identifying regional disparities in ICU availability

---

## 📊 Key Features

* ✅ Data ingestion from real government sources
* ✅ Data cleaning (encoding, formatting, normalization)
* ✅ Robust dataset merging (handling inconsistencies in city names)
* ✅ Feature engineering (ICU per capita metrics)
* ✅ Aggregation from hospital-level → city-level
* ✅ Ranking and analysis of healthcare capacity
* ✅ Export to CSV and Excel for reporting
* ✅ Data visualization (Top cities by ICU availability)

---

## 🗂️ Data Sources

### 🏥 Hospital Infrastructure

* Dataset: **"Leitos 2026"**
* Source: [https://dados.gov.br/dados/conjuntos-dados/hospitais-e-leitos](https://dados.gov.br/dados/conjuntos-dados/hospitais-e-leitos)
* Contains:

  * Hospital information
  * Available beds (general, ICU adult, pediatric, neonatal)
  * Contact and unit type data

---

### 👥 Population Data

* Dataset: **"POP2025"**
* Source: [https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2025/](https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2025/)
* Contains:

  * Estimated population per municipality

---

## ⚙️ Pipeline Architecture

```text
Raw CSVs
   ↓
Data Cleaning
   - Encoding fixes (UTF-8 / latin-1)
   - Column normalization
   - Numeric parsing (Brazilian formats)
   ↓
Data Validation
   - Required columns
   - Missing values
   ↓
Data Integration (Merge)
   - Municipality normalization
   - Join hospital + population data
   ↓
Aggregation
   - Group by (UF, Município)
   - Sum ICU capacity
   ↓
Feature Engineering
   - ICU per capita metrics
   ↓
Analysis & Ranking
   - Top cities by ICU availability
   ↓
Export
   - CSV / Excel
   - Visualizations
```

---

## 🧠 Key Metrics

* **UTI_TOTAL_SUS**
  Total ICU beds available per city

* **UTI_TOTAL_PER_CAPITA**
  ICU beds normalized by population

```text
UTI_TOTAL_PER_CAPITA = Total ICU Beds / Population
```

---

## 📈 Example Analysis

* Top 10 cities with highest ICU availability per capita
* Comparison across states (UF)
* Identification of underserved regions
* Detection of data inconsistencies (e.g., missing population)

---

## ⚠️ Data Challenges Solved

This project handles several real-world data issues:

* Inconsistent municipality naming (accents, casing)
* Mixed encodings (`latin-1` vs UTF-8)
* Brazilian numeric formats (`1.234.567`)
* Missing or misaligned columns in CSVs
* Merge mismatches between datasets
* Division errors (e.g., `inf` from zero population)

---

## 🛠️ Tech Stack

* Python
* pandas
* matplotlib
* openpyxl / xlsxwriter

---

## 📁 Project Structure

```text
src/
  ├── main.py
  ├── data_loader.py
  ├── processing.py
  ├── analysis.py

data/
  ├── raw/
  ├── processed/

outputs/
  ├── csv/
  ├── excel/
  ├── plots/
```

---

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/Brazil-Healthcare-Capacity-Analytics-Engine.git
cd Brazil-Healthcare-Capacity-Analytics-Engine
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the pipeline:

```bash
python src/main.py
```

---

## 📤 Outputs

* Cleaned datasets
* Aggregated city-level metrics
* Ranked ICU capacity results
* Excel reports
* Visualizations (Top cities)

---

## 🎯 Future Improvements

* Integrate municipality codes (IBGE) for more reliable joins
* Add geospatial visualization (maps)
* Build an interactive dashboard (Streamlit / Power BI)
* Time-series analysis of healthcare capacity
* Predictive modeling for demand vs capacity

---

## 💡 What This Project Demonstrates

* Data cleaning and preprocessing in real-world scenarios
* Handling messy public datasets
* Building reliable data pipelines
* Analytical thinking and metric design
* Translating raw data into business-relevant insights

---

## 📌 Author

Developed as a portfolio project focused on **Data Analytics and Data Engineering** in the healthcare domain.