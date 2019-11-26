#!/usr/bin/python

import boto3
import yaml
from common import *
import sys

#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]

#Global variables
kms_client = boto3.client('kms')
kms_response = kms_client.list_keys(
    Limit=1000,
)

#Function describing compliant kmsKeys
def func_kmsKeys_details_compliant ():
    for i in kms_response['Keys']:
        try:
            keyState = kms_client.describe_key(KeyId=i['KeyId'])
            if "PendingDeletion" not in str(keyState['KeyMetadata']['KeyState']) and "Default master key that protects my" not in str(keyState['KeyMetadata']['Description']):
                rotationStatus = kms_client.get_key_rotation_status(KeyId=i['KeyId'])
                if rotationStatus['KeyRotationEnabled'] is True :
                    status = kms_client.describe_key(KeyId=i['KeyId'])
                    if (status['KeyMetadata']['Enabled']) is True:
                        yield i
#                        print (status['KeyMetadata']['Enabled'])
        except Exception as e:
            print(e)
              
kmsKeys_compliant = func_kmsKeys_details_compliant ()

#Function describing non-compliant kmsKeys
def func_kmsKeys_details_nonCompliant ():
    for i in kms_response['Keys']:
        try:
            keyState = kms_client.describe_key(KeyId=i['KeyId'])
            if "PendingDeletion" not in str(keyState['KeyMetadata']['KeyState']) and "Default master key that protects my" not in str(keyState['KeyMetadata']['Description']):
                rotationStatus = kms_client.get_key_rotation_status(KeyId=i['KeyId'])
                status = kms_client.describe_key(KeyId=i['KeyId'])
                if rotationStatus['KeyRotationEnabled'] is False or (status['KeyMetadata']['Enabled']) is False :
                    yield i
        except Exception as e:
            print(e)

kmsKeys_nonCompliant = func_kmsKeys_details_nonCompliant ()

#Function to list customer managed keys kmsKeys
def func_kmsKeys_list_cmks ():
    for i in kms_response['Keys']:
        try:
            keyState = kms_client.describe_key(KeyId=i['KeyId'])
            if "PendingDeletion" not in str(keyState['KeyMetadata']['KeyState']) and "Default master key that protects my" not in str(keyState['KeyMetadata']['Description']):
                status = kms_client.describe_key(KeyId=i['KeyId'])
#                yield (i['KeyId'])
                yield i
                print (status['KeyMetadata']['Enabled'])
        except Exception as e:
            print(e)

kmsKeys_list_cmks = func_kmsKeys_list_cmks ()

#Function to create compliant key
def func_create_compliant_key ():
    kms_response = kms_client.create_key(Description="cis-testing-key")
    print (kms_response['KeyMetadata']['KeyId'])
    kms_client.enable_key_rotation(KeyId=kms_response['KeyMetadata']['KeyId'])

#Function to create non-compliant key
def func_create_non_compliant_key ():
    kms_response = kms_client.create_key(Description="cis-testing-key")

#If loop for performing operations on Cloudtrails as per config.yaml file
if varUserInput == 'nonCompliantUpdate':
    log.info('Non-compliant and Update')
    for value in func_kmsKeys_details_compliant ():
        print (value['KeyArn'])
        kms_client.disable_key_rotation(KeyId=value['KeyId'])
    func_create_non_compliant_key ()
elif varUserInput == 'compliantUpdate':
    log.info('compliant and Update')
    for value in func_kmsKeys_details_nonCompliant ():
        rotationStatus = kms_client.get_key_rotation_status(KeyId=value['KeyId'])
        status = kms_client.describe_key(KeyId=value['KeyId'])
        if (status['KeyMetadata']['Enabled']) is True :
            if rotationStatus['KeyRotationEnabled'] is False :
                print (value['KeyArn'])
                kms_client.enable_key_rotation(KeyId=value['KeyId'])
    func_create_compliant_key ()
elif varUserInput == 'compliantDelete':
    log.info('compliant and Delete')
    for value in func_kmsKeys_list_cmks () :
        print (value['KeyArn'])
        kms_client.schedule_key_deletion(KeyId=value['KeyId'])
    func_create_compliant_key ()
elif varUserInput == 'nonCompliantDelete':
    log.info('compliant and Delete')
    for value in func_kmsKeys_list_cmks () :
        print (value['KeyArn'])
        kms_client.schedule_key_deletion(KeyId=value['KeyId'])
    func_create_non_compliant_key ()
elif varUserInput == 'createcompliant':
    func_create_compliant_key ()
elif varUserInput == "createnoncompliant":
    func_create_non_compliant_key ()
