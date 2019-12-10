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

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

def get_cloudtrails(varDecision):
    trails = dict()
    for n in get_regions():
        client = boto3.client('cloudtrail', region_name=n)
        response = client.describe_trails()
        temp = []        
        for m in response['trailList']:
            if varDecision is None:
                if m['HomeRegion'] == n:
                    temp.append(m)
                if len(temp) > 0:
                    trails[n] = temp
            if varDecision is True:
                status = client.get_trail_status(Name=m['TrailARN'])
                if status['IsLogging'] is True and m['IsMultiRegionTrail'] == True:
                    if m['HomeRegion'] == n:
                        temp.append(m)
                        if len(temp) > 0:
                            trails[n] = temp
            elif varDecision is False:
                status = client.get_trail_status(Name=m['TrailARN'])
                if status['IsLogging'] is False or m['IsMultiRegionTrail'] == False:
                    if m['HomeRegion'] == n:
                        temp.append(m)
                        if len(temp) > 0:
                            trails[n] = temp

    return trails

#k=get_cloudtrails (False)
#print (k)
#for i in k:
#    print (k)

def func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,varDecision):
    print (varHomeRegion)
    client = boto3.client('cloudtrail', region_name=varHomeRegion)
    response = client.get_trail_status(Name=varTrailARN)
    if varDecision == False:
        log.info('Updateing the cloud trail resources as non-compliant')
        try:
                response=client.update_trail(
                    Name = varTrailARN,
                    IsMultiRegionTrail=False
                        )
                return response
        except Exception as e:
            print(e)
    elif varDecision == True:
        log.info('Updateing the cloud trail resources as compliant')
        try:
            response=client.update_trail(
                    Name = varTrailARN,
                    IsMultiRegionTrail=True,
                    IncludeGlobalServiceEvents=True
                    )
            response1=client.start_logging(
                    Name=varTrailARN
                    )
            return response
        except Exception as e:
            print(e)

def func_delete_cloudTrail():
    cloud_trails = get_cloudtrails(None)
    if cloud_trails:
        for i in cloud_trails:
            for j in  cloud_trails[i]:
                varHomeRegion = j['HomeRegion']
                varTrailARN = j['TrailARN']
                try:
                    cloudTrail = boto3.client('cloudtrail', region_name=varHomeRegion)
                    response = cloudTrail.delete_trail(Name = varTrailARN)
                    #if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    #    varFlag = True
                    #else:
                    #    varFlag = False
                except Exception as e:
                    print (e)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            log.info('Deletion performed successfully')
        else:
            log.error('Error occoured wile deleting the Cloudtrail')
    else:
        log.info("Cloudtrail resource does not exist")
        sys.exit()

if varUserInput == 'nonCompliantUpdate':
    log.info('The user request is to make resources non-compliant')
    log.info("Gathering information for compliant resources")
    varCompliant=get_cloudtrails(True)
    print (varCompliant)
    if varCompliant:
        for i in varCompliant:
            for j in  varCompliant[i]:
                print (j)
                varHomeRegion = j['HomeRegion']
                print(j['HomeRegion'])
                varTrailARN = j['TrailARN']
                response=func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,False)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info("Operation non-compliant update performed sucessfully")
    else:
        log.info("compliant resources does not exist")

if varUserInput == 'compliantUpdate':
    log.info('The user request is to make resources compliant')
    log.info("Gathering information for non-compliant resources")
    varNon_compliant=get_cloudtrails(False)
    if varNon_compliant:
        for i in varNon_compliant:
            for j in  varNon_compliant[i]:
                print(j)
                varHomeRegion = j['HomeRegion']
                varTrailARN = j['TrailARN']
                response=func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,True)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info("Operation compliant update performed sucessfully")
    else:
        log.info("non-compliant resources does not exist")

elif varUserInput == 'compliantDelete':
    log.info('The user request is to delete existing resource/resources and create a compliant resource')
    func_delete_cloudTrail()
    varFlag = True

elif varUserInput == 'nonCompliantDelete':
    log.info('The user request is to delete existing resource/resources and create a non-compliant resource')
    func_delete_cloudTrail()
    varFlag = False

elif varUserInput == 'createcompliant':
    log.info('The user request is to create a compliant resource')
    varFlag = True
elif varUserInput == "createnoncompliant":
    log.info('The user request is to create a non-compliant resource')
    varFlag = False

if varFlag is True:
    log.info('Creating a compliant resource')
    response=func_create_non_comp_cloudTrail()
    print (response['TrailARN'])
    Arn = response['TrailARN']
    response1=cloudTrail.update_trail(
            Name = Arn,
            IsMultiRegionTrail=True,
            IncludeGlobalServiceEvents=True
            )
    response2=cloudTrail.start_logging(
            Name=Arn
            )
    if response1['ResponseMetadata']['HTTPStatusCode'] == 200 and response2['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info('Compliant resource is created')

elif varFlag is False:
    log.info('Creating a compliant resource')
    response=func_create_non_comp_cloudTrail()
    if response1['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info('Compliant resource is created')
else:
    #func_reset_config()
    sys.exit()
