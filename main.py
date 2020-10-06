# -*- coding: utf-8 -*-
import logging
import argparse
import numpy as np
import pandas as pd

import library.UI as UI
import library.analysis as analysis
import library.yamlconfig as YC
import library.database as DB

#######################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

SETUP_PROFILE = "User1"
DB_FILE = "consolidated_data"

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

    con = DB.open_database(DB_FILE)

    res = DB._execute_reader_query(con, "SELECT ID, OP_DATE, VAL_DATE, CONCEPT, AMOUNT, BALANCE from all_movements")
    print(f"Reads result: {len(res)}")
    for item in res:
        print(item)
    res = DB._execute_non_reader_query(con, "INSERT INTO all_movements(OP_DATE, VAL_DATE, CONCEPT, AMOUNT, BALANCE) VALUES (\"2020-20-06\",\"2020-20-06\", \"Concepto prueba jeje\", 50, 50)")
    print("Insert result: ")
    print(res)
    res = DB._execute_reader_query(con, "SELECT ID, OP_DATE, VAL_DATE, CONCEPT, AMOUNT, BALANCE from all_movements")
    print(f"Reads result: {len(res)}")
    for item in res:
        print(item)

    DB.close_database(con)

    # UI.menu()