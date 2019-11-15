#!/usr/bin/python

import boto3
import json

# Create a bucket policy
s3 = boto3.client('s3')
response = s3.create_bucket(
    ACL='public-read-write',
    Bucket='gov-kms',
    )

bucket_name = 'gov-kms'

# Create the bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::gov-kms"
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::gov-kms/*",
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
        }
    ]
}

# Cloudtrail Encrypt policy

encrypt_policy = {
  "Version": "2012-10-17",
  "Statement": [{
              "Sid": "Enable CloudTrail Encrypt Permissions",
              "Effect": "Allow",
              "Principal": {
              "Service": "cloudtrail.amazonaws.com"
                    },
               "Action": "kms:GenerateDataKey*",
                 "Resource": "*",
                   "Condition": {
                     "StringLike": {
                       "kms:EncryptionContext:aws:cloudtrail:arn": [
                         "arn:aws:cloudtrail:*:998488308670:trail/*",
                              ]
                              }
                              }
                             }]
                              }

# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)
encrypt_policy = json.dumps(encrypt_policy)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

cTrail   = boto3.client('cloudtrail')
response2 = cTrail.describe_trails()
print (response2)

#=================================================KMS KEY ID=======================================================

kms_client = boto3.client('kms')
response = kms_client.create_key(Description="testing1")

    # Return the key ID and ARN
Key_id=response['KeyMetadata']['KeyId']
print (Key_id)

#=================================================Attach Policy========================================================

policy_response = kms_client.put_key_policy(
    KeyId=Key_id,
    PolicyName='default',
    Policy=encrypt_policy,
)

#=================================================Enabling KMS for CloudTrail=======================================

cTrail.create_trail(
     Name='govs-kms',
     S3BucketName=bucket_name,
     IncludeGlobalServiceEvents=True,
     IsMultiRegionTrail=True,
#    EnableLogFileValidation=True|False,
#    CloudWatchLogsLogGroupArn='string',
#    CloudWatchLogsRoleArn='string',
     KmsKeyId=Key_id,
#    IsOrganizationTrail=True|False
)
