# -*- coding: utf-8 -*-
import logging
import sqlite3

#######################################################################

def _split_query_result(row, sep=",", quot="\""):
    """Splits the given string by separator symbol, taking into account
    the quote symbol.
    """

    # TODO
    pass

#######################################################################

def _create_all_movements_table(con):
    """Creates the table for consolidated data. This function is
    idempotent, so it will not overwrite an existing config file.
    """

    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' " + \
                "AND name='all_movements'"

    if not con.execute(tb_exists).fetchone():

        logging.info("Table all_movements not detected!")

        con.execute('''CREATE TABLE all_movements
            (ID INTEGER PRIMARY KEY,
            OP_DATE        TEXT    NOT NULL,
            VAL_DATE       TEXT    NOT NULL,
            CONCEPT        TEXT    NULL,
            AMOUNT         REAL,
            BALANCE        REAL);''')

        logging.info("Table all_movements created!")

#######################################################################

def _execute_non_reader_query(con, query) -> int:
    """Execute a non-reader query that returns a `int` value indicating
    if the execution was successful.

    If the command executed was an `update`, then the returned value
    indicates the number of rows that have been updated.
    """

    result = 0
    cursor = con.execute(query)

    commit_commands = [
        "insert",
        "update",
        "delete"
    ]

    if query.split(" ")[0].lower() in commit_commands:
        con.commit()

    if query.split(" ")[0].lower() == "update":
        result = con.total_changes

    return result

def _execute_reader_query(con, query) -> list:
    """Execute a reader query that returns a `list` with the query
    response.
    """

    cursor = con.execute(query)
    rows = cursor.fetchall()

    return rows


#######################################################################

def open_database(db_file) -> sqlite3.Connection:
    """Open the specified file as a sqlite3 database file.

    Parameters:
    - A `str` with the filename of the database without extension

    Returns:
    - A `sqlite3.Connection` with the connection for the database
    """

    filepath = f"./data/{db_file}.db"
    con = None

    try:
        con = sqlite3.connect(filepath)
        _create_all_movements_table(con)

    except Exception as e:

        logging.warning("Couldn't connect to the specified database" + \
                        f" \"{db_file}\"")
        logging.info(e)

    return con

def close_database(con):
    """Close the given database connection

    Parameters:
    - A `sqlite3.Connection` to be closed
    """

    try:
        con.close()

    except Exception as e:

        logging.warning("Couldn't close the specified database" + \
                        " \"{db_file}\"")
        logging.info(e)