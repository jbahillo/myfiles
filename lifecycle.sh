#!/bin/bash
az login -o none
echo "The following accounts have some Lifecycle Policy:"
IFS=$'\n'
for SUBSCRIPTION in $(az account list | grep id | cut -f4 -d\")
do
	az account set -s $SUBSCRIPTION
	for SA in $(az storage account list --subscription $SUBSCRIPTION -o table --query "[].{Name:name, RGroup:resourceGroup}" | grep -v Name | grep -v -- "-----")
	do
		ACCOUNT=$(echo $SA | awk '{print $1}')
		RG=$(echo $SA | awk '{print $2}')
		az storage account management-policy show --account-name $ACCOUNT --resource-group $RG >/dev/null 2>&1;
		exit=$?
		if [ $exit -eq 0 ]; then
		    echo $ACCOUNT 
		fi
	done
done

