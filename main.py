# -*- coding: utf-8 -*-
import logging
import argparse
import numpy as np
import pandas as pd

import library.UI as UI
import library.database as DB
import library.yamlconfig as YC

#######################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(filename)s - %(levelname)s - %(message)s')

SETUP_PROFILE = "User1"
DB_FILE = "consolidated_data"

DEBUG=True

#######################################################################

if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description='Process a CSV file with ' \
    #     + 'bank account movements')
    # parser.add_argument('--file', default=None,
    #                     help='CSV File to process')
    # args = parser.parse_args()
    # if not args.file:
    #     parser.print_help()
    #     exit(1)
    # logging.info(f"File path: {args.file}")

    # print(f"1. Loading file...")
    # movements = processes.load_movements(args.file)
    
    # print(f"2. Recognise movements and wealth columns...")
    # mov_col, wea_col = analysis.detect_money_cols(movements)
    # print(f"\tMovements column: {mov_col}")
    # print(f"\tWealth column: {wea_col}")
    
    # print(f"3. Recognise dates columns...")
    # date_cols = analysis.detect_dates_cols(movements)
    # print(f"\tColumns: {date_cols}")

    configuration = YC.load_config(SETUP_PROFILE)

    UI.menu(configuration)

    YC.save_config(SETUP_PROFILE, configuration)