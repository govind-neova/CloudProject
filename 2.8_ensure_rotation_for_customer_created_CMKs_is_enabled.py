#!/usr/bin/python

import boto3
import yaml
from common import *
import sys

#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]


kms_client = boto3.client('kms')
#response = kms_client.create_key(Description="testing key")
#print (response['Key'])

#keys = kms_client.list_keys(
#    Limit=1000,
#)
#print (keys)
#
#response = client.describe_key(
#    KeyId='string'
#)

#if varUserInput == 'compliantUpdate' :
#    paginator = kms_client.get_paginator('list_keys')
#    response_iterator = paginator.paginate()
#    for page in response_iterator:
#    #    print (page)
#        for n in page['Keys']:
#            try:
#                rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
#                print (rotationStatus)
#                if rotationStatus['KeyRotationEnabled'] is False:
#                    keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
#                   # print (rotationStatus)
#                    kms_client.enable_key_rotation(
#                            KeyId=n['KeyId']
#                            )
#                    log.info("Compliant and Update")
#            except:
#                print("No result")
#
#elif varUserInput == 'nonCompliantUpdate' :
#    paginator = kms_client.get_paginator('list_keys')
#    response_iterator = paginator.paginate()
#    for page in response_iterator:
##        print ("nonCompliantUpdate")
##        print (page)
#        for n in page['Keys']:
#            rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
##            print (n['KeyId'])
#            if rotationStatus['KeyRotationEnabled'] is True:
#                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
#                if "Default master key that protects my" not in str(keyDescription['KeyMetadata']['Description']):
#                    print (n['KeyId'])
#                    print (rotationStatus)
#                    kms_client.disable_key_rotation(KeyId=n['KeyId'])
#                    log.info("Non-Compliant and Update")
           

paginator = kms_client.get_paginator('list_keys')
response_iterator = paginator.paginate()
for page in response_iterator:
    for n in page['Keys']:
        try:
            rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
#            print (n['KeyId'])
            if rotationStatus['KeyRotationEnabled'] is False :
                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
                if "Default master key that protects my" not in str(keyDescription['KeyMetadata']['Description']):
                    print (n['KeyId'])
                    print (rotationStatus)
                    if varUserInput == 'compliantUpdate':
                        kms_client.enable_key_rotation(KeyId=n['KeyId'])
                        log.info("Compliant and Update")
                    elif varUserInput == 'compliantDelete':
                        kms_client.schedule_key_deletion( KeyId=n['KeyId'] )
#                        log.info('deleting the keys')
#                        kms_response = kms_client.create_key(Description="testing key")
#                        log.info ('created key')
#                        Key_id=kms_response['KeyMetadata']['KeyId']
#                        kms_client.enable_key_rotation(KeyId=Key_id)
#                        log.info("Compliant and Delete")    
                    else:
                        log.info("No action taken compliantUpdate compliantDelete")
            elif rotationStatus['KeyRotationEnabled'] is True :
                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
                if "Default master key that protects my" not in str(keyDescription['KeyMetadata']['Description']):
                    print (n['KeyId'])
                    print (rotationStatus)
                    if varUserInput == 'nonCompliantUpdate':
                        kms_client.disable_key_rotation(KeyId=n['KeyId'])
                        log.info("NonCompliant and Update")
                    elif varUserInput == 'nonCompliantDelete':
                        log.info("Noncompliant and Delete")
                    else:
                        log.info("No action taken")
            else:
                log.info("No action 3")
        except Exception as e:
            print(e)


    


#print (keys['Keys'])
# Return the key ID and ARN
#Key_id=response['KeyMetadata']['KeyId']
#print (Key_id)
#
##====================================== Enable key rotation======================================
#
#response = kms_client.enable_key_rotation(
#    KeyId=Key_id
#)
