# -*- coding: utf-8 -*-
import logging
import pandas as pd

#######################################################################

def load_movements(filepath, col_limit=5) -> pd.DataFrame:
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

