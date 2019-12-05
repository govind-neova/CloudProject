#!/usr/bin/env python

import boto3
import yaml
from common import *
import sys
import os.path
from os import path

#Global Variables
iam = boto3.resource('iam')
account_password_policy = iam.AccountPasswordPolicy()

#Declairing user input variable
log.info("Checking if user input exist or not")
varUserInput = func_user_input_validation()
if varUserInput:
    log.info("User input is given")

#Declairing scriptname for json file
log.info("Storing script name in variable")
varScriptName = sys.argv[0]

#Function to change the account policies
def func_account_pasword_policy(number):
    response = account_password_policy.update(
            MaxPasswordAge=number,
            )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info("Operation performed sucessfully")
    else:
        log.error("Some error has occoured while changing account password policy")

#Performing user input validation
log.info("Performing user input validation")
if varUserInput == 'compliantUpdate' :
    log.info("The user request is to make script compliant and update it")
    response=func_account_pasword_policy(90)
elif varUserInput == 'nonCompliantUpdate' :
    log.info("The user request is to make script non-compliant and update it")
    response=func_account_pasword_policy(100)
elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete' :   
    log.error("Deletion does not apply to this process.")
elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")
else :
    log.error("Please provide valid inputs")

#Writing changes to json file
log.info("Writing changes to json file")
func_write_to_json(varScriptName)
if (path.exists('1.11_iam_password_policy_expires_passwords_within_90_days.py.json')) is True :
    log.info("Changes have been written to json file")
else:
    log.error("Json file is not created")
#func_reset_config ()
