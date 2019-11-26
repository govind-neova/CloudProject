#!/usr/bin/python3
import boto3
import sys
from common import *

##############Script for minimum password length #########################

#Declaring decision variable
varUserInput= func_user_input_validation()
varScriptName = sys.argv[0]

#Comparing whether request is for compliant or non-compliant 
if varUserInput == 'compliantUpdate':
    #Changing password length
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        MinimumPasswordLength=15
        )
    log.info("Success, minimum password length required is now set to 15")
elif varUserInput == 'nonCompliantUpdate':
    log.warning("Reducing password length makes it non-compliant")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        MinimumPasswordLength=13
        )
    log.info("Success, minimum password length required is now set to 13")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
elif varUserInput == '':
    log.error("Please provide valid inputs in config.yaml file")

func_write_to_json(varScriptName)
func_reset_config ()

