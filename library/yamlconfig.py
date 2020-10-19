# -*- coding: utf-8 -*-
import os
import yaml
import logging

#######################################################################

def _yaml_to_str(yaml_data) -> str:
    """Returns given YAML data as a string, using the YAML
    style with block indentation. Useful to print data.

    Parameters:
    - A `dict` with the YAML data to be represented.

    Returns:
    - A `str` with the YAML data in the specified format.
    """

    return yaml.dump(yaml_data, default_flow_style=False)

def _generate_base_config(profile_name):
    """Generate a basic configuration for a profile. This function is
    idempotent, so it will not overwrite an existing config file.
    """

    logging.info(f"Generating base config...")

    data = {
        "profile": {
            "name": "User1",
            "consolidate": "true",
            "load": {
                "wealth": "",
                "movements": "",
                "dates": []
            }
        }
    }
    
    save_config(profile_name, data)


def _load_config(profile_name) -> dict:
    """Load the specified file as a YAML configuration file and returns
    it parsed as a Python Dictionary

    Parameters:
    - A `str` specifying the profile name

    Returns:
    - A `dict` with the file YAML data loaded in it.

    FP: Non-pure function
    """

    filepath = f"./data/{profile_name}_setup.yml"

    if not os.path.exists(filepath):
        raise Exception("File does not exist!")

    with open(filepath, 'r') as stream:
        try:
            setup = yaml.safe_load(stream)
            # Map configuration to avoid having to go into profile object
            setup = setup["profile"]
        except yaml.YAMLError as e:
            raise e

    return setup

#######################################################################

def load_config(profile_name) -> dict:
    """Load the configuration for the specified profile. If is doesn't
    exist, creates a basic setup for it and then loads it.

    Parameters:
    - A `str` with the profile name to be loaded.

    Returns:
    - A `dict` with the loaded setup

    FP: Non-pure function
    """

    setup = {}

    logging.info(f"Loading config...")

    try: 
        
        _generate_base_config(profile_name)
        setup = _load_config(profile_name)

    except Exception as e:

        logging.warning(f"Error loading profile \"{profile_name}\"")
        logging.info(e)

    return setup

def save_config(profile_name, data):
    """Save the given configuration into the appropriate profile file.

    Parameters:
    - A `str` with the profile name.
    - A `dict` with the configuration to save.
    """

    filepath = f"./data/{profile_name}_setup.yml"

    logging.info(f"Saving config...")
        
    with open(filepath, 'w') as stream:

        try:

            if "profile" not in data:
                saving_data = {
                    "profile": {
                        "name": profile_name
                    }
                }

                for k in data.keys():
                    saving_data["profile"][k] = data[k]

            else:
                saving_data = data

            config = _yaml_to_str(saving_data)
            stream.write(config)
        except Exception as e:
            raise e