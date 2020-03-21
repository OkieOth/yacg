# yacg
yet another code generation

W.I.P.

# Basic usage

```bash
pipenv --python 3.7
pipenv --three install
pipenv shell

# do a demo run
python3 yacg/yacg.py --model resources/models/yaml/config_schema.yaml

# run a test
pipenv run python3 -m unittest -v tests/model/test_model.py

# run all tests
pipenv run python3 -m unittest discover tests "test_*.py"
```

# Documentation

## Mako templates
* Usage: https://docs.makotemplates.org/en/latest/usage.html
* Syntax: https://docs.makotemplates.org/en/latest/syntax.html

```bash
pip install -U Sphinx

sphinx-build -b html sphinx docs
```