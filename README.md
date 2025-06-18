# Prescription Cost Analysis with dbt & Streamlit

This project explores prescription cost data in England using **dbt (Data Build Tool)** for data modeling and **Streamlit** for interactive visualizations.

📍 **Live App:** [View on Streamlit](https://prescription-cost-analysis-with-dbt-ae3rmv6segeqr6du2lxwrs.streamlit.app/)

---

## 🎯 Project Purpose

The primary goal of this project was to gain **hands-on experience with dbt**. The project demonstrates:

- Setting up and structuring a dbt project
- Building data marts
- Generating documentation and tests
- Deploying a polished frontend using Streamlit
- Leveraging DuckDB as a fast, embedded data warehouse

This project showcases my ability to work across the modern data stack.

---

## 🧱 Architecture Overview

- **dbt** for transformation, modular SQL, testing, documentation
- **DuckDB** as the local analytical data warehouse
- **Streamlit** for the interactive data dashboard
- **Pandas, Plotly & Matplotlib** for data manipulation and visualizations in Python

---

## 📊 About the Data

The data comes from the [NHS Business Services Authority (NHSBSA)](https://opendata.nhsbsa.net/)'s **Prescription Cost Analysis (PCA)** annual release. This is an **official statistic** covering all prescription items dispensed in community settings across England.

Key points:

- Data covers item counts and associated Net Ingredient Cost (NIC)
- Granular breakdown by **BNF Chapter**, **Section**, and **Paragraph**
- Used to visualize cost distribution and prescribing patterns

📁 [Go directly to the PCA dataset](https://opendata.nhsbsa.net/dataset/prescription-cost-analysis-pca-annual-statistics/resource/b8cf68a5-4a93-4940-a5c1-4064bc947ffb)

---

## 🛠️ How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/chloestipinovich/prescription-cost-analysis-with-dbt.git
cd prescription-cost-analysis-with-dbt
