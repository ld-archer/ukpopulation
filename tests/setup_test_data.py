#!/usr/bin/env python3

# See ./tests/README.md for important information on testing.

# NOTE: ensure NOMIS_API_KEY=DUMMY in order to match the cached file names for England
import os
import sys

import pandas as pd

import ukpopulation.myedata as MYEData
import ukpopulation.nppdata as NPPData
import ukpopulation.snppdata as SNPPData
import ukpopulation.snhpdata as SNHPData

real_data_dir = "../../cache/"
#test_data_dir = "./tests/raw_data/"
test_data_dir = "./raw_data/"


def setup_snpp_data():
    """
    SNPP test data is 3 LADs per country for years 2018-2031
    """
    raw_files = ["NM_2006_1_449ecf2d283326dfe8f87b5e869a4b5c.tsv",  # England
                 "snpp_w.csv", "snpp_s.csv", "snpp_ni.csv"]

    for file in raw_files:
        sep = "\t" if file[-4:] == ".tsv" else ","
        df = pd.read_csv(real_data_dir + file, sep=sep)

        geogs = df.GEOGRAPHY_CODE.unique()[:3]
        df = df[(df.GEOGRAPHY_CODE.isin(geogs)) & (df.PROJECTED_YEAR_NAME <= 2031)]

        df.to_csv(test_data_dir + file, sep=sep, index=False)

    # NB the file NM_2006_1_d76d72a49d14b5e740ea04a14b741101.tsv also needs to be in the test data folder,
    # containing column headings only. (This will prevent the data being re-downloaded)


def setup_npp_data():
    """
    NPP test data is 3 variants, all ages, for years 2018-2035
    """
    raw_files = ["NM_2009_1_59d6a992314f6af6217f50ae9514e5a5.tsv",  # ppp
                 "npp_hhh.csv", "npp_lll.csv"]

    for file in raw_files:
        sep = "\t" if file[-4:] == ".tsv" else ","
        df = pd.read_csv(real_data_dir + file, sep=sep)
        df = df[(df.PROJECTED_YEAR_NAME < 2036)]
        df.to_csv(test_data_dir + file, sep=sep, index=False)


def fetch_full_data_into_cache():
    npp = NPPData.NPPData()
    npp.force_load_variants(['hhh', 'ppp', 'lll'])
    MYEData.MYEData()
    SNPPData.SNPPData()
    SNHPData.SNHPData()


def fetch_dummy_data_into_raw():
    if not os.environ['NOMIS_API_KEY'] == "DUMMY":
        print("This Function requires to be NOMIS_API_KEY == 'DUMMY' in env.\n"
              "Currently set to {} ".format(os.environ['NOMIS_API_KEY']))
        sys.exit()
    NPPData.NPPData(test_data_dir)
    MYEData.MYEData(test_data_dir)
    SNPPData.SNPPData(test_data_dir)
    SNHPData.SNHPData(test_data_dir)


def main():
    setup_snpp_data()
    setup_npp_data()
    fetch_full_data_into_cache()
    fetch_dummy_data_into_raw()


if __name__ == '__main__':
    main()
