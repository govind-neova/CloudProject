#!/usr/bin/env python

import boto3
import yaml
from common import *
import sys
import os.path
from os import path

s3 = boto3.resource('s3')
bucket_acl = s3.BucketAcl('ato-s3-bucket-1576141785')
print (bucket_acl.grants('Grantee'))
