#!/usr/bin/python

import boto3
import json

# Create a bucket policy
s3 = boto3.client('s3')
response = s3.create_bucket(
    ACL='private',
    Bucket='gov-gvmmgmkfvmf123',
    )

bucket_name = 'gov-gvmmgmkfvmf123'

s3.put_public_access_block(
    Bucket='gov-gvmmgmkfvmf123',
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
#        'IgnorePublicAcls': True|False,
        'BlockPublicPolicy': True,
#        'RestrictPublicBuckets': True|False
    }
)

# Create the bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::gov-gvmmgmkfvmf123"
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::gov-gvmmgmkfvmf123/*",
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
        }
    ]
}

# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

cTrail   = boto3.client('cloudtrail')
response2 = cTrail.describe_trails()
print (response2)

cTrail.create_trail(
    Name='govs6',
    S3BucketName=bucket_name,
    IncludeGlobalServiceEvents=True,
    IsMultiRegionTrail=True,
#    EnableLogFileValidation=True|False,
#    CloudWatchLogsLogGroupArn='string',
#    CloudWatchLogsRoleArn='string',
#    KmsKeyId='string',
#    IsOrganizationTrail=True|False
)
