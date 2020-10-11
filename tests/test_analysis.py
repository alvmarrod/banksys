# -*- coding: utf-8 -*-
import os
import pytest
import random
import numpy as np
import pandas as pd
import banksys.library.analysis as A

#######################################################################

def test_detect_money_cols():

    test_data = []
        
    for i in range(0,50):
        test_row = [
            "2020-05-01",
            "2020-05-01",
            random.randint(-i*2, i*2),
            "Test Concept",
            500
        ]
        test_data.append(test_row)

    test_dataframe = pd.DataFrame(test_data)

    mov, wea = A.detect_money_cols(test_dataframe)

    assert mov == 2
    assert wea == 4

def test_detect_date_cols():

    test_data = []
        
    for i in range(1,12):
        for j in range(1,20):
            test_row = [
                25,
                f"2020-{i}-{j}",
                f"2020-{i}-{j}",
                "Test Concept",
                500
            ]
            test_data.append(test_row)

    test_dataframe = pd.DataFrame(test_data)

    result = A.detect_dates_cols(test_dataframe)

    date_cols_expected = (2, 3)

    for index in result:
        assert index in date_cols_expected

#######################################################################

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup after tests
    """

    test_profile = "test_profile"

    def remove_config_test():
        print("All tests have finished! Test dabasase will be removed")
        filepath = f"./data/{test_profile}_setup.yml"
        os.remove(filepath)

    request.addfinalizer(remove_config_test)