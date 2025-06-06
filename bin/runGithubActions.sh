#!/bin/bash

scriptPos=${0%/*}

pushd $scriptPos/.. > /dev/null

echo "remove content of tmp folder ..."

rm -rf tmp/*

echo "removed content of tmp folder"

# stop the build if there are Python syntax errors or undefined names
if ! flake8 --exclude venv --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "There are flake8 problems [1]"
    popd > /dev/null
    exit 1
else
    echo "flake8-1 is done"
fi

# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
if ! flake8 --exclude venv --count --exit-zero --max-complexity=15 --max-line-length=127 --statistics --per-file-ignores='yacg/model/*.py:E501 E303 W391'; then
    echo "There are flake8 problems [2]"
    popd > /dev/null
    exit 1
else
    echo "flake8-2 is done"
fi

source venv/bin/activate

if ! python -m unittest discover tests "test_*.py"; then
    echo "There are problems in the tests"
    popd > /dev/null
    exit 1
fi

if ! python yacg.py \
    --models resources/models/json/yacg_config_schema.json \
            resources/models/json/yacg_model_schema.json \
    --singleFileTemplates plantUml=stdout > /dev/null; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

if ! python yacg.py \
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

if ! python \
    modelToYaml.py --model resources/models/json/yacg_model_schema.json --dryRun &> /dev/null; then
    echo "problems while run modelToYaml.py"
    popd > /dev/null
    exit 1
fi

if ! python \
    modelToJson.py --model resources/models/yaml/yacg_config_schema.yaml --dryRun &> /dev/null; then
    echo "problems while run modelToJson.py"
    popd > /dev/null
    exit 1
fi

if ! python \
    validate.py --schema resources/models/json/yacg_config_schema.json \
    --inputFile resources/configurations/conf_with_vars.json --draft07hack; then
    echo "can't validate schema"
    popd > /dev/null
    exit 1
fi

if python \
    validate.py --schema resources/models/json/yacg_config_schema.json \
    --inputFile resources/configurations/conf_with_vars.json &> /dev/null; then
    echo "wrong validation of schema"
    popd > /dev/null
    exit 1
fi

if ! python createRandomData.py --model resources/models/json/yacg_config_schema.json \
  --type Job \
  --defaultElemCount 10 \
  --outputDir ./tmp &> /dev/null; then
    echo "error while create random data"
    popd > /dev/null
    exit 1
fi

if ! python yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0202.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types.mako=stdout > /dev/null; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

if python yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0203.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types.mako=stdout; then
    echo "not detectig missing http based model"
    popd > /dev/null
    exit 1
fi

if python yacg.py \
    --models https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/models/model_0202.json \
    --delExistingStoredTemplates \
    --singleFileTemplates https://raw.githubusercontent.com/OkieOth/oth.types/master/configs/codegen/templates/golang_types_X.mako=stdout; then
    echo "problems while running a single file job from command line"
    popd > /dev/null
    exit 1
fi

# Tests for the schema validation

if python validateSchemas.py --schema tests/resources/evil/evil1.json --noEmptySchemas > /dev/null; then
    echo "Didn't identify violated schema: evil1.json"
    popd &> /dev/null
    exit 1
fi

if python validateSchemas.py --schema tests/resources/evil/evil2.json  --noEmptySchemas > /dev/null; then
    echo "Didn't identify violated schema: evil2.json"
    popd &> /dev/null
    exit 1
fi

if ! python validateSchemas.py --inputDir tests/resources/models  --noEmptySchemas > /dev/null; then
    echo "didn't validate inputDir: tests/resources/models"
    popd &> /dev/null
    exit 1
fi

if python validateSchemas.py --inputDir tests/resources/evil  --noEmptySchemas > /dev/null; then
    echo "didn't fail on inputDir: tests/resources/evil"
    popd &> /dev/null
    exit 1
fi

echo "all good :)"
popd > /dev/null
