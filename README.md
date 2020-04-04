# yacg
yet another code generation

W.I.P.

# Basic usage

```bash
# basic preparation
pip install --user pipenv

pipenv --python 3.7
pipenv --three install
pipenv shell

# do a demo run
pipenv run python3 yacg.py --model \
    resources/models/json/config_schema.json \
    resources/models/json/yacg_model_schema.json

# run a test
pipenv run python3 -m unittest -v tests/model/test_model.py

# run all tests
pipenv run python3 -m unittest discover tests "test_*.py"
```

# Documentation

## Mako templates
* Usage: https://docs.makotemplates.org/en/latest/usage.html
* Syntax: https://docs.makotemplates.org/en/latest/syntax.html

# Visual Studio Code
This project is written with vscode as editor. It contains also the .vscode configuration for the development.

Most interesting are in the debug section to pre-configured debugging tasks for the included
tests.

* 'current tests' expects a open test file in the editor, and if this configuration is started, all test from this file are executed.
* 'all tests' let run all tests in the 'tests' folder of the repository
