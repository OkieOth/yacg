# yacg - yet another code generation

The purpose of this project is to handle JSON schema models and generate
stuff based on them.

Possible use-case are for instance to create PlanUML class diagrams based
on the models, create bean classes based on model or more sophisticated
create fully dao code with included tests. 

Basically it's a tool to play with model driven development ...

The general workflow is:
1. Take a bunch of models - for this tool JSON schemas
2. Use some suitable templates
3. Feed all of them into the tool
4. yacg - processes templates and models
5. ... and produces different text outputs

Even if this tool written in Python it can be used to create text output
in every format - all depends from choosen templates.

To free the usage of yacg from too much care about dependencies, is on 
Docker Hub `https://hub.docker.com/repository/docker/okieoth/yacg/general` 
also a docker image, from the latest master brunch push, available. 

```bash
# pull the image
docker pull okieoth/yacg
```

# Usage
## Basic Usage

Ubuntu 20.04: Attention, for some strange reasons I had to create some links manually to avoid error messages.

```bash
sudo su
ln -s /bin/python
ln -s /bin/python3
ln -s /bin/pip
```

```bash
# basic preparation
sudo apt-get install python3-venv
pip install --user pipenv

pipenv --python 3.8
pipenv install
pipenv shell

# in case of errors to create virtual env look here
# https://askubuntu.com/questions/1241993/why-i-cannot-create-pipenv-shell-in-ubuntu-20-04-lts-with-python3-8

# do a demo run ... and create plantuml
pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --singleFileTemplates plantUml=stdout

pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --usedFilesOnly

# demo run with protobuf example output
pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --singleFileTemplates protobuf=stdout


# run a test
pipenv run python3 -m unittest -v tests/model/test_model.py

# run all tests
pipenv run python3 -m unittest discover tests "test_*.py"
```
## Docker
```bash
# build a docker images
./bin/buildDockerImage.sh

# run the docker image
cd REPO_PATH
docker run -u $(id -u ${USER}):$(id -g ${USER}) -v `pwd`/resources:/resources --rm -t okieoth/yacg:0.13.0 \
    --models /resources/models/json/yacg_config_schema.json \
             /resources/models/json/yacg_model_schema.json \
    --singleFileTemplates plantUml=stdout

docker run -u $(id -u ${USER}):$(id -g ${USER}) -v `pwd`/resources:/resources --rm -t okieoth/yacg:0.13.0 \
    --models /resources/models/json/yacg_config_schema.json \
             /resources/models/json/yacg_model_schema.json \
    --singleFileTemplates xsd=stdout

```

# Documentation

## Mako templates
* Usage: https://docs.makotemplates.org/en/latest/usage.html
* Syntax: https://docs.makotemplates.org/en/latest/syntax.html

# Visual Studio Code
This project is written with vscode as editor. It contains also the .vscode configuration for the development.

Most interesting are in the debug section to pre-configured debugging tasks for the included tests.

* 'current tests' expects a open test file in the editor, and if this configuration is started, all test from this file are executed.
* 'all tests' let run all tests in the 'tests' folder of the repository

# Increment model versions
This project contains also a script to increment model versions. I has the ability to increment the version of one schema and searching for additional dependencies of that schema, and increment there the version too.

## Usage
```bash
# see the possible parameters of the script
pipenv run python3 incrementVersion.py

# do an example dry-run
pipenv run python3 incrementVersion.py --model resources/models/json/yacg_model_schema.json --version minor
```


# Models to yaml
This project contains also a script to convert JSON schemas to the yaml format. Quick'n Dirty :D

## Usage
```bash
# see the possible parameters of the script
pipenv run python3 modelToYaml.py --help

# do an example dry-run
pipenv run python3 modelToYaml.py --model resources/models/json/yacg_model_schema.json --dryRun

# feed stdin to convert
cat resources/models/json/yacg_model_schema.json | pipenv run python3 modelToYaml.py --stdin --dryRun
```

# Models to JSON
This project contains also a script to convert yaml schemas to the JSON format. Quick'n Dirty :D

## Usage
```bash
# see the possible parameters of the script
pipenv run python3 modelToJson.py --help

# do an example dry-run
pipenv run python3 modelToJson.py --model resources/models/yaml/yacg_config_schema.yaml --dryRun

# feed stdin to convert
cat resources/models/yaml/yacg_config_schema.yaml | pipenv run python3 modelToJson.py \
    --stdin --dryRun
```

# Some Last Words
This project is a spare time project - with all its pros and cons. The development of this project is done under a Linux OS, so I have no clue how it is working on Windows machines. 
