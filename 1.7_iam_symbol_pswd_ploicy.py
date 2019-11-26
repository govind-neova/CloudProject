#!/usr/bin/python3
import boto3
import sys
from common import *

#################This script Ensures compliance password policy require at least one symbol#################

#Declaring decision variable
varUserInput= func_user_input_validation()
varScriptName = sys.argv[0]

#Comparing whether request is for compliant or non-compliant 
if varUserInput == 'compliantUpdate':
#Enabling the RequireSymbols field
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireSymbols=True
    )
    log.info("Enabled required at least one symbol in password")
elif varUserInput == 'nonCompliantUpdate':
    log.warning("Disabling require at least one symbol in password makes non-compliance")
#Disabling the RequireSymbols field to make non-compliance
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireSymbols=False
    )
    log.info("Disabled requirement of at least one symbol in password")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
else:
    log.error("Please provide valid inputs in config.yaml file")


func_write_to_json(varScriptName)
func_reset_config ()
