#!/usr/bin/python

import boto3
import json

# Create a bucket policy
s3 = boto3.client('s3')
response = s3.create_bucket(
    ACL='private',
    Bucket='gov-gvmmgmkfvmf1234',
    )

bucket_name = 'gov-gvmmgmkfvmf1234'

s3.put_public_access_block(
    Bucket='gov-gvmmgmkfvmf1234',
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
)
