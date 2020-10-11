# -*- coding: utf-8 -*-
import os
import random
import pytest
import banksys.library.database as DB

#######################################################################



#######################################################################

def test_open_database():

    db_file = "test_database"

    con = DB.open_database(db_file)

    assert con is not None
    con.close()

def test_insert_movement_correct():

    db_file = "test_database"

    con = DB.open_database(db_file)
    assert con is not None

    test_data = (
        "2000-12-12",
        "2000-12-12",
        "Test Concept",
        25,
        50)
    result = DB.insert_movement(con, test_data)

    assert result == True

    DB.close_database(con)

def test_insert_movement_wrong_args_amount():

    db_file = "test_database"

    con = DB.open_database(db_file)
    assert con is not None

    test_data = (
        "2000-12-12",
        "2000-12-12",
        "Test Concept",
        25)
    result = DB.insert_movement(con, test_data)

    assert result == False

    DB.close_database(con)


def test_get_movements():

    db_file = "test_database"

    con = DB.open_database(db_file)
    assert con is not None

    result = DB.read_movements(con)
    assert len(result) > 0

    DB.close_database(con)

def test_get_movement_by_amount():

    db_file = "test_database"
    test_value = 25

    con = DB.open_database(db_file)
    assert con is not None

    result = DB.read_movements_by_amount(con, test_value)
    
    for row in result:
        assert row[4] == test_value

    DB.close_database(con)

def test_read_movements_by_amount_range():

    db_file = "test_database"
    test_min_value = 20
    test_max_value = 30

    con = DB.open_database(db_file)
    assert con is not None

    for i in range(0, 50):
        test_data = (
            "2000-12-12",
            "2000-12-12",
            "Test Concept",
            random.randint(1, 100),
            i + 50)
        result = DB.insert_movement(con, test_data)

    result = DB.read_movements_by_amount_range(con, 
                test_min_value, test_max_value)
    
    for row in result:
        assert row[4] >= test_min_value
        assert row[4] <= test_max_value

    DB.close_database(con)

def test_read_movements_by_balance_range():

    db_file = "test_database"
    test_min_value = 125
    test_max_value = 150

    con = DB.open_database(db_file)
    assert con is not None

    for i in range(0, 50):
        test_data = (
            "2000-12-12",
            "2000-12-12",
            "Test Concept",
            i+5,
            random.randint(100, 200))
        result = DB.insert_movement(con, test_data)

    result = DB.read_movements_by_balance_range(con, 
                test_min_value, test_max_value)
    
    for row in result:
        assert row[5] >= test_min_value
        assert row[5] <= test_max_value

    DB.close_database(con)

def test_read_movements_by_op_date():

    db_file = "test_database"

    con = DB.open_database(db_file)
    assert con is not None

    for i in range(0, 12):
        for j in range(0, 20):

            test_date = f"2000-{i}-{j}"

            test_data = (
                test_date,
                test_date,
                "Test Concept",
                50,
                100)
            result = DB.insert_movement(con, test_data)

            if result:
                result = DB.read_movements_by_op_date(con, test_date)
    
    for row in result:
        assert row[1] == test_date

    DB.close_database(con)

def test_read_movements_by_val_date():

    db_file = "test_database"

    con = DB.open_database(db_file)
    assert con is not None

    for i in range(0, 12):
        for j in range(0, 20):

            test_date = f"2000-{i}-{j}"

            test_data = (
                test_date,
                test_date,
                "Test Concept",
                50,
                100)
            result = DB.insert_movement(con, test_data)

            if result:
                result = DB.read_movements_by_op_date(con, test_date)
    
    for row in result:
        assert row[2] == test_date

    DB.close_database(con)

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup after tests
    """

    db_file = "test_database"

    def remove_db_test():
        print("All tests have finished! Test dabasase will be removed")
        filepath = f"./data/{db_file}.db"
        os.remove(filepath)

    request.addfinalizer(remove_db_test)