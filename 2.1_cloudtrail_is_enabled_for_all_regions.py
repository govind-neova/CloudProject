#!/usr/bin/python

import boto3
import json


#client = boto3.client('ec2')
#regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
#print (regions)
#for i in regions:
#    region_name = i
#    print (region_name)

with open('./variable.json') as f:
  data = json.load(f)
  print (data['region'])
  for i in data['region']:
      print (i)
      cloudTrail = boto3.client('cloudtrail', region_name=i)
      cloudTrail_response = cloudTrail.describe_trails()
#      print (cloudTrail_response['trailList'])
      for i in cloudTrail_response['trailList']:
          print(i['TrailARN'])
  
#region = region_client.describe_regions()
#for i in region:
#    print (i)


#cloudTrail   = boto3.client('cloudtrail')
#cloudTrail_response = cloudTrail.describe_trails()
#print (cloudTrail_response)

# Create a bucket policy
#s3 = boto3.client('s3')
#response = s3.create_bucket(
#    ACL='public-read-write',
#    Bucket='gov-gvmmgmkfvmfg',
#    )
#
#bucket_name = 'gov-gvmmgmkfvmfg'
#
## Create the bucket policy
#bucket_policy = {
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Sid": "AWSCloudTrailAclCheck20150319",
#            "Effect": "Allow",
#            "Principal": {"Service": "cloudtrail.amazonaws.com"},
#            "Action": "s3:GetBucketAcl",
#            "Resource": "arn:aws:s3:::gov-gvmmgmkfvmfg"
#        },
#        {
#            "Sid": "AWSCloudTrailWrite20150319",
#            "Effect": "Allow",
#            "Principal": {"Service": "cloudtrail.amazonaws.com"},
#            "Action": "s3:PutObject",
#            "Resource": "arn:aws:s3:::gov-gvmmgmkfvmfg/*",
#            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
#        }
#    ]
#}
#
## Convert the policy to a JSON string
#bucket_policy = json.dumps(bucket_policy)
#
## Set the new policy on the given bucket
#s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
#
#cTrail   = boto3.client('cloudtrail')
#response2 = cTrail.describe_trails()
#print (response2)
#
#cTrail.create_trail(
#    Name='govs1',
#    S3BucketName=bucket_name,
#    IncludeGlobalServiceEvents=True,
#    IsMultiRegionTrail=True,
##    EnableLogFileValidation=True|False,
##    CloudWatchLogsLogGroupArn='string',
##    CloudWatchLogsRoleArn='string',
##    KmsKeyId='string',
##    IsOrganizationTrail=True|False
#)
