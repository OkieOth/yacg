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
```