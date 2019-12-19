#!/usr/bin/python

import boto3
import json
import sys
import os.path
from os import path
sys.path.insert(0, '../')
from common import *

#for n in get_regions():
#    func_create_config()

def func_create_config():

    # Create IAM client
    iam = boto3.client('iam')
    #role_name = funcResName("Config","Role")
    
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
        #PolicyArn='arn:aws:iam::aws:policy/service-role/AWSConfigRole',
        PolicyArn='arn:aws:iam::aws:policy/service-role/%s' % role_name,
        #RoleName='AwsconfigRole',
        RoleName=role_name,
    )
    
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    print(response)
    
    response2 = iam.get_role(
        #RoleName='AwsConfigRole'
        RoleName=role_name
    )
    
    iam_arn = response2["Role"]["Arn"]
    print (iam_arn)
    
    #=============================================S3 BUCKET=============================================
    
    # Create a bucket policy
    bucket = funcResName("s3","bucket")
    s3 = boto3.client('s3')
    response = s3.create_bucket(
        ACL='public-read-write',
        #Bucket='gov-config-aws1',
        Bucket=bucket,
        )
    
    #bucket_name = 'gov-config-aws1'
    
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
          "Resource": "arn:aws:s3:::%s" % bucket
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
          #"Resource": "arn:aws:s3:::gov-config-aws1"
          "Resource": "arn:aws:s3:::%s" % bucket
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
          #"Resource": "arn:aws:s3:::gov-config-aws1/AWSLogs/998488308670/Config/*",
          "Resource": "arn:aws:s3:::%s/AWSLogs/998488308670/Config/*" % bucket,
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
    s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
    
    #=====================================================SNS TOPIC==============================================================
    
    sns = boto3.client('sns')
    sns_name = funcResName("sns","topic")

    sns_response = sns.create_topic(
        #Name='config-sns-topic2',
        Name=sns_name,
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
    name = funcResName("config","recorder")
    try:
        response3 = config.put_configuration_recorder(
        ConfigurationRecorder={
               #'name': 'default',
               'name': name,
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
            #'name': 'default',
            'name': name,
            #'s3BucketName': 'gov-config-aws1',
            's3BucketName': bucket,
            'snsTopicARN': sns_arn,
            'configSnapshotDeliveryProperties': {
                'deliveryFrequency': 'One_Hour'
            }
        }
    )


for n in get_regions():
    func_create_config()
