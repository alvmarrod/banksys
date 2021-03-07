# -*- coding: utf-8 -*-
import os
import pytest
import banksys.library.yamlconfig as YC

#######################################################################

def test_yaml_config():

    test_profile = "test_profile"

    # Load original data/generate it
    test_data = YC.load_config(test_profile)

    # Modify it
    test_data["profile"]["load"]["wealth"] = 288

    # Save it
    YC.save_config(test_profile, test_data)

    # Load again to check if saving works
    data_saved = YC.load_config(test_profile)

    for k in test_data["profile"]:
        print(f"{test_data} vs {data_saved}")
        assert test_data["profile"][k] == data_saved["profile"][k]

#######################################################################

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup after tests
    """

    test_profile = "test_profile"

    def remove_config_test():
        print("All tests have finished! Test configuration will be removed")
        filepath = f"./data/{test_profile}_setup.yml"
        # os.remove(filepath)

    request.addfinalizer(remove_config_test)