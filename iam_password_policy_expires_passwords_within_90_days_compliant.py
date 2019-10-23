#!/usr/bin/env python

import boto3
import logging

iam = boto3.resource('iam')
account_password_policy = iam.AccountPasswordPolicy()
response = account_password_policy.update(
    MaxPasswordAge=90,
    )
