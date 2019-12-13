#!/usr/bin/python

import boto3
import json
from common import *
import sys

#def func_variables ():
#    with open('./variable.json') as f:
#        data = json.load(f)
#        bucket = (data['Bucket'])
#        cloudTrail_name = (data['cloudTrail'])
#        return data
#
#variables = func_variables ()
#print (variables)

#with open('./variable.json') as f:
#        data = json.load(f)
#        bucket = (data['Bucket'])
#        cloudTrail_name = (data['cloudTrail'])
#
#print (bucket)
#print (cloudTrail_name)


#Global variables
cloudTrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')

bucket = funcResName("s3","bucket")
print (bucket)
cloudTrail_name = funcResName("cloudTrail","trail")
print (cloudTrail_name)

def func_create_non_comp_cloudTrail():

    print ('hiiiiiiiii')
    # Create a bucket policy
    s3 = boto3.client('s3')
    response = s3.create_bucket(
        ACL='private',
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
    print ('1') 
    
    ## Set the new policy on the given bucket
    s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
    
    response=cloudTrail.create_trail(
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
    print ('2')
    cloudTrail.start_logging(
        Name=cloudTrail_name
                    )
    return response

func_create_non_comp_cloudTrail()    
