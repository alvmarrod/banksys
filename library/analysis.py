
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

