#!/bin/bash

scriptPos=${0%/*}

imageBase=okieoth/yacg
imageTag=0.0.1

imageName="$imageBase:$imageTag"

pushd "$scriptPos" > /dev/null
	if docker build -t $imageName ..
    then
        echo -en "\033[1;34m  image created: $imageName \033[0m\n"
    else
        echo -en "\033[1;31m  error while create image: $imageName \033[0m\n"
    fi
popd > /dev/null
