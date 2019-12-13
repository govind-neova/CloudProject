#!/usr/bin/python3
import boto3
import sys
sys.path.insert(0, '../')
from common import *

####################Script for require numbers in password policy###############
log.info("Initiating script ")

#Function enables/disables the "require at least one number in password"
def funcRequireNumber(varDecision):
    log.info("Updating the policy, please wait....")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireNumbers=varDecision
        )
    if (response['ResponseMetadata']['HTTPStatusCode']) == 200:
        log.info("Password policy updated successfully")
    else:
        log.error("Error occurred while updating Password policy")
        sys.exit()



#Comparing whether request is for compliant or non-compliant 
if func_user_input_validation() == 'compliantUpdate':
    #Checking the require number checkbox
    log.info("Enabling require number in password")
    funcRequireNumber(True)
    log.info("Enabled require number in password")
    log.info("Password policy is now updated to compliant")
elif func_user_input_validation() == 'nonCompliantUpdate':
    #Un-Checking the require number checkbox
    log.warning("Disabling require numbers in password makes non-compliance")
    log.info("Disabling require numbers in password")
    funcRequireNumber(False)
    log.info("Disabled require number in password")
    log.info("Password policy is now updated to non-compliant")
elif func_user_input_validation() == 'compliantDelete' or func_user_input_validation() == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
    sys.exit()
elif func_user_input_validation() == 'createcompliant' or func_user_input_validation() == "createnoncompliant":
    log.error("Creation does not apply to this process")
    sys.exit()

func_write_to_json()
