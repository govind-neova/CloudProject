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
cloudTrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')

#Variable function to fetch regions and bucket names
def func_variables ():
    with open('./variable.json') as f:
        data = json.load(f)
        bucket = (data['Bucket'])
        cloudTrail_name = (data['cloudTrail'])
        return data

data = func_variables ()
print (data)

bucket = (data['Bucket'])
cloudTrail_name = (data['cloudTrail'])

#Function cloudtrail to create non comliant cloud Trail
def func_create_nonCompCloudTrail ():

    bucket = (data['Bucket'])
    cloudTrail_name = (data['cloudTrail'])

    try:

        # Create a bucket policy
        s3 = boto3.client('s3')
        response = s3.create_bucket(
            ACL='public-read-write',
            Bucket=bucket
            )

        # Create the bucket policy and convert to json
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck20150319",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::%s" % bucket
                },
                {
                    "Sid": "AWSCloudTrailWrite20150319",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::%s/*" % bucket ,
                    "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
                }
            ]
        }

        bucket_policy = json.dumps(bucket_policy)


        ## Set the new policy on the given bucket
        s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)

        cloudTrail_response=cloudTrail.create_trail(
            Name=cloudTrail_name,
            S3BucketName=bucket,
            IncludeGlobalServiceEvents=True,
        #    IsMultiRegionTrail=True
        #    EnableLogFileValidation=True|False,
        #    CloudWatchLogsLogGroupArn='string',
        #    CloudWatchLogsRoleArn='string',
        #    KmsKeyId='string',
        #    IsOrganizationTrail=True|False
        )

        yield cloudTrail_response

    except Exception as e:
        print (e)

#Function describing compliant Cloudtrails
def func_logFileValidation_details_compliant ():
    for i in data['region']:
        client = boto3.client('cloudtrail')
        cloudTrail = boto3.client('cloudtrail', region_name=i)
        cloudTrail_response = cloudTrail.describe_trails()
#        print (cloudTrail_response['trailList'])
        if cloudTrail_response['trailList']:
#            print cloudTrail_response['trailList']
            for j in cloudTrail_response['trailList']:
#                print (j['TrailARN'])
#                print (j['LogFileValidationEnabled'])
                if (j['LogFileValidationEnabled']) is True:
                    yield (j)
                    

def func_logFileValidation_details_nonCompliant ():
    for i in data['region']:
        client = boto3.client('cloudtrail')
        cloudTrail = boto3.client('cloudtrail', region_name=i)
        cloudTrail_response = cloudTrail.describe_trails()
        if cloudTrail_response['trailList']:
            for j in cloudTrail_response['trailList']:
                if (j['LogFileValidationEnabled']) is False:
                    yield (j)

def func_logFileValidation_details_list ():
    for i in data['region']:
        client = boto3.client('cloudtrail')
        cloudTrail = boto3.client('cloudtrail', region_name=i)
        cloudTrail_response = cloudTrail.describe_trails()
        for j in cloudTrail_response['trailList']:
            yield (j)


#If loop for performing operations on Cloudtrails as per config.yaml file
if varUserInput == 'nonCompliantUpdate':
    log.info('Non-compliant and Update')
    for value in func_logFileValidation_details_compliant ():
        print (value)
        homeRegion=value['HomeRegion']
        cloudTrailArn=value['TrailARN']
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        cloudTrail.update_trail(
                Name=value['TrailARN'],
                EnableLogFileValidation=False
                )
    
    func_create_nonCompCloudTrail ()

elif varUserInput == 'compliantUpdate':
    log.info('Compliant and Update')
    for value in func_logFileValidation_details_nonCompliant ():
        print (value)
        homeRegion=value['HomeRegion']
        cloudTrailArn=value['TrailARN']
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        cloudTrail.update_trail(
                Name=value['TrailARN'],
                EnableLogFileValidation=True
                )

    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        Arn = i['TrailARN']
        cloudTrail.update_trail(
            Name = Arn,
            EnableLogFileValidation=True
            )

elif varUserInput == 'compliantDelete':
    log.info('Compliant and Delete')
    for value in func_logFileValidation_details_list ():
        cloudTrailArn=value['TrailARN']
        print (cloudTrailArn)
        homeRegion=value['HomeRegion']
        print (homeRegion)
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        response = cloudTrail.delete_trail(Name = cloudTrailArn)
        print (response)

    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        Arn = i['TrailARN']
        cloudTrail.update_trail(
            Name = Arn,
            EnableLogFileValidation=True
            )

elif varUserInput == 'nonCompliantDelete':
    log.info('Non-compliant and Delete')
    for value in func_logFileValidation_details_list ():
        cloudTrailArn=value['TrailARN']
        homeRegion=value['HomeRegion']
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        response = cloudTrail.delete_trail(Name = cloudTrailArn)
   
    func_create_nonCompCloudTrail ()
