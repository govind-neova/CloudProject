#!/usr/bin/python3
import boto3
import sys
from common import *

####################Script for require numbers in password policy###############

varUserInput= func_user_input_validation()
varScriptName = sys.argv[0]

#Comparing whether request is for compliant or non-compliant 
if varUserInput == 'compliantUpdate':
    #Checking the require number checkbox
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireNumbers=True
        )
    log.info("Enabled require number in password")
elif varUserInput == 'nonCompliantUpdate':
    #Un-Checking the require number checkbox
    log.warning("Disabling require numbers in password makes non-compliance")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireNumbers=False
    )
    log.info("Disabled require number in password")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
elif varUserInput == '':
    log.error("Please provide valid inputs in config.yaml file")

func_write_to_json(varScriptName)
func_reset_config ()
