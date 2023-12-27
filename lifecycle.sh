#!/bin/bash
az login -o none
IFS=$'\n'
echo "The following accounts have some Lifecycle Policy:"
for SA in $(az storage account list   -o table | awk '{print $8, $11}')
do
	if [ $SA != "Name ResourceGroup" ] && [ $SA != "----------------------- -------------------------------------" ]
	then
		ACCOUNT=$(echo $SA | awk '{print $1}')
		RG=$(echo $SA | awk '{print $2}')
		az storage account management-policy show --account-name $ACCOUNT --resource-group $RG >/dev/null 2>&1;
		exit=$?
		if [ $exit -eq 0 ]; then
		    echo $ACCOUNT 
		fi
	fi
done

