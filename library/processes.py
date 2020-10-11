# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd

#######################################################################

def _ask_bool_user(msg) -> bool:
    """Ask anything to the user and returns a boolean
    """

    result = False
    try:
        
        option = input(f"Do you want {msg}? (Y/N): ")
        if option.lower() == "y":
            result = True
            
    except ValueError as e:
        print(f"Error! {e}")

    return result

def _ask_str_user(msg) -> str:
    """Ask anything to the user and returns the answer
    """

    result = input(f"{msg}: ")

    return result

def _load_movements(filepath, col_limit=5) -> pd.DataFrame:
    """Reads a CSV file with bank account movements and returns a pandas
    Dataframe.

    + First two columns will be tried to be parsed as dates.
    + Sepatator is `;`
    + Decimal separator is `,`
    + Expected encoding is `utf-8`
    + Only takes up to the column limit specified to avoid garbage data.

    FP: Non-pure function
    """

    moves = pd.read_csv(filepath,
                        sep=";",
                        decimal=",",
                        thousands=".",
                        header="infer",
                        parse_dates=[0,1],
                        infer_datetime_format=True,
                        #encoding="iso-8859-1")
                        encoding="utf-8")

    logging.debug(f"Removing unnecesary columns...")
    moves = moves.iloc[:, 0:col_limit]

    return moves

#######################################################################

def load_data():
    """Loads new data to the consolidated system.

    1. Asks the user for the file to load
    2. Loads it, removing garbage from an specific column onwards
    3. Saves it to the consolidated data (TO-DO)
    """

    data = None
    filepath = _ask_str_user("Please, insert the path to the file to load")
    logging.info(f"File path: {filepath}")

    if os.path.isfile(filepath):
        logging.info(f"Loading file data...")
        data = _load_movements(filepath)

    if len(data) < 1:
        logging.warning(f"File did not exist or did not contain valid data!")
    else:
        logging.warning(f"Consolidate data is not still implemented")
        print(data)


#######################################################################