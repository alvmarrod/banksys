
import logging
import argparse
import numpy as np
import pandas as pd

import library.analysis as analysis

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a CSV file with ' \
        + 'bank account movements')

    parser.add_argument('--file', default=None,
                        help='CSV File to process')

    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        exit(1)

    logging.info(f"File path: {args.file}")

    print(f"1. Loading file...")
    movements = analysis.load_movements(args.file)

    print(f"2. Removing unnecesary columns...")
    movements = movements.iloc[:, 0:5]
    
    print(f"3. ...")
    #print(movements.dtypes)
    #print(movements.describe)
