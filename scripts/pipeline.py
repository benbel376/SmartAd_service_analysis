from data_summarizing_functions import DataSummarizer
import os
import sys
import pandas as pd
import numpy as np

# setting path to folders
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
scripts_dir = parent_dir+"/scripts"
data_dir = parent_dir+"/data"
sys.path.insert(1, scripts_dir)


sumar = DataSummarizer()


# function to  clean and save data
def clean__and_save_data(df="/SmartAd_original_data.csv", cdf="/SmartAd_ccclean_data.csv"):
    original_df = pd.read_csv(data_dir+df)
    clean_df = original_df.loc[~(
        (original_df["yes"] == 0) & (original_df["no"] == 0))]
    clean_df.to_csv(data_dir+cdf, index=False)

    return clean_df


# exploring the identity of experiment groups.
def aggregate_exprement_group():
    # Displaying unique values for each categorical variables.

    cleaned_df = clean__and_save_data()
    aggr_df = sumar.find_agg(cleaned_df, ["experiment"], [
                             "auction_id"], ["count"], ["count"])
    aggr_df["percentage"] = (aggr_df["count"]/cleaned_df.shape[0])*100
    return aggr_df


def pipeline(clean, aggregate):
    clean()
    ggg = aggregate()
    print("merber")
