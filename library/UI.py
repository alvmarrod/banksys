# -*- coding: utf-8 -*-
import os
import logging

def _ask_back_to_menu() -> bool:
    """Checks if the user wants to go back to the menu
    """

    result = False

    try:
        
        option = input("Do you want to go back to menu? (Y/N): ")
        
        if option.lower() == "y":
            result = True
            
    except ValueError as e:
        print("Error! {e}")

    return result

def _menu_generation() -> bool:
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
            "function": None
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

    os.system("cls")

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
            options[option]["function"]()
        else:
            raise ValueError(f"Option {option} is not available!")

    except ValueError as e:

        print(f"Error! {e}\n")

        if not _ask_back_to_menu():
            show_again = False
    
    return show_again

#######################################################################

def menu():
    """Generates and controls the menu for the app.
    """

    generate = _menu_generation()

    while generate:
        generate = _menu_generation()