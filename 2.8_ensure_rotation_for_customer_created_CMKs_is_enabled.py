#!/usr/bin/python

import boto3
import json
import sys
import os.path
from os import path
sys.path.insert(0, '../')
from common import *

#Global variables
kms_client = boto3.client('kms')
kms_response = kms_client.list_keys(
    Limit=1000,
)

#Function describing compliant kmsKeys
def func_kmsKeys_details (varDecision):
    keys = dict()
    for i in kms_response['Keys']:
        temp = []
        try:
            keyState = kms_client.describe_key(KeyId=i['KeyId'])
            if "PendingDeletion" not in str(keyState['KeyMetadata']['KeyState']) and "Default master key that protects my" not in str(keyState['KeyMetadata']['Description']):
                rotationStatus = kms_client.get_key_rotation_status(KeyId=i['KeyId'])
                if varDecision is True:
                    if rotationStatus['KeyRotationEnabled'] is True :
                        status = kms_client.describe_key(KeyId=i['KeyId'])
                        if (status['KeyMetadata']['Enabled']) is True:
                            temp.append(i['KeyId'])
                        keys[i['KeyArn']] = temp
#                            print (status['KeyMetadata']['Enabled'])
                elif varDecision is False:
                    status = kms_client.describe_key(KeyId=i['KeyId'])
                    if rotationStatus['KeyRotationEnabled'] is False or (status['KeyMetadata']['Enabled']) is False :
                        temp.append(i['KeyId'])
                    keys[i['KeyArn']] = temp
                elif varDecision is None:
                    temp.append(i['KeyId'])
                    keys[i['KeyArn']] = temp
        except Exception as e:
            print(e)
    return keys
            

kmsKeys_compliant = func_kmsKeys_details (True)
for i in kmsKeys_compliant:
    for j in kmsKeys_compliant[i]:
        print (j)

#Function to create compliant key and non complianr keys
def func_create_compliant_or_non_compliant_key (varDecision):
    if varDecision is True:
        log.info('Creating compliant key')
        kms_response = kms_client.create_key()
        print (kms_response['KeyMetadata']['KeyId'])
        kms_client.enable_key_rotation(KeyId=kms_response['KeyMetadata']['KeyId'])
    elif varDecision is False:
        log.info('Creating non-compliant key')
        kms_response = kms_client.create_key(Description="cis-testing-key")
        print (kms_response['KeyMetadata']['KeyId'])

#If loop for performing operations on Cloudtrails as per config.yaml file
if func_user_input_validation() == 'nonCompliantUpdate':
    log.info('Updating resources as non-compliant as per request')
    log.info("Gathering information for compliant resources")
    kmsKeys_compliant = func_kmsKeys_details (True)
    for i in kmsKeys_compliant:
        for j in kmsKeys_compliant[i]:
            print(j)
            kms_client.disable_key_rotation(KeyId=j)

elif func_user_input_validation() == 'compliantUpdate':
    log.info('Updating resources as compliant as per request')
    log.info("Gathering information for non-compliant resources")
    kmsKeys_compliant = func_kmsKeys_details (False)
    for i in kmsKeys_compliant:
        for j in kmsKeys_compliant[i]:
            rotationStatus = kms_client.get_key_rotation_status(KeyId=j)
            status = kms_client.describe_key(KeyId=j)
            if (status['KeyMetadata']['Enabled']) is True :
                if rotationStatus['KeyRotationEnabled'] is False :
                    print (j)
                    kms_client.enable_key_rotation(KeyId=j)

elif func_user_input_validation() == 'compliantDelete':
    log.info('The user request is to delete existing resource/resources and create a compliant resource')
    kmsKeys_compliant = func_kmsKeys_details (None)
    for i in kmsKeys_compliant:
        for j in kmsKeys_compliant[i]:
            kms_client.schedule_key_deletion(KeyId=j)
    func_create_compliant_or_non_compliant_key (True)

elif varUserInput == 'nonCompliantDelete':
    log.info('The user request is to delete existing resource/resources and create a non-compliant resource')
    kmsKeys_compliant = func_kmsKeys_details (None)
    for i in kmsKeys_compliant:
        for j in kmsKeys_compliant[i]:
            kms_client.schedule_key_deletion(KeyId=j)
    func_create_compliant_or_non_compliant_key (False)

elif varUserInput == 'createcompliant':
    func_create_compliant_or_non_compliant_key (True)

elif varUserInput == "createnoncompliant":
    func_create_compliant_or_non_compliant_key (False)
