#!/usr/bin/python

import boto3
import json
import sys
import os.path
from os import path
sys.path.insert(0, '../')
from common import *

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

def get_cloudtrails():
    trails = dict()
    for n in get_regions():
        client = boto3.client('cloudtrail', region_name=n)
        response = client.describe_trails()
        temp = []
        for m in response['trailList']:
            if m['HomeRegion'] == n:
                temp.append(m)
        if len(temp) > 0:
            trails[n] = temp
    return trails

def func_validate_compliant_or_not(varDecision):
    cloud_trails = get_cloudtrails()
    trails = dict()
    temp = []
    if cloud_trails:
        for i in cloud_trails:
            for j in  cloud_trails[i]:
                if (j['LogFileValidationEnabled']) is varDecision:
                    temp.append(j)
                    trails = temp
        return trails
    else:
        log.info("Cloudtrail resource does not exist")
        sys.exit()

def func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,varDecision):
    cloudTrail = boto3.client('cloudtrail', region_name=varHomeRegion)
    response=cloudTrail.update_trail(
            Name=varTrailARN,
            EnableLogFileValidation=varDecision
            )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if varDecision == True:
            log.info('Resourse "' +varTrailARN+ '" updated as compliant')
        elif varDecision == False:
            log.info('Resourse "' +varTrailARN+ '" updated as non-compliant')
        else:
            log.info('Error occoured while updating resources')

def func_delete_cloudTrail():
    cloud_trails = get_cloudtrails()
    if cloud_trails:
        for i in cloud_trails:
            for j in  cloud_trails[i]:
                varHomeRegion = j['HomeRegion']
                varTrailARN = j['TrailARN']
                try:
                    cloudTrail = boto3.client('cloudtrail', region_name=varHomeRegion)
                    response = cloudTrail.delete_trail(Name = varTrailARN)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        log.info('Resourse "' +varTrailARN+ '" is deleted')
                    elif response['ResponseMetadata']['HTTPStatusCode'] != 200:
                        log.info('Error occoured while deleting the resource')
                except Exception as e:
                    print (e)
    else:
        log.info("Cloudtrail resource does not exist")
        sys.exit()

if varUserInput == 'nonCompliantUpdate':
    log.info('The user request is to make resources non-compliant')
    log.info("Gathering information for compliant resources")
    compliant=func_validate_compliant_or_not(True)
    if compliant:
        for j in compliant:
            varHomeRegion = j['HomeRegion']
            varTrailARN = j['TrailARN']
            func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,False)
    else:
        log.info("compliant resources does not exist")

elif varUserInput == 'compliantUpdate':
    log.info('The user request is to make resources compliant')
    log.info("Gathering information for non-compliant resources")
    non_compliant=func_validate_compliant_or_not(False)
    if non_compliant:
        for j in non_compliant:
            varHomeRegion = j['HomeRegion']
            varTrailARN = j['TrailARN']
            func_update_compliant_or_non_compliant(varHomeRegion,varTrailARN,True)
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
    log.info('Creating a compliant cloudtrail resource')
    i=func_create_non_comp_cloudTrail()
    print (i['TrailARN'])
    Arn = i['TrailARN']
    response=cloudTrail.update_trail(
            Name = Arn,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True
            )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info('Resourse "' +Arn+ '" is created')
elif varFlag is False:
    log.info('Creating a non-compliant cloudtrail resource')
    i=func_create_non_comp_cloudTrail()
    Arn = i['TrailARN']
    response=cloudTrail.update_trail(
            Name = Arn,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=False
            )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log.info('Resourse "' +Arn+ '" is created')
