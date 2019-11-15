#!/usr/bin/env python
# coding: utf-8

# # Beer Sales, Preferences, and the Macroeconomy
# ### Data Engineering Platforms (Fall 2019) | The University of Chicago
# finalProjectNotebook_cloud_1.py
# Extracts all columns that require clustering/manual manipulation. 

import os
import glob
import numpy as np
import pandas as pd

# We read in the product table:
prod_all_beer_df = pd.concat([pd.read_excel(f) for f in glob.glob("./IRI BEER DATASET/beer_attributes/prod*_beer.xls*")], ignore_index = True, sort=False)
prod_all_beer_df["FLAVOR/SCENT"] = prod_all_beer_df["FLAVOR/SCENT"].replace("MISSING", "NO FLAVOR").replace("REGULAR", "NO FLAVOR")
prod_all_beer_df["PACKAGE"] = prod_all_beer_df["PACKAGE"].replace("MISSING", "UNKNOWN")
prod_all_beer_df["TYPE OF BEER/ALE"] = prod_all_beer_df["TYPE OF BEER/ALE"].replace("MISSING", "BEER")
prod_all_beer_df.head()

# Extract columns for clustering in OpenRefine:
# Unique flavors
flavor_df = prod_all_beer_df[["FLAVOR/SCENT"]].dropna().drop_duplicates()
flavor_df.rename(columns={"FLAVOR/SCENT": "flavor_name"}, inplace=True)
flavor_df["flavor_cat"] = flavor_df["flavor_name"]
flavor_df.reset_index(drop=True, inplace=True)
flavor_df.to_csv("./OpenRefine_data/pre-openrefine/flavor.csv", index=False)

# Unique packaging
packaging_df = prod_all_beer_df[["PACKAGE"]].dropna().drop_duplicates()
packaging_df.rename(columns={"PACKAGE": "packaging_name"}, inplace=True)
packaging_df["packaging_cat"] = packaging_df["packaging_name"]
packaging_df.reset_index(drop=True, inplace=True)
packaging_df.to_csv("./OpenRefine_data/pre-openrefine/packaging.csv", index=False)

# Unique beer_type
beer_type_df = prod_all_beer_df[["TYPE OF BEER/ALE"]].dropna().drop_duplicates()
beer_type_df.rename(columns={"TYPE OF BEER/ALE": "beer_type_name"}, inplace=True)
beer_type_df["beer_type_cat"] = beer_type_df["beer_type_name"]
beer_type_df.reset_index(drop=True, inplace=True)
beer_type_df.to_csv("./OpenRefine_data/pre-openrefine/beer_type.csv", index=False)

# # We read in the store (Delivery_Stores) tables table:
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

# Extract market column for edits in Excel:
# Unique market
market_df = stores_all_df[["market_name"]].drop_duplicates()
market_df["market_id"] = np.arange(1,1+len(market_df))
market_df.reset_index(drop=True, inplace=True)
market_df.to_csv("./OpenRefine_data/pre-openrefine/market.csv", index=False)

# End
