#!/usr/bin/python3
#Script for the uppercase password policy compliance/Non-compliance
import boto3
import sys
from common import *

####################Script for the uppercase password policy compliance###################

#Declaring decision variable
varUserInput= func_user_input_validation()
varScriptName = sys.argv[0]


#Comparing whether request is for compliant or non-compliant 
if varUserInput == 'compliantUpdate':
    #Checking the required uppercase characters checkbox
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireUppercaseCharacters=True
    )
    log.info("Enabled uppercase character in password")
elif varUserInput == 'nonCompliantUpdate':
    #Un-Checking the required uppercase characters checkbox
    log.warning("Disabling require uppercase character in password makes non-compliance")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireUppercaseCharacters=False
    )   
    log.info("Disabled uppercase character in password")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
elif varUserInput == '':
    log.error("Please provide valid inputs in config.yaml file")

func_write_to_json(varScriptName)
func_reset_config ()
