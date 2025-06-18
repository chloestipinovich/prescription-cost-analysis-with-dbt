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

## 🧱 Architecture Overview

- **dbt** for transformation, modular SQL, testing, documentation
- **DuckDB** as the local analytical data warehouse
- **Streamlit** for the interactive data dashboard
- **Pandas, Plotly & Matplotlib** for data manipulation and visualizations in Python

## 📊 About the Data

The data comes from the [NHS Business Services Authority (NHSBSA)](https://opendata.nhsbsa.net/)'s **Prescription Cost Analysis (PCA)** annual release. This is an **official statistic** covering all prescription items dispensed in community settings across England.

Key points:

- Data covers item counts and associated Net Ingredient Cost (NIC)
- Granular breakdown by **BNF Chapter**, **Section**, and **Paragraph**
- Used to visualize cost distribution and prescribing patterns

📁 [Go directly to the PCA dataset](https://opendata.nhsbsa.net/dataset/prescription-cost-analysis-pca-annual-statistics/resource/b8cf68a5-4a93-4940-a5c1-4064bc947ffb)

## 🛠️ How to Reproduce the Data Warehouse Locally

### 1. Clone the repo

```bash
git clone https://github.com/chloestipinovich/prescription-cost-analysis-with-dbt.git
```
```bash
cd prescription-cost-analysis-with-dbt
```

### 2.1 Set Up the Virtual Environment (Optional)

```bash
# Create a virtual environment
uv venv venv
```

```bash
# Activate the virtual environment
# On Windows:
. venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
# Install dependencies using pip
pip install -r requirements.txt
```
```bash
# Optional: Use uv for faster installation (if installed)
uv pip install -r requirements.txt --link-mode=copy

```

### 3. Download the Original Data
Download the original prescription data from [this link](https://opendata.nhsbsa.net/dataset/prescription-cost-analysis-pca-annual-statistics/resource/b8cf68a5-4a93-4940-a5c1-4064bc947ffb) and place it in a new `data` directory:

```bash
# Create the data directory
mkdir data
```

```bash
# Move your downloaded file to the data folder and rename it
# (Update path if necessary)
mv ~/Downloads/pca_icb_snomed_2024_2025.csv ./data/pca_icb_snomed_2024_2025.csv
```

### 4. Run the DBT Models

#### ⚙️ 4.0 Configure your `profiles.yml`

Before running `dbt` models, ensure your `profiles.yml` is properly set up with your database connection details. On most systems, the `profiles.yml` file is located at:

- Linux/macOS: ~/.dbt/`profiles.yml`  
- Windows: C:\Users\<your-username>\.dbt\`profiles.yml`

Paste the below into your `profiles.yml` file to match this project's `dbt_project.yml`’s profile name:
```bash
pca_with_dbt:
  outputs:
    dev:
      type: duckdb
      path: pca_with_dbt.duckdb
      threads: 1
  target: dev
```

#### ⚙️ 4.1 Run the transformation pipeline using `dbt`:

```bash
# Move the data to the seeds folder
mv data/pca_icb_snomed_2024_2025.csv seeds/
```
```bash
# load the pca_icb_snomed_2024_2025.csv into the database
dbt seed
```
```bash
# Run the staging models to base/staging tables from the raw data
dbt run --select staging
```
```bash
# Then run the mart models to build the transformed tables or views used in analysis
dbt run --select marts
```

### 5. View the Database
Use a SQL client like `DBeaver` to inspect the transformed data:

- Connect to your local database (e.g., SQLite, Postgres, etc.)

- Explore schemas such as staging and marts