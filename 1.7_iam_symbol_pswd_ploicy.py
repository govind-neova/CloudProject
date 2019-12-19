#!/usr/bin/python3
import boto3
import sys
sys.path.insert(0, '../')
from common import *

#################This script Ensures compliance password policy require at least one symbol#################
log.info("Initiating script ")

#Function to update "require at least one symbol" password policy
def funcRequireSymbol(varDecision):
    log.info("Updating the policy, please wait....")
    client = boto3.client('iam')    
    response = client.update_account_password_policy(
        RequireSymbols=varDecision
    )
    if (response['ResponseMetadata']['HTTPStatusCode']) == 200:
        log.info("Password policy updated successfully")
    else:
        log.error("Error occurred while updating Password policy")
        sys.exit()

#Comparing whether request is for compliant or non-compliant 
if func_user_input_validation() == 'compliantUpdate':
    #Enabling the RequireSymbols field
    log.info("Enabling require symbol in password policy")
    funcRequireSymbol(True)
    log.info("Enabled require symbol in password")
    log.info("Password policy is now updated to compliant")
elif func_user_input_validation() == 'nonCompliantUpdate':
    log.warning("Disabling require symbol in password makes non-compliance")
    #Disabling the RequireSymbols field
    log.info("Disabling require symbol in password")
    funcRequireSymbol(False)
    log.info("Disabled require symbol in password")
    log.info("Password policy is now updated to non-compliant")
elif func_user_input_validation() == 'compliantDelete' or func_user_input_validation() == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
    sys.exit()
elif func_user_input_validation() == 'createcompliant' or func_user_input_validation() == "createnoncompliant":
    log.error("Creation does not apply to this process")
    sys.exit()


func_write_to_json()

