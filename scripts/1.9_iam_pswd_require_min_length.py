#!/usr/bin/python3
import boto3
import sys
sys.path.insert(0, '../')
from common import *

##############Script for minimum password length #########################
log.info("Initiating script ")

#This function updates length of password
def funcUpdatePaswdLenght(varLen):
    log.info("Updating the policy, please wait....")
    client = boto3.client('iam')
    response = client.update_account_password_policy(
        MinimumPasswordLength=varLen
        )
    if (response['ResponseMetadata']['HTTPStatusCode']) == 200:
        log.info("Password policy updated successfully")
    else:
        log.error("Error occurred while updating Password policy")
        sys.exit()

#Comparing whether request is for compliant or non-compliant 
if func_user_input_validation() == 'compliantUpdate':
    #Changing password length
    log.info("Updating the required password length greater than 14")
    funcUpdatePaswdLenght(15)
    log.info("Minimum password length required is now set to 15")
    log.info("Password policy is now updated to compliant")
elif func_user_input_validation() == 'nonCompliantUpdate':
    log.warning("Reducing password length makes it non-compliant")
    log.info("Updating the required password length less than 14")
    funcUpdatePaswdLenght(13)
    log.info("Minimum password length required is now set to 13")
    log.info("Password policy is now updated to non-compliant")
elif func_user_input_validation() == 'compliantDelete' or func_user_input_validation() == 'nonCompliantDelete':
    log.error("Deletion does not apply to this process.")
    sys.exit()
elif func_user_input_validation() == 'createcompliant' or func_user_input_validation() == "createnoncompliant":
    log.error("Creation does not apply to this process")
    sys.exit()

func_write_to_json()

