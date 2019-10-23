#!/usr/bin/python

import boto3
import json

s3 = boto3.client('s3')
s3.create_bucket(
    ACL='public-read-write',
    Bucket='ashdhcbeuirbcsbdcb'
)

bucket_name = 'ashdhcbeuirbcsbdcb'

bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': "arn:aws:s3:::%s/*" % bucket_name
    }]
}


bucket_policy = json.dumps(bucket_policy)

s3.put_bucket_policy(
    Bucket=bucket_name,
    ConfirmRemoveSelfBucketAccess=True,
    Policy='bucket_policy'
)
    
cTrail   = boto3.client('cloudtrail')
response2 = cTrail.describe_trails()
print (response2)

cTrail.create_trail(
    Name='govs1',
    S3BucketName=bucket_name,
    IncludeGlobalServiceEvents=True,
    IsMultiRegionTrail=True,
#    EnableLogFileValidation=True|False,
#    CloudWatchLogsLogGroupArn='string',
#    CloudWatchLogsRoleArn='string',
#    KmsKeyId='string',
#    IsOrganizationTrail=True|False
)
