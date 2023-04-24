#!/bin/bash

scriptPos=${0%/*}

pushd $scriptPos/.. > /dev/null

rm -rf tmp/*

# stop the build if there are Python syntax errors or undefined names
if ! pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "There are flake8 problems [1]"
    popd > /dev/null
    exit 1
fi

# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
if ! pipenv run flake8 . --count --exit-zero --max-complexity=15 --max-line-length=127 --statistics --per-file-ignores='yacg/model/*.py:E501 E303 W391'; then
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
    --singleFileTemplates plantUml=stdout > /dev/null; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 yacg.py \
    --models resources/models/json/yacg_config_schema.json \
             resources/models/json/yacg_model_schema.json \
    --usedFilesOnly > /dev/null; then
    echo "problems while run with usesFilesOnly"
    popd > /dev/null
    exit 1
fi


if ! bin/demoMultiFileGenerator.sh > /dev/null; then
    echo "problems while running multifile job from command line"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 \
    modelToYaml.py --model resources/models/json/yacg_model_schema.json --dryRun &> /dev/null; then
    echo "problems while run modelToYaml.py"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 \
    modelToJson.py --model resources/models/yaml/yacg_config_schema.yaml --dryRun &> /dev/null; then
    echo "problems while run modelToJson.py"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 \
    validate.py --schema resources/models/json/yacg_config_schema.json \
    --inputFile resources/configurations/conf_with_vars.json --draft07hack &> /dev/null; then
    echo "can't validate schema"
    popd > /dev/null
    exit 1
fi

if pipenv run python3 \
    validate.py --schema resources/models/json/yacg_config_schema.json \
    --inputFile resources/configurations/conf_with_vars.json &> /dev/null; then
    echo "wrong validation of schema"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 createRandomData.py --model resources/models/json/yacg_config_schema.json \
  --type Job \
  --defaultElemCount 10 \
  --outputDir ./tmp &> /dev/null; then
    echo "error while create random data"
    popd > /dev/null
    exit 1
fi

if ! pipenv run python3 yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0202.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types.mako=stdout > /dev/null; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

if pipenv run python3 yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0203.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types.mako=stdout; then
    echo "not detectig missing http based model"
    popd > /dev/null
    exit 1
fi

if pipenv run python3 yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0202.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types_X.mako=stdout; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi


echo "all good :)"
popd > /dev/null
