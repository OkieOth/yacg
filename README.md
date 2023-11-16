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

To free the usage of yacg from too much care about dependencies, it's also
available as container image from the GitHub repository. There are a 'latest'
tag and also a tag matching the content of the `version.txt` file.

```bash
# e.g. pull the image with a fixed tag
docker pull ghcr.io/okieoth/yacg:3.2.2

# pull the lastest images
docker pull ghcr.io/okieoth/yacg
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

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt



# do a demo run ... and create plantuml
python yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --singleFileTemplates plantUml=stdout

python yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --usedFilesOnly

# demo run with protobuf example output
python yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --singleFileTemplates protobuf=stdout


# run a test
python -m unittest -v tests/model/test_model.py

# run all tests
python -m unittest discover tests "test_*.py"
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
python incrementVersion.py

# do an example dry-run
python incrementVersion.py --model resources/models/json/yacg_model_schema.json --version minor
```


# Models to yaml
This project contains also a script to convert JSON schemas to the yaml format. Quick'n Dirty :D

## Usage
```bash
# see the possible parameters of the script
python modelToYaml.py --help

# do an example dry-run
python modelToYaml.py --model resources/models/json/yacg_model_schema.json --dryRun

# feed stdin to convert
cat resources/models/json/yacg_model_schema.json | python modelToYaml.py --stdin --dryRun


# more sophisticated example to create openApi yaml
python yacg.py \
    --models tests/resources/models/json/examples/openapi_v3_example_refs.json \
    --singleFileTemplates resources/templates/examples/normalizedOpenApiJson.mako=/tmp/test.json && \
    python modelToYaml.py --model /tmp/test.json --destDir /tmp
```

# Models to JSON
This project contains also a script to convert yaml schemas to the JSON format. Quick'n Dirty :D

## Usage
```bash
# see the possible parameters of the script
python modelToJson.py --help

# do an example dry-run
python modelToJson.py --model resources/models/yaml/yacg_config_schema.yaml --dryRun

# feed stdin to convert
cat resources/models/yaml/yacg_config_schema.yaml | python modelToJson.py \
    --stdin --dryRun
```

# Normalize Models
The project contains a function to resolve and remove external references from a
schema

## Usage
```bash
# python version
python normalizeSchema.py --model

# docker version
docker run -u $(id -u ${USER}):$(id -g ${USER}) \
    -v `pwd`:/resources \
    --rm -t --entrypoint "python3" \
    ghcr.io/okieoth/yacg:5.6.0 \
    normalizeSchema.py \
    --model /resources/my_model.yaml \
    --outputFile /resources/generated/my_model_without_externals.yaml \
    --yaml
```

# Validate JSON files against schemas
For the validation of schemas is `https://github.com/johnnoone/json-spec` used.

Attention, the current version of json-spec doesn't support JSON schema draft-07.
If the right parameter set, then the validation wrapper removes the `$schema` tag
from the schema input and tries the validation without it.

## Usage
```bash
# bash version
python validate.py --schema resources/models/json/yacg_config_schema.json \
  --inputFile resources/configurations/conf_with_vars.json \
  --draft07hack # used because json-spec has currently not draft07 support

# docker version
docker run -u $(id -u ${USER}):$(id -g ${USER}) \
    -v `pwd`:/resources \
    --rm -t --entrypoint "python3" \
    ghcr.io/okieoth/yacg:5.9.0 \
    validate.py \
    --schema /resources/resources/models/json/yacg_config_schema.json \
    --inputFile /resources/resources/configurations/conf_with_vars.json \
    --draft07hack
```

# Create Random Data From Models

With the `createRandomData.py` script, the package contains a tool to create random data based on the models.
For further configurations see [here](docs/random_data_creation.md)

```bash
# creates in the tmp folder a file Job.json with 10 random objects of the Job type
python createRandomData.py --model resources/models/json/yacg_config_schema.json \
  --type Job \
  --defaultElemCount 10
  --outputDir ./tmp
```
# Create Random Data and provide them over REST

The script `randomDataServer.py` provides a simple http server that loads a model and
provides random data based on the contained type description. It basically recycles
the functions used in `createRandomData.py` and shares also the same commandline switches
with that script.

```bash
# will start a simple http server on port 8080 that provides random data for a given type
python randomDataServer.py --model resources/models/json/yacg_config_schema.json

# reading one random data set of the type 'Job'
curl 'http://localhost:8080/job'

# reading two random data sets of the type 'Job'
curl 'http://localhost:8080/job?count=2'

# reading two random data sets of the type 'Job', w/o any indent
curl 'http://localhost:8080/job?count=2&noIndent=true'

# reading one random data set of the type 'Job', with no random decision if non-required
# properties should be generated or not
curl 'http://localhost:8080/templateparam?probabilityToBeEmpty=0'
```

# Some Last Words
This project is a spare time project - with all its pros and cons. The development of this project is done under a Linux OS, so I have no clue how it is working on Windows machines.

This project is advanced challended here: https://github.com/OkieOth/nibelheim_ts
