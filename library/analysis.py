# -*- coding: utf-8 -*-
import logging
import numpy as np
import pandas as pd

#######################################################################

def _is_date_type(type) -> bool:
    """Checks if the given type is a valid date type
    """

    result = False

    if np.issubdtype(type, np.datetime64):
        result = True

    return result 


#######################################################################

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

def detect_dates_cols(dataframe) -> list:
    """Detects those columns with dates in it and returns their names as a list.
    """

    results = []

    for col in dataframe.columns:

        if _is_date_type(dataframe[col].dtype):

            logging.debug(f"Column: {col} - {dataframe[col].dtype} Type")
            results.append(col)

    return results