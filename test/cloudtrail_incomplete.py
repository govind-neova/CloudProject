#!/usr/bin/python

import boto3
import json

import boto3, json

# Create IAM client
iam = boto3.client('iam')

path='/'
role_name='AwsconfigRole'
description='AwsconfigRole'

trust_policy={
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

tags=[
    {
        'Key': 'AwsconfigRole',
        'Value': 'AwsconfigRole'
    }
]


try:
    response = iam.create_role(
        Path=path,
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description=description,
        MaxSessionDuration=3600,
        Tags=tags
    )

    print(response)
except Exception as e:
    print(e)

response = iam.attach_role_policy(
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSConfigRole',
    RoleName='AwsconfigRole',
)

account_id = boto3.client('sts').get_caller_identity().get('Account')

print(response)

response2 = iam.get_role(
    RoleName='AwsConfigRole'
)

iam_arn = response2["Role"]["Arn"]
print (iam_arn)

#=============================================S3 BUCKET=============================================

# Create a bucket policy
s3 = boto3.client('s3')
response = s3.create_bucket(
    ACL='public-read-write',
    Bucket='gov-config-aws1',
    )

bucket_name = 'gov-config-aws1'

# Create the bucket policy
bucket_policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSConfigBucketPermissionsCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": [
         "config.amazonaws.com"
        ]
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::gov-config-aws1"
    },
    {
      "Sid": "AWSConfigBucketExistenceCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "config.amazonaws.com"
        ]
      },
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::gov-config-aws1"
    },
    {
      "Sid": " AWSConfigBucketDelivery",
      "Effect": "Allow",
      "Principal": {
        "Service": [
         "config.amazonaws.com"    
        ]
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::gov-config-aws1/AWSLogs/998488308670/Config/*",
      "Condition": { 
        "StringEquals": { 
          "s3:x-amz-acl": "bucket-owner-full-control" 
        }
      }
    }
  ]
}   

        
# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

#=====================================================SNS TOPIC==============================================================

sns = boto3.client('sns')

sns_response = sns.create_topic(
    Name='config-sns-topic2',
#    Attributes={
#        'string': 'sns'
#    },
    Tags=[
        {
            'Key': 'sns',
            'Value': 'sns'
        },
    ]
)

print (sns_response)

sns_arn = sns_response["TopicArn"]

print ("sns_arn = %s" %sns_arn)


#=============================================================================================================================

config = boto3.client('config')

try:
    response3 = config.put_configuration_recorder(
    ConfigurationRecorder={
           'name': 'default',
           'roleARN': iam_arn,
           'recordingGroup': {
               'allSupported': True,
               'includeGlobalResourceTypes': True
           }
       }
   )

except Exception as f:
    print(f)

#============================================SNS AND S3 Bucket===============================================================

config.put_delivery_channel(
    DeliveryChannel={
        'name': 'default',
        's3BucketName': 'gov-config-aws1',
        'snsTopicARN': sns_arn,
        'configSnapshotDeliveryProperties': {
            'deliveryFrequency': 'One_Hour'
        }
    }
)
