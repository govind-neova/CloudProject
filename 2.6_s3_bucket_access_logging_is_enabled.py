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
s3 = boto3.client('s3')
var_bucket_name = ''

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


def func_validate_s3_bkt_complianr_or_not(varDecision):
    buckets = dict()
    for n in get_regions():
        client = boto3.client('cloudtrail', region_name=n)
        response = client.describe_trails()
        S3_CLIENT = boto3.client('s3')
        temp = []
        for m in response['trailList']:
            if m['HomeRegion'] == n:
                #print (m['S3BucketName'])
                s3_response = S3_CLIENT.get_bucket_logging(Bucket=m['S3BucketName'])
                #print(s3_response)
                if varDecision is True:
                    if 'LoggingEnabled' in s3_response:
                        temp.append(m['S3BucketName'])
                elif varDecision is False:
                    if 'LoggingEnabled' not in s3_response:
                        temp.append(m['S3BucketName'])
        if len(temp) > 0:
            buckets[n] = temp
    return (buckets)    

def func_create_bucket(var_bucket_name,varRegion):
    region = varRegion
    print (region)
    if region == 'us-east-1':
        s3 = boto3.client('s3')
        bucket = var_bucket_name
        response = s3.create_bucket(
                ACL='log-delivery-write',
                Bucket=bucket
                )
    elif region != 'us-east-1' and ( region != 'eu-west-2' or region != 'eu-west-3' or region != 'eu-north-1' ):
        s3 = boto3.client('s3',region_name=region)
        bucket = var_bucket_name
        response = s3.create_bucket(
                ACL='log-delivery-write',
                CreateBucketConfiguration={
                    'LocationConstraint':region
                    },
                Bucket=bucket
                )
    elif region == 'eu-west-2' or region == 'eu-west-3' or region == 'eu-north-1':
        region = 'EU'
        s3 = boto3.client('s3',region_name=region)
        bucket = var_bucket_name
        response = s3.create_bucket(
                ACL='log-delivery-write',
                CreateBucketConfiguration={
                    'LocationConstraint':region
                    },
                Bucket=bucket
                )

    return response

if varUserInput == 'nonCompliantUpdate':
    log.info('Updating resources as non-compliant as per request')
    log.info("Gathering information for compliant resources")
    varCompliant=func_validate_s3_bkt_complianr_or_not(True)
    for i in varCompliant:
        for j in varCompliant[i]:
            print (j)
            #bucket_logging = s3.BucketLogging(j)
            s3_response = s3.put_bucket_logging(
                    Bucket=j,
                    BucketLoggingStatus={},
                    )
            print(s3_response)

elif varUserInput == 'compliantUpdate':
    log.info('Updating resources as compliant as per request')
    log.info("Gathering information for non-compliant resources")
    varNonCompliant=func_validate_s3_bkt_complianr_or_not(False)
    for i in varNonCompliant:
        for j in varNonCompliant[i]:
            var_bucket_name = funcResName("s3","bucket")
            print (var_bucket_name)
            varRegion = i
            s3_response1=func_create_bucket(var_bucket_name,varRegion)
            print(s3_response1)
            print (var_bucket_name)
            print (j)
            s3_response = s3.put_bucket_logging(
                    Bucket=j,
                    BucketLoggingStatus={
                        'LoggingEnabled': {
                        'TargetBucket' : var_bucket_name,
                        'TargetPrefix': 'user/'
                        }
                    },
                )
            print(s3_response)

elif varUserInput == 'compliantDelete' or varUserInput == 'nonCompliantDelete' :   
    log.error("Deletion does not apply to this process.")

elif varUserInput == 'createcompliant' or varUserInput == "createnoncompliant":
    log.error("Creation does not apply to this process")

