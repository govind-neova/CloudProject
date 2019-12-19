#!/usr/bin/python

import boto3
import json
import sys
import os.path
from os import path
sys.path.insert(0, '../')
from common import *

#Global variables
client = boto3.client('cloudtrail')
varFlag = ''
s3 = boto3.client('s3')
#var_bucket_name = ''
varResources = []

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

def func_update_and_validate_config(varDecision):
    for n in get_regions():
        configClient = boto3.client('config', region_name=n)
        response = configClient.describe_configuration_recorder_status()
        if response['ConfigurationRecordersStatus']:
            for i in response['ConfigurationRecordersStatus']:
                recorderName = i['name']
                print(recorderName)
                print (response['ConfigurationRecordersStatus'])
                if varDecision is True:
                    config_response = configClient.start_configuration_recorder(
                               ConfigurationRecorderName=i['name']
                            )
                    if config_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        log.info('Resourse "' +recorderName+ '" made compliant')
                elif varDecision is False:
                    config_response = configClient.stop_configuration_recorder(
                            ConfigurationRecorderName=i['name']
                            )
                    if config_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        log.info('Resourse "' +recorderName+ '" made non-compliant')
                elif varDecision == Delete:
                    config_response = configClient.stop_configuration_recorder(
                            ConfigurationRecorderName=i['name']
                            )
                    if config_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        log.info('Resourse "' +recorderName+ '" deleted')

func_update_and_validate_config(False)
