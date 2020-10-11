# banksys

This project aims to generate an analysis of your finances, taking as input a CSV file with bank account movements.

## Usage

Execute the main script to access the app main menu and start working from there.

```
$ python main.py

############### banksys ###############
####                               ####
# 1. See report                       #
# 2. Load new movements               #
# 3. Manual analysis                  #
# 4. Remove database                  #
# 5. Exit                             #
####                               ####
#######################################

Choose an option:
```

## Versions

Current version tag is available in [version.txt](./version.txt) file, and you can refer to the [changelog](./changelog.md) file for more information on each version number.

Remember that a new commit does not imply a new version.

## Testing

Tests are performed using PyTest library. To run them all, you can perform from the project folder:

```
pytest
```

## Dependencies

- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [PyTest](https://pypi.org/project/pytest/)