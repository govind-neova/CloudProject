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
                status = kms_client.describe_key(KeyId=i['KeyId'])
                if (status['KeyMetadata']['Enabled']) is True:
                    yield i
#                    print (status['KeyMetadata']['Enabled'])
        except Exception as e:
            print(e)
              
kmsKeys_compliant = func_kmsKeys_details_compliant ()

#Function describing non-compliant kmsKeys
def func_kmsKeys_details_nonCompliant ():
    for i in kms_response['Keys']:
        try:
            keyState = kms_client.describe_key(KeyId=i['KeyId'])
            if "PendingDeletion" not in str(keyState['KeyMetadata']['KeyState']) and "Default master key that protects my" not in str(keyState['KeyMetadata']['Description']):
                status = kms_client.describe_key(KeyId=i['KeyId'])
                if (status['KeyMetadata']['Enabled']) is False:
                    yield (i['KeyId'])
                    print (status['KeyMetadata']['Enabled'])
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


#If loop for performing operations on Cloudtrails as per config.yaml file
if varUserInput == 'nonCompliantUpdate':
    log.info('Non-compliant and Update')
    for value in func_kmsKeys_details_compliant ():
        print (value['KeyArn'])
        kms_client.disable_key_rotation(KeyId=value['KeyId'])
kms_response = kms_client.create_key(Description="cis-testing-key")
print (kms_response)
#elif varUserInput == 'compliantUpdate':
#    log.info('Compliant and Update')
#    for value in func_cloudTrails_details_nonCompliant ():
#        print (value)
#        homeRegion=value['HomeRegion']
#        cloudTrailArn=value['TrailARN']
#        s3BucketName=value['S3BucketName']
#        print (homeRegion)
#        print (cloudTrailArn)
#        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
#        cloudTrail.update_trail(
#                Name = cloudTrailArn,
#                IsMultiRegionTrail=True,             
#                IncludeGlobalServiceEvents=True
#                )
#        cloudTrail.start_logging(
#                Name=cloudTrailArn
#                )
#elif varUserInput == 'compliantDelete':
#    log.info('Compliant and Delete')
#    for value in func_cloudTrails_resources_details ():
#        print (value)
#        cloudTrailArn=value['TrailARN']
#        homeRegion=value['HomeRegion']
#        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
#        response = cloudTrail.delete_trail(Name = cloudTrailArn)
#elif varUserInput == 'nonCompliantDelete':
#    log.info('Compliant and Delete')
#    for value in func_cloudTrails_resources_details ():
#        print (value)
#        cloudTrailArn=value['TrailARN']
#        homeRegion=value['HomeRegion']
#        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
#        response = cloudTrail.delete_trail(Name = cloudTrailArn)


#paginator = kms_client.get_paginator('list_keys')
#response_iterator = paginator.paginate()
#for page in response_iterator:
#    for n in page['Keys']:
#        try:
#            rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
##            print (n['KeyId'])
#            if rotationStatus['KeyRotationEnabled'] is False :
#                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
#                if "Default master key that protects my" not in str(keyDescription['KeyMetadata']['Description']):
#                    print (n['KeyId'])
#                    print (rotationStatus)
#                    if varUserInput == 'compliantUpdate':
#                        kms_client.enable_key_rotation(KeyId=n['KeyId'])
#                        log.info("Compliant and Update")
#                    elif varUserInput == 'compliantDelete':
#                        kms_client.schedule_key_deletion( KeyId=n['KeyId'] )
##                        log.info('deleting the keys')
##                        kms_response = kms_client.create_key(Description="testing key")
##                        log.info ('created key')
##                        Key_id=kms_response['KeyMetadata']['KeyId']
##                        kms_client.enable_key_rotation(KeyId=Key_id)
##                        log.info("Compliant and Delete")    
#                    else:
#                        log.info("No action taken compliantUpdate compliantDelete")
#            elif rotationStatus['KeyRotationEnabled'] is True :
#                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
#                if "Default master key that protects my" not in str(keyDescription['KeyMetadata']['Description']):
#                    print (n['KeyId'])
#                    print (rotationStatus)
#                    if varUserInput == 'nonCompliantUpdate':
#                        kms_client.disable_key_rotation(KeyId=n['KeyId'])
#                        log.info("NonCompliant and Update")
#                    elif varUserInput == 'nonCompliantDelete':
#                        log.info("Noncompliant and Delete")
#                    else:
#                        log.info("No action taken")
#            else:
#                log.info("No action 3")
#        except Exception as e:
#            print(e)

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
