# Beer Sales, Preferences, and the Macroeconomy
### Data Engineering Platforms (Fall 2019) | The University of Chicago

## 0. Introduction

### 0.1. Executive summary

Alcohol is one of the most popular purchases in the US, but does consumers’ love of beer vary with their economic condition? In this project, we seek to derive insights on alcohol consumption patterns with respect to changes in US economic metrics. 

Questions that this project can potentially answer:

- Do preferences for beer types change during recession? Do consumers favor particular beers, price points, or alcohol content?
- How does unemployment affect beer purchasing? Does it significantly impact the total amount purchased, or just shifts the product mix?

### 0.2. Business use case

This project can provide insight into consumer purchasing habits, which is highly desirable to a variety of businesses. Breweries can use this data to plan their production, such that they focus their production on the beer with the highest expected demand. Retailers and restaurants can use this data to plan their inventory, stocking particular products ahead of expected increases in demand.

### 0.3. Methodology

The order of operation is as follows: First, the schema (snowflake EER) of the final MySQL database is designed upon examining the data.  The relevant data from the IRI dataset are combined in groups and read into dataframes in Python. Text columns that appear to be non-categorical are clustered in OpenRefine. The clustered results then are used as a dictionary to normalise said dataframes. The dataframes are then read into a local MySWL server, then upon verification is migrated to Google Cloud SQL. This then allows data access for analysis and visualisation by various stakeholders using Python, R, and Tableau. 

### 0.4. Data sources

- The IRI Academic Marketing Data Set (Bronnenberg, et al, 2012) - 130 GB unzipped - NDA required, access through The University of Chicago Office of Research and National Laboratories Research Computing Center 
- St. Louis Fed Federal Research Economic Data (FRED) - through FRED API

### 0.5 Prerequisites

System requirements: 50 GB of free drive space. 8 GB memory. Jupyter Lab/Notebook, OpenRefine 3.2, MySQL 8.0.18 server, MySQL Workbench 8.0, Google Cloud Platform, Cloud SQL, and Tableau.

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

Section 4 includes the code to create an blank schema on a local MySQL server.

Section 5-9 works with import, transformation, normalisation, and pushing data (product, store, sales, dates, and economic data) onto the local MySQL server. 

Section 10 details the steps taken to migrate the database from local server to Google Cloud SQL. 

Section 11 gives a quick run-down of Cloud SQL access for data visualisation and analysis in Tableau.

---