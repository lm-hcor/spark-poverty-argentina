# Multidimensional Poverty in Argentina with PySpark

## Overview

This project applies **Apache Spark and PySpark** to the large-scale processing and analysis of socioeconomic data from Argentina.

It extends my Master's research on **multidimensional poverty in Argentina** into a Big Data environment, focusing on distributed data processing, feature engineering and territorial analysis.

The project explores how scalable data-processing techniques can be applied to complex social research questions involving household-level socioeconomic data.

---

## Research Question

**How can distributed data processing help identify socioeconomic and territorial patterns associated with multidimensional poverty in Argentina?**

The analysis focuses on dimensions including:

* Income and economic vulnerability
* Employment
* Education
* Housing conditions
* Access to basic services
* Household characteristics
* Demographic factors
* Regional inequalities

---

## Technologies

* **Python**
* **Apache Spark**
* **PySpark**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Jupyter Notebook**
* **Git / GitHub**

The core data-processing pipeline is implemented in **PySpark**.

---

## Data

The project uses socioeconomic microdata from Argentina, with a focus on household and individual characteristics relevant to multidimensional poverty.

The analysis is based on data from the **Encuesta Permanente de Hogares (EPH)** and related socioeconomic information.

The dataset contains variables covering areas such as income, employment, education, housing, household composition and geographic location.

---

## Project Structure

```text
argentina-poverty-pyspark/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pyspark_processing.ipynb
│   └── 03_poverty_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── preprocessing.py
│   ├── poverty.py
│   └── analysis.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Methodology

### 1. Data Ingestion

Raw socioeconomic data are loaded into Spark DataFrames and prepared for distributed processing.

### 2. Data Preprocessing

The preprocessing pipeline includes:

* Schema validation
* Data type conversion
* Missing-value treatment
* Variable standardization
* Filtering and cleaning
* Feature construction

### 3. Distributed Data Processing

PySpark is used to perform large-scale transformations and aggregations.

The pipeline makes use of:

* DataFrame transformations
* Filtering
* Joins
* Grouped aggregations
* Window functions
* Spark SQL
* Partitioning strategies

### 4. Multidimensional Poverty Indicators

Socioeconomic variables are transformed into indicators representing different dimensions of deprivation and vulnerability.

These indicators are combined to construct an analytical framework for identifying multidimensional poverty.

### 5. Territorial Analysis

The processed data are aggregated across geographic areas to examine territorial differences in socioeconomic vulnerability.

This allows the analysis to move beyond individual households and identify broader regional patterns.

### 6. Analysis

The resulting datasets are used to investigate:

* Regional differences in poverty
* Socioeconomic inequalities
* Household characteristics associated with deprivation
* Employment and income patterns
* Geographic concentration of vulnerability

---

## Why PySpark?

The project uses PySpark to demonstrate how computational social science workflows can be adapted to a **distributed data-processing environment**.

Rather than simply replacing Pandas with Spark, the project explores concepts relevant to scalable data pipelines, including:

* Distributed DataFrames
* Lazy evaluation
* Transformations and actions
* Distributed aggregations
* Large-scale joins
* Partitioning
* Window operations
* Spark SQL

This provides a practical bridge between **social research and Big Data engineering**.

---

## Analytical Pipeline

```text
Socioeconomic Microdata
          │
          ▼
     Data Ingestion
          │
          ▼
   Data Preprocessing
          │
          ▼
   Feature Engineering
          │
          ▼
 Multidimensional Poverty
       Indicators
          │
          ▼
 Distributed Aggregation
          │
          ▼
 Territorial & Socioeconomic
         Analysis
          │
          ▼
      Insights
```

---

## Expected Outputs

The project produces:

* Processed socioeconomic datasets
* Multidimensional poverty indicators
* Regional aggregations
* Descriptive statistics
* Analytical tables
* Data visualizations

The final analysis aims to identify **where socioeconomic vulnerability is concentrated and which household and territorial characteristics are most strongly associated with multidimensional poverty**.

---

## Research Context

This project builds on my Master's research:

**"Determinants of Multidimensional Poverty in Argentina: A Regional and Intertemporal Perspective with Explainable Artificial Intelligence (2016–2025)."**

The original research combines socioeconomic microdata, machine learning and Explainable AI to study the determinants of multidimensional poverty.

This repository develops a complementary dimension of that work by focusing on **distributed computing and Big Data technologies**.

---

## Author

**Luis Miguel**

Computational Social Data Scientist

**Political Science · International Studies · Computational Social Science**

Interested in the intersection of:

**Social Research · Data Science · Big Data · Machine Learning · Public Policy**

---

## License

This project is intended for research, educational and portfolio purposes.
