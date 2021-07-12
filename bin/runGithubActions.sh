#!/bin/bash

scriptPos=${0%/*}

pushd $scriptPos/.. > /dev/null

rm -rf tmp/*

# stop the build if there are Python syntax errors or undefined names
if ! flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "There are flake8 problems [1]"
    popd > /dev/null
    exit 1
fi

# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
if ! flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics; then
    echo "There are flake8 problems [2]"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 -m unittest discover tests "test_*.py"; then
    echo "There are problems in the tests"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
            resources/models/json/yacg_model_schema.json \
    --singleFileTemplates plantUml=stdout; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --usedFilesOnly; then
    echo "problems while run with usesFilesOnly"
    popd > /dev/null
    exit 1
fi


if ! bin/demoMultiFileGenerator.sh; then
    echo "problems while running multifile job from command line"
    popd > /dev/null
    exit 1
fi

if ! bin/generateRandomData_example.sh; then
    echo "problems while generate random data job from command line"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 \
    modelToYaml.py --model resources/models/json/yacg_model_schema.json --dryRun; then
    echo "problems while run modelToYaml.py"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 \
    modelToJson.py --model resources/models/yaml/yacg_config_schema.yaml --dryRun; then
    echo "problems while run modelToJson.py"
    popd > /dev/null
    exit 1
fi

echo "all good :)"
popd > /dev/null
