#!/usr/bin/env python

import boto3
import yaml
from common import *
import sys

#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]

if varUserInput == 'compliantUpdate' :
    iam = boto3.resource('iam')
    account_password_policy = iam.AccountPasswordPolicy()
    response = account_password_policy.update(
        MaxPasswordAge=90,
        )
    log.info("Compliant and Update")
elif varUserInput == 'nonCompliantUpdate' :
    iam = boto3.resource('iam')
    account_password_policy = iam.AccountPasswordPolicy()
    response = account_password_policy.update(
        MaxPasswordAge=100,
        )
    log.info("non-Compliant and Update")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete' :   
    log.error("Deletion does not applies to this process.")
else :
    log.error("Please provide valid inputs")


func_write_to_json(varScriptName)