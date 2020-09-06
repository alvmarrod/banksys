
import logging
import numpy as np
import pandas as pd

def load_movements(filepath) -> pd.DataFrame:
    """Reads a CSV file with bank account movements and returns a pandas
    Dataframe.

    + First two columns will be tried to be parsed as dates.
    + Sepatator is `;`
    + Decimal separator is `,`
    + Expected encoding is `Latin-1`

    FP: Non-pure function
    """

    return pd.read_csv(filepath,
                        sep=";",
                        decimal=",",
                        thousands=".",
                        header="infer",
                        parse_dates=[0,1],
                        infer_datetime_format=True,
                        encoding="iso-8859-1")

def detect_money_cols(dataframe) -> (str, str):
    """Detects the movement and wealth column names by looking for both
    positive and negative values in it.

    If serveral have the negative values, the one with the maximum positive
    value stands as result, since accumulated wealth should be the available
    money and therefore higher than just money movements.
    """

    mov = None
    wea = None
    candidates = {}

    for col in dataframe.columns:

        logging.debug(f"Column: {col} - {dataframe[col].dtype} Type")

        if np.issubdtype(dataframe[col].dtype, np.number):

            candidates[col] = {
                "min": dataframe[col].min(),
                "max": dataframe[col].max(),
            }

            if not mov:
                mov = col
            else:
                if dataframe[col].min() < candidates[mov]["min"]:
                    mov = col

            if not wea:
                wea = col
            else:
                if dataframe[col].max() > candidates[wea]["max"]:
                    wea = col            

    return mov, wea
