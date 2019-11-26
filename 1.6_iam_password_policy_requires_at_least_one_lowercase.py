#!/usr/bin/env python

import boto3
import yaml
from common import *

#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]


if varUserInput == 'compliantUpdate' :
    iam = boto3.resource('iam')
    account_password_policy = iam.AccountPasswordPolicy()
    response = account_password_policy.update(
        RequireLowercaseCharacters=True,
        )
    log.info("Compliant, Updateid account password policy")
elif varUserInput == 'nonCompliantUpdate' :
    iam = boto3.resource('iam')
    account_password_policy = iam.AccountPasswordPolicy()
    response = account_password_policy.update(
        RequireLowercaseCharacters=False,
        )
    log.info("Non-Compliant, Updated account password policy")
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete' :
    log.error("Deletion does not applies to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
else :
    log.error("Please provide valid inputs in config file")

func_write_to_json(varScriptName)
func_reset_config ()
