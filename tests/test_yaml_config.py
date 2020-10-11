# -*- coding: utf-8 -*-
import os
import pytest
import banksys.library.yamlconfig as YC

#######################################################################

def test_yaml_config():

    test_profile = "test_profile"
    test_data = {
        "profile": {
            "name": "test_user",
            "consolidate": "true"
        }
    }

    YC.save_config(test_profile, test_data)
    reloaded_data = YC.load_config(test_profile)

    for k in test_data["profile"]:
        assert test_data["profile"][k] == reloaded_data["profile"][k]

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