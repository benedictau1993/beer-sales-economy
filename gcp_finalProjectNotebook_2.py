#!/usr/bin/env python
# coding: utf-8

# # Beer Sales, Preferences, and the Macroeconomy
# ### Data Engineering Platforms (Fall 2019) | The University of Chicago
# finalProjectNotebook_cloud_2.py
# Takes clustered columns, cleans the data, and pushes to local MySQL server.

## Create schema in MySQL server
# In MySQL Workbench, create the schema/EER the `beer` database on a local MySQL server using the DDL script `beer_ddl.sql`.
# Note: When populating the database with data, it is **paramount** that the data for the tips of the snowflake is inputted first, and the fact tables (`sales`) and `econ` be inserted last. Otherwise, it would throw a `FOREIGN_KEY_CHECKS` error (ERROR 1452: Cannot add or update a child row: a foreign key constraint fails).
# Note note: For each instance a MySQL table is populated, there will be a binary log generated. Since the SALES data is large, the corresponding binary log will also be large, taking up space in your storage up to 5GB at a time. To purge the binary logs, use the script `PURGE BINARY LOGS BEFORE '<DATETIME>';`.


# run with `python3`, not `python`. The latter will bring up Python2

import os
import glob
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import time
from fredapi import Fred
# import mysqlclient

# MySQL server credentials
engine = create_engine("mysql+pymysql://{user}:{pw}@{public_ip}/{db}".format(user="root", pw="rootroot", public_ip = "35.226.184.202", "db="beer"))

# To GCP Cloud SQL DB `depa-cloud-beer2`
# Need to add public IP using GCloud somehow...

# We read in the product table:
prod_all_beer_df = pd.concat([pd.read_excel(f) for f in glob.glob("./IRI BEER DATASET/beer_attributes/prod*_beer.xls*")], ignore_index = True, sort=False)
prod_all_beer_df["FLAVOR/SCENT"] = prod_all_beer_df["FLAVOR/SCENT"].replace("MISSING", "NO FLAVOR").replace("REGULAR", "NO FLAVOR")
prod_all_beer_df["PACKAGE"] = prod_all_beer_df["PACKAGE"].replace("MISSING", "UNKNOWN")
prod_all_beer_df["TYPE OF BEER/ALE"] = prod_all_beer_df["TYPE OF BEER/ALE"].replace("MISSING", "BEER")

# Normalisation
# Unique flavors
flavor_df = pd.read_csv("./OpenRefine_data/post-openrefine/flavor-or.csv")
flavor_df = flavor_df.assign(flavor_id = flavor_df["flavor_cat"].astype('category').cat.codes).sort_values(by=['flavor_id'])
flavor_df.reset_index(drop=True, inplace=True)
flavor_dict = flavor_df.set_index("flavor_name")["flavor_id"].to_dict()

# Unique packaging
packaging_df = pd.read_csv("./OpenRefine_data/post-openrefine/packaging-or.csv")
packaging_df = packaging_df.assign(packaging_id = packaging_df["packaging_cat"].astype('category').cat.codes).sort_values(by=['packaging_id'])
packaging_df.reset_index(drop=True, inplace=True)
packaging_dict = packaging_df.set_index("packaging_name")["packaging_id"].to_dict()

# Unique beer_type
beer_type_df = pd.read_csv("./OpenRefine_data/post-openrefine/beer_type-or.csv")
beer_type_df = beer_type_df.assign(beer_type_id = beer_type_df["beer_type_cat"].astype('category').cat.codes).sort_values(by=['beer_type_id'])
beer_type_df.reset_index(drop=True, inplace=True)
beer_type_dict = beer_type_df.set_index("beer_type_name")["beer_type_id"].to_dict()

# Unique vendor
vendor_df = prod_all_beer_df[["L4"]].replace("MISSING", np.nan).replace("ALL OTHERS", np.nan).replace("PRIVATE LABEL", np.nan).dropna().drop_duplicates()
vendor_df.rename(columns={"L4": "vendor_name"}, inplace=True)
vendor_df["vendor_id"] = np.arange(1,1+len(vendor_df))
vendor_df.reset_index(drop=True, inplace=True)
vendor_dict = vendor_df.set_index("vendor_name")["vendor_id"].to_dict()

# A dataframe of unique products (defined by UPC codes) is created.
prod_all_beer_unique_df = prod_all_beer_df.drop_duplicates(subset="UPC")
prod_all_beer_unique_df = prod_all_beer_unique_df[prod_all_beer_unique_df.L4 != "ALL OTHERS"]
prod_all_beer_unique_df = prod_all_beer_unique_df[prod_all_beer_unique_df.L4 != "PRIVATE LABEL"]
prod_all_beer_unique_df["domestic"] = [1 if x == "DOMESTIC BEER/ALE (INC NON-ALCOH" else 0 for x in prod_all_beer_unique_df["L2"]]
prod_all_beer_unique_df = prod_all_beer_unique_df[["UPC", "SY", "GE", "VEND", "ITEM", "domestic", "L4", "VOL_EQ", "TYPE OF BEER/ALE", "PACKAGE", "FLAVOR/SCENT"]]
prod_all_beer_unique_df.rename(columns={"L4": "vendor_id", "TYPE OF BEER/ALE": "beer_type_id", "PACKAGE": "packaging_id", "FLAVOR/SCENT": "flavor_id"}, inplace=True)

prod_all_beer_unique_df["vendor_id"] = prod_all_beer_unique_df["vendor_id"].map(vendor_dict)
prod_all_beer_unique_df["beer_type_id"] = prod_all_beer_unique_df["beer_type_id"].map(beer_type_dict)
prod_all_beer_unique_df["beer_type_id"] = prod_all_beer_unique_df["beer_type_id"].astype('Int64')
prod_all_beer_unique_df["packaging_id"] = prod_all_beer_unique_df["packaging_id"].map(packaging_dict)
prod_all_beer_unique_df["packaging_id"] = prod_all_beer_unique_df["packaging_id"].astype('Int64')
prod_all_beer_unique_df["flavor_id"] = prod_all_beer_unique_df["flavor_id"].map(flavor_dict)
prod_all_beer_unique_df["flavor_id"] = prod_all_beer_unique_df["flavor_id"].astype('Int64')

prod_all_beer_unique_df.reset_index(drop=True, inplace=True)
prod_all_beer_unique_df["UPC_id"] = np.arange(1,1+len(prod_all_beer_unique_df))
prod_all_beer_unique_df.reset_index(drop=True, inplace=True)
prod_all_beer_unique_df["total_vol_oz"] = (prod_all_beer_unique_df["VOL_EQ"]*192).round()

# UPC codes in `sales` tables are atomized with no leading zeros.
# Will need to normalise sales tables by replacing atomized UPC codes by surrogate UPC_id codes instead.
# Can't use UPC column in `prod_all_beer_unique_df` to make dictionary since values have leading zeros.
# Create df by concat-ing "SY", "GE", "VEND", "ITEM" columns with dash as separator.
# Create dict for use later.
atom_upc_upcid_df = prod_all_beer_unique_df[["UPC_id", "SY", "GE", "VEND", "ITEM"]]
concat_upc_atom = atom_upc_upcid_df[["SY", "GE", "VEND", "ITEM"]].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
atom_upc_upcid_df = pd.concat([atom_upc_upcid_df, concat_upc_atom], axis=1)
atom_upc_upcid_df.drop(["SY", "GE", "VEND", "ITEM"], axis = 1, inplace=True)
atom_upc_upcid_df.rename(columns = {0: "UPC_atom_concat"}, inplace=True)
atom_upc_upcid_dict = atom_upc_upcid_df.set_index("UPC_atom_concat")["UPC_id"].to_dict()

# Push to MySQL server
# Before doing so, keep only unique categories and ID.
flavor_df.drop(["flavor_name"],axis=1, inplace=True)
flavor_df.drop_duplicates(inplace=True)
flavor_df.to_sql('flavor', con = engine, if_exists = 'append', chunksize = 1000, index = False)

packaging_df.drop(["packaging_name"],axis=1, inplace=True)
packaging_df.drop_duplicates(inplace=True)
packaging_df.to_sql('packaging', con = engine, if_exists = 'append', chunksize = 1000, index = False)

beer_type_df.drop(["beer_type_name"],axis=1, inplace=True)
beer_type_df.drop_duplicates(inplace=True)
beer_type_df.to_sql('beer_type', con = engine, if_exists = 'append', chunksize = 1000, index = False)

vendor_df.to_sql('vendor', con = engine, if_exists = 'append', chunksize = 1000, index = False)

prod_all_beer_unique_df.to_sql('upc', con = engine, if_exists = 'append', chunksize = 1000, index = False)


# We read in the store (Delivery_Stores) tables table:
stores_all_df = pd.concat([pd.read_csv(f, sep="\t") for f in glob.glob("./IRI BEER DATASET/Year*/Delivery_Stores")], ignore_index = True, sort=False)
stores_all_df.columns = ["string"]

# The store data is vertically aligned but not tab-separated, so it is read into a dataframe as a string. Attributes are manually extracted:
# Split column by character location
stores_all_df["store_id"] = stores_all_df.string.str[0:7].astype(str).astype(int)
stores_all_df["outlet_cat_name"] = stores_all_df.string.str[8:10]
stores_all_df["market_name"] = stores_all_df.string.str[20:45]
stores_all_df["market_name"] = stores_all_df["market_name"].apply(lambda x: x.strip())

outlet_cat_convert_dict = {"DR": "drug", "GR": "groceries", "MA": "mass", "DK": "drug", "GK": "groceries", "MK": "mass"}
stores_all_df["outlet_cat_name"] = stores_all_df["outlet_cat_name"].map(outlet_cat_convert_dict)
stores_all_df.drop(["string"], axis = 1, inplace=True)
stores_all_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stores_all_df.drop_duplicates(subset="store_id", inplace=True)

# Normalisation
# Unique outlet_cat
outlet_cat_df = stores_all_df[["outlet_cat_name"]].drop_duplicates()
outlet_cat_df["outlet_cat_id"] = np.arange(1,1+len(outlet_cat_df))
outlet_cat_df.reset_index(drop=True, inplace=True)
outlet_cat_dict = outlet_cat_df.set_index("outlet_cat_name")["outlet_cat_id"].to_dict()

# Unique market
market_df  = pd.read_csv("./OpenRefine_data/post-openrefine/market-or.csv")
market_dict = market_df.set_index("market_name")["market_id"].to_dict()

stores_all_df["outlet_cat_name"] = stores_all_df["outlet_cat_name"].map(outlet_cat_dict)
stores_all_df["market_name"] = stores_all_df["market_name"].map(market_dict)
stores_all_df.rename(columns = {"outlet_cat_name": "outlet_cat_id", "market_name": "market_id"}, inplace=True)
stores_all_df.reset_index(drop=True, inplace=True)
stores_all_df.tail()

# Push to MySQL server
outlet_cat_df.to_sql('outlet_cat', con = engine, if_exists = 'append', chunksize = 1000, index = False)
market_df.to_sql('market', con = engine, if_exists = 'append', chunksize = 1000, index = False)
stores_all_df.to_sql('store', con = engine, if_exists = 'append', chunksize = 1000, index = False)


# Create week table
# Create a week table to convert IRI week codes to calendar date, refers to the Sunday of each week.
week_index = pd.date_range(start='12/30/2000', end='01/01/2013', freq='W-MON')
week_df = week_index.to_frame(index=False)
week_df.columns = ["date"]
week_df["week_id"] = np.arange(1114,1114+len(week_df))
week_df.shape

# Import into MySQL server
week_df.to_sql('week', con = engine, if_exists = 'append', chunksize = 1000, index = False)


# We read in the sales tables:
# Sales data are stored in `YearXX` directories with the naming convention: `beer_<OUTLET_CAT>_<START_WEEKID>_<END_WEEK_ID>`.
# List of all sales data and total size
sales_file_list = glob.glob("./IRI BEER DATASET/Year*/beer_????_????_????")
sales_files_size_GB = round(sum([os.stat(file).st_size for file in sales_file_list])/(1024**3),2)
print("There are", len(sales_file_list), "files and the total size of sales data is", sales_files_size_GB, "GB.")

# Since files are big but each file has the same spacing format, for each sales file:
# 1. `read_table()` into dataframe
# 2. Split string into columns by character position (IRI_KEY, WEEK, SY, GE, VEND, ITEM, UNITS, DOLLARS)
# 3. Push to mySQL by `if_exists = 'append'` method
#
# Estimated time for manipulating and importing sales data: 120 minutes. System: macOS 10.15.1, Intel 7th gen Core i5 (I5-7267U), 8GB memory, Iris Plus Graphics 650.

for series in tqdm(sales_file_list):
    sales_each_df = pd.read_csv(series, sep="\t")
    sales_each_df.columns = ["string"]
    sales_each_df.tail()

    # split string into columns
    sales_each_df["store_id"] = sales_each_df.string.str[0:7].astype(str).astype(int)
    sales_each_df["week_id"] = sales_each_df.string.str[8:12].astype(str).astype(int)
    sales_each_df["SY"] = sales_each_df.string.str[13:15].astype(str).astype(int)
    sales_each_df["GE"] = sales_each_df.string.str[16:18].astype(str).astype(int)
    sales_each_df["VEND"] = sales_each_df.string.str[19:24].astype(str).astype(int)
    sales_each_df["ITEM"] = sales_each_df.string.str[25:30].astype(str).astype(int)
    sales_each_df["UNITS"] = sales_each_df.string.str[31:36].astype(str).astype(int)
    sales_each_df["DOLLARS"] = sales_each_df.string.str[37:45].astype(str).astype(float)
    sales_each_df.drop(["string"], axis = 1, inplace=True)
    sales_each_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    concat_upc_atom = sales_each_df[["SY", "GE", "VEND", "ITEM"]].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
    sales_each_df = pd.concat([sales_each_df, concat_upc_atom], axis=1)
    sales_each_df.drop(["SY", "GE", "VEND", "ITEM"], axis = 1, inplace=True)
    sales_each_df.rename(columns = {0: "UPC_atom_concat"}, inplace=True)
    sales_each_df["upc_id"] = sales_each_df["UPC_atom_concat"].map(atom_upc_upcid_dict)
    # sales_each_df[sales_each_df.isna().any(axis=1)]
    # UPC code 0-1-11170-83511 does not exist in any of the `prod*_beer.xls*` tables so it's being dropped
    sales_each_df.dropna(inplace = True)
    sales_each_df.drop(["UPC_atom_concat"], axis = 1, inplace=True)
    sales_each_df["upc_id"] = sales_each_df["upc_id"].astype('Int64')

    # dump into MySQL
    #sales_each_df.to_sql('sales', con = engine, if_exists = 'append', chunksize = 1000, index = False)
    sales_each_df.to_sql('sales', con = engine, if_exists = 'append', chunksize = 1000, index = False)


# We pull FRED economic data. #
# FRED API documentation: [https://research.stlouisfed.org/docs/api/fred/ ]
# State abbreviations data
# **[IMPORTANT]** Downloaded from: http://www.whypad.com/wp-content/uploads/us_states.zip and placed in notebook directory.
state_code_df = pd.read_csv("us_states.csv")
state_code_df.columns = ["STATE", "state", "state_abbrev"]
state_code_df.drop(["STATE"], axis = 1, inplace=True)
state_code_df.head()


# ### 9.2. FRED economic data
#
# JSON Request (HTTPS GET) example:
# https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key=85482ff982c94bb52ca2ae28568ee970&file_type=json&observation_start=2001-01-01&observation_end=2012-12-31
# API key: 85482ff982c94bb52ca2ae28568ee970
#
# series_id's:#
# Real Gross Domestic Product: `GDPC1`
# State unemployment rate: `state_code` + `UR`; use state abbreviations dataframe from section `4.5.1`
# CPI (for All Urban Consumers: All Items in U.S. City Average): `CPIAUCSL`
# Long-Term Government Bond Yields: 10-year: Main (Including Benchmark): `IRLTLT01USM156N`
# S&P/Case-Shiller U.S. National Home Price Index: `CSUSHPISA`
# NBER based Recession Indicator: `USRECP`
#
# We form the list of economic series to pull from FRED:
us_unemploy_api = ["UNRATE"]
state_unemploy_api_list = state_code_df['state_abbrev'].astype(str) + "UR"
state_unemploy_api_list = state_unemploy_api_list.tolist()
all_unemploy_api = us_unemploy_api + state_unemploy_api_list
other_api_list = ["IRLTLT01USM156N", "CSUSHPISA", "GDPC1", "CPIAUCSL", "USRECP"]
all_api = other_api_list + all_unemploy_api

# Upon setting up the API credentials, we pull data from FRED and nest it in DICTIONARY with format `{series_id : series_data_df}`. A dictionary is much preferred to dynamically creating objects through a loop since they are unnecessary, hard to create (use exec or globals()), and I can't use them dynamically anyway. But if you really want to, use `globals()`.
#
# Sometimes the API reaches 504 Gateway Timeout error and yells at you. Just keep trying:
api_key = "85482ff982c94bb52ca2ae28568ee970"
fred = Fred(api_key=api_key)
dict_series_values = {series: fred.get_series_latest_release(series).to_frame() for series in all_api}
# We clean the dataframes and drop all observations that are not between 2001 and 2012:
for series, df in dict_series_values.items():
    df.columns = [series]
    df.reset_index(level=0, inplace=True)
    df.rename(columns={"index": "date"}, inplace = True)
    pd.to_datetime(df['date'], format = "%Y-%m-%d")
    dict_series_values[series] = df.loc[(df['date'] >= "2001-01-01") & (df['date'] <= "2012-12-31")]

econ_df = pd.concat([df.set_index('date') for (series, df) in dict_series_values.items()], axis=1, join='outer').reset_index()

# Merge IRI week number ID's with economic dataframe
econ_df = pd.merge_asof(econ_df, week_df, direction='nearest')
econ_df.rename(columns={"week_id": "econ_week_id"}, inplace = True)

# Import into MySQL server
econ_df.to_sql('econ', con = engine, if_exists = 'append', chunksize = 1000, index = False)


# Integration with Google Cloud Platforms and Google Cloud SQL Server
# Create database dump file with `mysqldump`:
get_ipython().system('mysqldump --databases beer -h 127.0.0.1 -uroot -p --hex-blob --skip-triggers --single-transaction --set-gtid-purged=OFF --default-character-set=utf8mb4 > beer_dump.sql`')

# End
