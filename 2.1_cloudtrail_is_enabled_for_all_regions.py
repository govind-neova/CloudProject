#!/usr/bin/python

import boto3
import json
from common import *
import sys

#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]

#Global variables
client = boto3.client('cloudtrail')
varFlag = ''
log.info('Gathering information for regions')
data = get_regions()
if data:
    log.info('Ragion list stored in a variable')
else:
    log.error('Unable to fetch list of regions')
    sys.exit()

def func_cloudTrails_details_compliant ():
    log.info("Gathering information for compliant resources")
    for i in data:
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            homeRegion = cloudTrail_response['trailList']
            for k in cloudTrail_response['trailList']:
                if k:
                    response = cloudTrail.get_trail_status(Name=k['TrailARN'])
                    if (k['IsMultiRegionTrail']) is True and (response['IsLogging']) is True:
                        yield (k)

#Function describing non-compliant Cloudtrails
def func_cloudTrails_details_nonCompliant ():
    log.info("Gathering information for non-compliant resources")
    for i in data:
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            homeRegion = cloudTrail_response['trailList']
            for k in cloudTrail_response['trailList']:
                if k:
                    response = cloudTrail.get_trail_status(Name=k['TrailARN'])
                    if (k['IsMultiRegionTrail']) is False or (response['IsLogging']) is False:
                        yield (k)

#If loop for performing operations on Cloudtrails as per config.yaml file
log.info("Performing user input validation")
if varUserInput == 'nonCompliantUpdate':
    log.info('The user request is to make resources compliant')
    for value in func_cloudTrails_details_compliant ():
        #print (value)
        homeRegion=value['HomeRegion']
        #print (homeRegion)
        cloudTrailArn=value['TrailARN']
        #print (value['TrailARN'])
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        try:
            response1=cloudTrail.update_trail(
                    Name = cloudTrailArn,
                    IsMultiRegionTrail=False
                    )
            response2=cloudTrail.stop_logging(
                    Name=cloudTrailArn
                    )
            if response1['ResponseMetadata']['HTTPStatusCode'] == 200 and response2['ResponseMetadata']['HTTPStatusCode'] == 200:
                log.info('Resources are made non-compliant successfully')
            else:
                log.info('Compliant resource/resources not found')
        except Exception as e:
            if e.response['Error']['Code'] == 'S3BucketDoesNotExistException':
                log.error ("No bucket is configured for above cloudtrail therefore operation can't be performed")
                pass

elif varUserInput == 'compliantUpdate':
    log.info('The user request is to make resources non-compliant')
    for value in func_cloudTrails_details_nonCompliant ():
        print (value)
        homeRegion=value['HomeRegion']
        cloudTrailArn=value['TrailARN']
        s3BucketName=value['S3BucketName']
        print (homeRegion)
        print (cloudTrailArn)
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        try:
            response1=cloudTrail.update_trail(
                    Name = cloudTrailArn,
                    IsMultiRegionTrail=True,             
                    IncludeGlobalServiceEvents=True
                    )
            response2=cloudTrail.start_logging(
                    Name=cloudTrailArn
                    )
            if response1['ResponseMetadata']['HTTPStatusCode'] == 200 and response2['ResponseMetadata']['HTTPStatusCode'] == 200:
                log.info('Resources are made compliant successfully')
            else:
                log.info('Non-compliant resource/resources not found')
        except Exception as e:
            if e.response['Error']['Code'] == 'S3BucketDoesNotExistException':
                log.error ("No bucket is configured for above bucket therefore operation can't be performed")
                pass

elif varUserInput == 'compliantDelete':
    log.info('The user request is to delete existing resource/resources and create a compliant resource')
    for value in func_cloudTrails_resources_details ():
        print (value)
        cloudTrailArn=value['TrailARN']
        homeRegion=value['HomeRegion']
        try:
            cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
            response = cloudTrail.delete_trail(Name = cloudTrailArn)
        except Exception as e:
            print (e)
            continue
    varFlag = False

elif varUserInput == 'nonCompliantDelete':
    log.info('The user request is to delete existing resource/resources and create a non-compliant resource')
    for value in func_cloudTrails_resources_details ():
        print (value)
        cloudTrailArn=value['TrailARN']
        homeRegion=value['HomeRegion']
        try:
            cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
            response = cloudTrail.delete_trail(Name = cloudTrailArn)
        except Exception as e:
            print (e)
            continue
    varFlag = False

elif varUserInput == 'createcompliant':
    log.info('The user request is to create a compliant resource')
    varFlag = True
elif varUserInput == "createnoncompliant":
    log.info('The user request is to create a non-compliant resource')
    varFlag = False

if varFlag is True:
    log.info('Creating a non-compliant resource')
    i=func_create_non_comp_cloudTrail()
    print (i['TrailARN'])
    Arn = i['TrailARN']
    cloudTrail.update_trail(
            Name = Arn,
            IsMultiRegionTrail=True,
            IncludeGlobalServiceEvents=True
            )
    cloudTrail.start_logging(
            Name=Arn
            )
elif varFlag is False:
    log.info('Creating a compliant resource')
    func_create_non_comp_cloudTrail()
else:
    #func_reset_config()
    sys.exit()
