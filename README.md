# DEPA Final Project (Fall 2019) - Beer Sales, Preferences, and the Macroeconomy

## 0. Introduction

### 0.1. Executive summary

Alcohol is one of the most popular purchases in the US, but does consumers’ love of beer vary with their economic condition? In this project, we seek to derive insights on alcohol consumption patterns with respect to changes in US economic metrics.

Questions that this project can potentially answer:

- Do preferences for beer types change during recession? Do consumers favor particular beers, price points, or alcohol content?
- How does unemployment affect beer purchasing? Does it significantly impact the total amount purchased, or just shifts the product mix?

### 0.2. Business use case

This project can provide insight into consumer purchasing habits, which is highly desirable to a variety of businesses. Breweries can use this data to plan their production, such that they focus their production on the beer with the highest expected demand. Retailers and restaurants can use this data to plan their inventory, stocking particular products ahead of expected increases in demand.

### 0.3 Methodology

The final product of this project is a collection of Tableau dashboards for data visualization and exploration. To achieve this, upon acquisition of the data from IRI, this project first designs a data warehouse in a local MySQL server for data storage, then uses Python to clean, stage, and import data into MySQL. Next, the local data warehouse is pushed onto an SQL server on Google Cloud Platforms (GCP). Finally, Tableau connects to GCP to perform dataviz tasks.

### 0.4. Data sources

This projects uses the following databases:

- The IRI Academic Marketing Data Set (Bronnenberg, et al, 2012) - 130 GB unzipped - NDA required, accessed through The University of Chicago Office of Research and National Laboratories Research Computing Center
- St. Louis Fed Federal Research Economic Data (FRED) - through FRED API

### 0.5. Prerequisites

System requirements: 50 GB of free drive space. 8 GB memory. MySQL 8.0.18 server, MySQL Workbench 8.0, Jupyter Lab/Notebook.

The MySQL database size will be approximately **17.2 GB**. Check by running the following code in MySQL:  

SELECT table_schema 'database name',  
  sum( data_length + index_length ) / 1024 / 1024 /1024 'data Base Size in GB'  
FROM information_schema.TABLES  
GROUP BY table_schema;

MySQL Workbench DBMS connection read timeout interval to be set at >3600 seconds.

Section 4 requires an empty schema `beer` in MySQL 8. The code is provided in `section 4.0`.

The following packages are also required and can be installed using `pip` or `conda`:  
`os`, `glob` (allows for UNIX-style pathname pattern expansion), `NumPy`, `pandas 0.25` , `sqlalchemy` (writes records stored in a DataFrame to a SQL database), `tqdm` (low overhead iterable progress bar), and `fredapi` (pulls data from St Louis Fed FRED API).

**IMPORTANT**: pandas version `0.24.+` is required as pandas has gained the ability to hold integer dtypes with missing values.

### 0.6. Sections in this notebook

The following sections in this notebook progress as follows:

Section 1 explains the procedure to access the IRI dataset on UChicago Research Computing Center and documents the steps taken to extract the necessary files and directories pertinent to this project, given the limitations of the memory size of personal laptop computers.

Section 2 provides an overview of the IRI dataset and its various dimensions, their limitations.

Section 3 describes the fact-dimension schema in MySQL.

Section 4 contains the code for data intake and manipulation. It also pushes pandas dataframes into an empty MySQL `beer` schema.

---
