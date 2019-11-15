#!/usr/bin/env python

import boto3

response = client.create_security_group(
    Description='CIS-SG',
    GroupName='CIS-SG',
    VpcId='string',
    DryRun=True
)
