#!/usr/bin/python

import boto3
import json

session = boto3.Session(region_name="us-east-1")

ec2 = session.resource('ec2')

instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['terminated']}])

for instance in instances:
    print(instance.id, instance.instance_type)
