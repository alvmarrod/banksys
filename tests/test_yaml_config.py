
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