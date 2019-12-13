#!/usr/bin/python3
#Script for the uppercase password policy compliance/Non-compliance
import boto3
import sys
sys.path.insert(0, '../')
from common import *

####################Script for the uppercase password policy compliance###################
log.info("Initiating script ")

#Function to update Password policy as per the inputs provided
def funcUpdatePwdPolicy(vardecision):
    log.info("Updating the policy, please wait....")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        RequireUppercaseCharacters=vardecision
        )
    if (response['ResponseMetadata']['HTTPStatusCode']) == 200:
        log.info("Password policy updated successfully")
    else:
        log.error("Error occurred while updating Password policy")
        sys.exit()

#According to inputs provided script will take action
if func_user_input_validation() == 'compliantUpdate':
    #Ticks the required uppercase characters checkbox
    log.info("Enabling uppercase case in password policy")
    funcUpdatePwdPolicy(True)
    log.info("Enabled uppercase character in password")
    log.info("Password policy is now updated to compliant")
elif func_user_input_validation() == 'nonCompliantUpdate':
    #Un-Checking the required uppercase characters checkbox
    log.warning("Disabling require uppercase character in password makes non-compliance")
    funcUpdatePwdPolicy(False)
    log.info("Disabled uppercase character in password")
    log.info("Password policy is now updated to compliant")
elif func_user_input_validation() == 'compliantDelete' or func_user_input_validation() == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
    sys.exit()
elif func_user_input_validation() == 'createcompliant' or func_user_input_validation() == "createnoncompliant":
    log.error("Creation does not apply to this process")
    sys.exit()


func_write_to_json()
