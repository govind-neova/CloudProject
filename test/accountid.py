#!/usr/bin/python

import boto3
import json

#account_id = boto3.client('sts').get_caller_identity().get('Account')
#print (account_id)

#try:
#ARN = account_id
#   print(ARN)
 
#except Exception as f:
#    print(f)

#client = boto3.client('iam')

#response = client.get_role(
#    RoleName='AwsConfigRole'
#)

#print (response)

#ARN = response["Role"]["Arn"]
#print (ARN)

#================================================================================

#sns = boto3.client('sns')


#sns_response = sns.create_topic(
#    Name='config-sns-topic1',
#    Attributes={
#        'string': 'sns'
#    },
#    Tags=[
#        {
#            'Key': 'sns',
#            'Value': 'sns'
#        },
#    ]
#)

#print (sns_response)

#sns_arn = sns_response["TopicArn"]

#print (sns_arn)

#===========================================================================================
#import boto3

#client = boto3.client('kms')

#kms_response = client.list_keys(
#)

#print(kms_response)

#key_id =  kms_response['Keys'][0]['KeyId']

#print(key_id)

#=======================================================

#kms_client = boto3.client('kms')

#policy = """{
#"Sid": "Enable CloudTrail log decrypt permissions",
#  "Effect": "Allow",
#  "Principal": {
#    "AWS": "arn:aws:iam::998488308670:user/root"
#  },
#  "Action": "kms:Decrypt",
#  "Resource": "*",
#  "Condition": {
#    "Null": {
#      "kms:EncryptionContext:aws:cloudtrail:arn": "false"
#    }
#  }
#}"""
    
# Convert the policy to a JSON string
#bucket_policy = json.dumps(policy)

# Creating client key
#desc = "Key for testing"
#response = kms_client.create_key(
#    Description = desc,
#    Policy = policy
#)

#====================================================================

kms_client = boto3.client('kms')
response = kms_client.create_key(Description="testing")

    # Return the key ID and ARN
#resp=response['KeyMetadata']['KeyId'], response['KeyMetadata']['Arn']
resp=response['KeyMetadata']['KeyId']
print (resp)
