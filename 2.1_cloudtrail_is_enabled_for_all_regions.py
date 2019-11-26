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

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    data = [region['RegionName'] for region in region_response['Regions']]
    yield data

data = get_regions()

bucket = funcResName("s3","bucket")
print (bucket)
cloudTrail_name = funcResName("cloudTrail","trail")
print (cloudTrail_name)

#def func_create_non_comp_cloudTrail():
#    try:
#        # Create a bucket policy
#        s3 = boto3.client('s3')
#        response = s3.create_bucket(
#            ACL='public-read-write',
#            Bucket=bucket
#            )
#        
#    except Exception as e:
#        print (e)
#
#    try:
#        # Create the bucket policy and convert to json
#        bucket_policy = {
#            "Version": "2012-10-17",
#            "Statement": [
#                {
#                    "Sid": "AWSCloudTrailAclCheck20150319",
#                    "Effect": "Allow",
#                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
#                    "Action": "s3:GetBucketAcl",
#                    "Resource": "arn:aws:s3:::%s" % bucket
#                },
#                {
#                    "Sid": "AWSCloudTrailWrite20150319",
#                    "Effect": "Allow",
#                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
#                    "Action": "s3:PutObject",
#                    "Resource": "arn:aws:s3:::%s/*" % bucket ,
#                    "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
#                }
#            ]
#        }
#        
#        bucket_policy = json.dumps(bucket_policy)
#    
#        ## Set the new policy on the given bucket
#        s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
#        
#        cloudTrail.create_trail(
#            Name=cloudTrail_name,
#            S3BucketName=bucket,
#            IncludeGlobalServiceEvents=True,
#        #    IsMultiRegionTrail=True
#        #    EnableLogFileValidation=True|False,
#        #    CloudWatchLogsLogGroupArn='string',
#        #    CloudWatchLogsRoleArn='string',
#        #    KmsKeyId='string',
#        #    IsOrganizationTrail=True|False
#        )
#        
#        cloudTrail.start_logging(
#            Name=cloudTrail_name
#                        )
#    except Exception as e:
#        print (e)
#
#func_create_non_comp_cloudTrail()    

def func_cloudTrails_details_compliant ():
    for i in data:
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            homeRegion = cloudTrail_response['trailList']
            for k in cloudTrail_response['trailList']:
                response = cloudTrail.get_trail_status(Name=k['TrailARN'])
                if (k['IsMultiRegionTrail']) is True and (response['IsLogging']) is True:
                    yield (k)

#Function describing non-compliant Cloudtrails
def func_cloudTrails_details_nonCompliant ():
    for i in data:
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            homeRegion = cloudTrail_response['trailList']
            for k in cloudTrail_response['trailList']:
                response = cloudTrail.get_trail_status(Name=k['TrailARN'])
                if (k['IsMultiRegionTrail']) is False or (response['IsLogging']) is False:
                    yield (k)

##Function describing All Cloudtrails in all regions
def func_cloudTrails_resources_details ():
    for i in data:
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            for k in cloudTrail_response['trailList']:
                yield (k)

#If loop for performing operations on Cloudtrails as per config.yaml file
if varUserInput == 'nonCompliantUpdate':
    log.info('Non-compliant and Update')
    for value in func_cloudTrails_details_compliant ():
        print (value)
        homeRegion=value['HomeRegion']
        print (homeRegion)
        cloudTrailArn=value['TrailARN']
        print (value['TrailARN'])
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        cloudTrail.update_trail(
                Name = cloudTrailArn,
                IsMultiRegionTrail=False
                )
        cloudTrail.stop_logging(
                Name=cloudTrailArn
                )
    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        print i['TrailARN']

elif varUserInput == 'compliantUpdate':
    log.info('Compliant and Update')
    for value in func_cloudTrails_details_nonCompliant ():
        print (value)
        homeRegion=value['HomeRegion']
        cloudTrailArn=value['TrailARN']
        s3BucketName=value['S3BucketName']
        print (homeRegion)
        print (cloudTrailArn)
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        cloudTrail.update_trail(
                Name = cloudTrailArn,
                IsMultiRegionTrail=True,             
                IncludeGlobalServiceEvents=True
                )
        cloudTrail.start_logging(
                Name=cloudTrailArn
                )
    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        print i['TrailARN']
        Arn = i['TrailARN']
        cloudTrail.update_trail(
                Name = Arn,
                IsMultiRegionTrail=True,
                IncludeGlobalServiceEvents=True
                )
        cloudTrail.start_logging(
                Name=Arn
                )

elif varUserInput == 'compliantDelete':
    log.info('Compliant and Delete')
    for value in func_cloudTrails_resources_details ():
        print (value)
        cloudTrailArn=value['TrailARN']
        homeRegion=value['HomeRegion']
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        response = cloudTrail.delete_trail(Name = cloudTrailArn)
    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        print i['TrailARN']
        Arn = i['TrailARN']
        cloudTrail.update_trail(
                Name = Arn,
                IsMultiRegionTrail=True,
                IncludeGlobalServiceEvents=True
                )
        cloudTrail.start_logging(
                Name=Arn
                )

elif varUserInput == 'nonCompliantDelete':
    log.info('nonCompliant and Delete')
    for value in func_cloudTrails_resources_details ():
        print (value)
        cloudTrailArn=value['TrailARN']
        homeRegion=value['HomeRegion']
        cloudTrail = boto3.client('cloudtrail', region_name=homeRegion)
        response = cloudTrail.delete_trail(Name = cloudTrailArn)
    func_create_nonCompCloudTrail ()

elif varUserInput == 'createcompliant':
    func_create_nonCompCloudTrail ()
    for i in func_create_nonCompCloudTrail ():
        print i['TrailARN']
        Arn = i['TrailARN']
        cloudTrail.update_trail(
                Name = Arn,
                IsMultiRegionTrail=True,
                IncludeGlobalServiceEvents=True
                )
        cloudTrail.start_logging(
                Name=Arn
                )
elif varUserInput == "createnoncompliant":
    func_create_nonCompCloudTrail ()

