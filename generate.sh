#!/usr/bin/env bash

mkdir -p ./generated
npx nextlove-sdk-generator generate python ./generated

rm -rf ./seamapi
cp -r ./generated/seamapi ./seamapi

# 2. Why is node not recognized inside the container?