#!/usr/bin/env python

#import boto3
#import yaml
#from common import *
#import sys
#import os.path
#from os import path
import os.path
from os import path
import boto3
import sys
sys.path.insert(0, '../')
from common import *

#Global Variables
iam = boto3.resource('iam')
account_password_policy = iam.AccountPasswordPolicy()
varResources = []

#Function to change the account policies
def func_account_pasword_policy(decision):
    response = account_password_policy.update(
            RequireLowercaseCharacters=decision,
            )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info("Operation performed sucessfully")
    else:
        log.error("Some error has occoured while changing account password policy")
    
#Performing user input validation
log.info("Performing user input validation")
if func_user_input_validation() == 'compliantUpdate' :
    log.info("The user request is to make script compliant and update it")
    response=func_account_pasword_policy(True)
elif func_user_input_validation() == 'nonCompliantUpdate' :
    log.info("The user request is to make script non-compliant and update it")
    response=func_account_pasword_policy(False)
elif func_user_input_validation() == 'compliantDelete' or func_user_input_validation() == 'nonCompliantDelete' :
    log.error("Deletion does not applies to this process.")
elif func_user_input_validation() == 'createcompliant' or func_user_input_validation() == "createnoncompliant":
    log.error("Creation does not apply to this process")
else :
    log.error("Please provide valid inputs in config file")

#Writing changes to json file
func_write_to_json(varResources)
if (path.exists('1.11_iam_password_policy_expires_passwords_within_90_days.json')) is True :
    log.info("Changes has been written to json file")
else:
    log.info("Json file is not created")
