#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

echo "create meta model cconfiglasses ..."
if ! pipenv run python3 yacg.py --models \
    resources/models/json/yacg_model_schema.json \
    --singleFileTemplates pythonBeans=${scriptPos}/../yacg/model/model.py \
                pythonBeansTests=${scriptPos}/../tests/model/test_model.py \
                plantUml=${scriptPos}/../docs/puml/yacg_model.puml \
    --templateParameters modelPackage=yacg.model.model \
                         title="yacg model"; then
    echo "    ERROR while create meta model classes"
    exit 1
fi

echo "create config model classes ..."
if ! pipenv run python3 yacg.py --models \
    resources/models/json/yacg_config_schema.json \
    --singleFileTemplates pythonBeans=${scriptPos}/../yacg/model/config.py \
                pythonBeansTests=${scriptPos}/../tests/model/test_config.py \
                plantUml=${scriptPos}/../docs/puml/yacg_config_schema.puml \
    --templateParameters modelPackage=yacg.model.config \
                         title="yacg configuration model"; then
    echo "    ERROR while create config model classes"
    exit 1
fi

echo "create openapi model classes ..."
if ! pipenv run python3 yacg.py --models \
    resources/models/json/yacg_openapi_paths.json \
    --singleFileTemplates pythonBeans=${scriptPos}/../yacg/model/openapi.py \
                pythonBeansTests=${scriptPos}/../tests/model/test_openapi.py \
                plantUml=${scriptPos}/../docs/puml/yacg_openapi.puml \
    --blackListed yacgCore=domain \
    --templateParameters modelPackage=yacg.model.openapi \
                         baseModelDomain=yacgCore \
                         baseModelPackage=yacg.model.model \
                         baseModelPackageShort=model \
                         title="yacg openapi model"; then
    echo "    ERROR while create openapi model classes"
    exit 1
fi

popd > /dev/null