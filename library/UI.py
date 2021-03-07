# -*- coding: utf-8 -*-
import os
import logging
import platform

import library.analysis as analysis
import library.processes as processes

if "banksys" in __name__:
    import banksys.main as main
else:
    import main as main

PLATFORM = platform.system().lower()
CLEAN_CMD = "cls" if "win" in PLATFORM else "clear"

def _ask_bool_user(msg, default=False) -> bool:
    """Ask anything to the user and returns a boolean.

    If the pattern is not followed, returns false.
    """

    result = default
    try:
        
        option = input(f"{msg} (Y/N): ")
        if option.lower() == "y":
            result = True
        elif option.lower() == "n":
            result = False
            
    except ValueError as e:
        print(f"Error! {e}")

    return result

def _ask_str_user(msg, default="") -> str:
    """Ask anything to the user and returns the answer
    """

    result = input(f"{msg}: ")
    if len(result) == 0:
        result = default

    return result

def _ask_int_user(msg, default=0) -> int:
    """Ask anything to the user and returns an int.
    """

    result = default
    try:
        
        option = input(f"{msg}: ")
        result = int(option)
            
    except ValueError as e:
        print(f"Error! {e}")

    return result

def _ask_loop(asktype, msg, default_value, failcheck, checkparameters=None):
    """Handles asking to the user several times until the desired value
    to be used is agreed.

    A fail check function can be provided to run over the given result,
    which will be passed as parameter to it. A tuple with parameters can
    be provided to feed that function, where the result from the input
    will be appended.
    
    If the failcheck returns `true`, it will trigger a rollback to the
    `default_value` given.
    """

    result = None
    again = True
    function = None

    if "str" == asktype.lower():
        function = _ask_str_user
    elif "bool" == asktype.lower():
        function = _ask_bool_user
    elif "int" == asktype.lower():
        function = _ask_int_user

    if function:

        while again == True:

            result = function(msg, default=default_value)

            parameters = (*checkparameters, result)
            #from IPython import embed
            #embed()
            if failcheck(*parameters):

                result = default_value
                print(f"Error! {parameters[-1]} value is not correct." + \
                        " Rolling back...")

            else:
                
                if result != default_value:
                    ask_again = f"Input given is \"{result}\", do you agree?"
                    again = _ask_bool_user(ask_again)
                else:
                    again = False

    return result

def _ask_back_to_menu() -> bool:
    """Checks if the user wants to go back to the menu
    """

    result = False

    try:
        
        option = input("Do you want to go back to menu? (Y/N): ")
        
        if option.lower() == "y":
            result = True
            
    except ValueError as e:
        print(f"Error! {e}")

    return result

def _menu_generation(configuration=None) -> bool:
    """Generates the menu options. If returns false means the
    menu should be finished
    """

    show_again = False

    options = {
        1: {
            "text": "See report",
            "function": None
        },
        2: {
            "text": "Load new movements",
            "function": run_load_data
        },
        3: {
            "text": "Manual analysis",
            "function": None
        },
        4: {
            "text": "Remove database",
            "function": None
        },
        5: {
            "text": "Exit",
            "function": exit
        }
    }

    if not main.DEBUG:
        os.system(CLEAN_CMD)

    print("############### banksys ###############")
    print("####                               ####")

    lon = len("############### banksys ###############")
    for i in range(1, len(options)+1):
        opt = f'# {i}. {options[i]["text"]}'
        if len(opt) < lon:
            opt += " " * (lon-(len(opt)+1)) + "#"
        print(opt)

    print("####                               ####")
    print("#######################################")

    print("")

    try:

        option = int(input("Choose an option: "))

        if option <= 0 or option > len(options):
            raise ValueError("Option number not recognised")

        show_again = True

        if options[option]["function"]:
            options[option]["function"](configuration)
        else:
            raise ValueError(f"Option {option} is not available!")

    except ValueError as e:

        print(f"Error! {e}\n")

    if not _ask_back_to_menu():
        show_again = False
    
    return show_again

#######################################################################

def run_load_data(configuration):
    """Manages the data adquisition from the user to run the load data
    process.
    """

    profile = configuration["profile"]

    filepath = _ask_str_user("Please, insert the path to the file to load")
    logging.info(f"File path: {filepath}")

    logging.info("Loading movements from CSV...")
    moves = processes.load_movements(filepath)

    logging.info("Recognising column types on import...")
    mov_col, wea_col = analysis.detect_money_cols(moves)
    date_cols = analysis.detect_dates_cols(moves)

    logging.debug("Recognised:")
    logging.debug(f"\tColumn {mov_col} is the amount column")
    logging.debug(f"\tColumn {wea_col} is the balance column")

    if profile["load"]["wealth"] == str(wea_col) and \
        profile["load"]["movements"] == str(mov_col):
        logging.info(f"Match with stored configuration. Importing directly...")

    else:

        mov_col_ask = f"Please, confirm that you want to use column " \
                    + f"\"{mov_col}\" as moves column, or change it"
        checkparams = [moves]
        mov_col = _ask_loop("str", mov_col_ask, mov_col,
                            analysis.column_filter, checkparameters=checkparams)

        logging.debug(f"Ok, using column \"{mov_col}\"")

        wea_col_ask = f"Please, confirm that you want to use column " \
                    + f"\"{wea_col}\" as balance column, or change it"
        checkparams = [moves]
        wea_col = _ask_loop("str", wea_col_ask, wea_col,
                            analysis.column_filter, checkparameters=checkparams)
        logging.debug(f"Ok, using column \"{wea_col}\"")

        save_setup_ask = "Do you want to save these column names as default" \
                    + " for future imports"
        if _ask_bool_user(save_setup_ask):
            profile["load"]["wealth"] = wea_col
            profile["load"]["movements"] = mov_col

    logging.debug(f"\tColumns: {date_cols} are dates")
    date_column_matching = True
    for date in profile["load"]["dates"]:
        if date not in date_cols:
            date_column_matching = False

    if date_column_matching:
        logging.info(f"Match with stored configuration. Importing directly...")
    else:

        for i in range(0, len(date_cols)):
            date_cols_ask = "Please, confirm that you want to use column " \
                            + f" \"{date_cols[i]}\" as date column, or change it"
            date_cols[i] = _ask_str_user(date_cols_ask, default=date_cols[i])
            logging.debug(f"Ok, using column \"{date_cols[i]}\"")

    logging.info(f"File path: {filepath}")

#######################################################################

def menu(configuration):
    """Generates and controls the menu for the app.

    Transfers the given configuration to the functions.
    """

    generate = _menu_generation(configuration)

    while generate:
        generate = _menu_generation(configuration)