#!/usr/bin/python

import boto3
import json
import sys
import os.path
from os import path
sys.path.insert(0, '../')
from common import *

#Global variables
client = boto3.client('cloudtrail')
varFlag = ''
varResources = []

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

def func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,varDecision):
    #print (varHomeRegion)
    client = boto3.client('cloudtrail', region_name=varHomeRegion)
    response = client.get_trail_status(Name=varTrailARN)
    if varDecision == False:
        log.info('Updateing the cloud trail resources as non-compliant')
        try:
                response=client.update_trail(
                    Name = varTrailARN,
                    IsMultiRegionTrail=False
                        )
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    log.info('Resourse "'  +varTrailARN+  '" made non-compliant')
                else:
                    log.error('Error occoured while performing non-compliant update')
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
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response1['ResponseMetadata']['HTTPStatusCode'] == 200:
                log.info('Resourse "' +varTrailARN+ '" made compliant')
            else:
                log.error('Error occoured while performing compliant update')
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
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        log.info('Resourse "' +varTrailARN+ '" id deleted')
                except Exception as e:
                    print (e)
    else:
        log.info("Cloudtrail resource does not exist")
        sys.exit()

if func_user_input_validation() == 'nonCompliantUpdate':
    log.info('The user request is to make resources non-compliant')
    log.info("Gathering information for compliant resources")
    varCompliant=get_cloudtrails(True)
    #print (varCompliant)
    if varCompliant:
        for i in varCompliant:
            for j in  varCompliant[i]:
                #print (j)
                varHomeRegion = j['HomeRegion']
                #print(j['HomeRegion'])
                varTrailARN = j['TrailARN']
                response=func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,False)
    else:
        log.info("compliant resources does not exist")

if func_user_input_validation() == 'compliantUpdate':
    log.info('The user request is to make resources compliant')
    log.info("Gathering information for non-compliant resources")
    varNon_compliant=get_cloudtrails(False)
    if varNon_compliant:
        for i in varNon_compliant:
            for j in  varNon_compliant[i]:
                #print(j)
                varHomeRegion = j['HomeRegion']
                varTrailARN = j['TrailARN']
                response = func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,True)
                #print (response)
    else:
        log.info("non-compliant resources does not exist")

elif func_user_input_validation() == 'compliantDelete':
    log.info('The user request is to delete existing resource/resources and create a compliant resource')
    func_delete_cloudTrail()
    varFlag = True

elif func_user_input_validation() == 'nonCompliantDelete':
    log.info('The user request is to delete existing resource/resources and create a non-compliant resource')
    func_delete_cloudTrail()
    varFlag = False

elif func_user_input_validation() == 'createcompliant':
    log.info('The user request is to create a compliant resource')
    varFlag = True
elif func_user_input_validation() == "createnoncompliant":
    log.info('The user request is to create a non-compliant resource')
    varFlag = False

if varFlag is True:
    log.info('Creating a compliant resource')
    response=func_create_non_comp_cloudTrail()
    #print (response['TrailARN'])
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
        log.info('Resourse "' +Arn+ '" is created')

elif varFlag is False:
    log.info('Creating a compliant resource')
    response=func_create_non_comp_cloudTrail()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info('Resourse "' +response['TrailARN']+ '" is created')

#Writing changes to json file
log.info("Writing changes to json file")
func_write_to_json(varResources)
varFile = sys.argv[0]
varFile = varFile[:-2]
if (path.exists(varFile+ ".json")) is True :
    log.info("Changes have been written to json file")
else:
    log.error("Json file is not created")
