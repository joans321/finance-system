#!/bin/bash

url="http://localhost:5000/api/v1"

json_header="Content-Type: application/json"

account_json='{"username":"xyz","password":"123","type":"ctp","brokerId":"9999","mdserver":"tcp://180.168.146.187:10031","tdserver":"tdserver=tcp://180.168.146.187:10030"}'

function check() {
  if [ $? -ne 0 ]; then
    echo "command failed : $*"
    exit 1
  fi
}

## Create An Account
curl --header "$json_header"  ${url}/accounts -d $account_json -X POST

## Get All Accounts
curl ${url}/accounts

## Get Account id 1
curl ${url}/account/1 

## Get Account id 2
curl ${url}/account/2

## Update Account id 1
curl ${url}/account/1 -d "data=Remember the milk" -X PUT

## Delete Account id 1
curl ${url}/account/1 -X DELETE -v
