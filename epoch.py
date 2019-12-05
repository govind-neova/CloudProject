#!/usr/bin/env python

import boto3
import yaml
import sys
import os
import datetime
import logging
import time

#This function fetches data from perm_config.yaml file
def func_premenant_yaml_input_vars():
   with open(r'perm_config.yaml') as file:
       configData = yaml.safe_load(file)
       return configData

#Function to print the logs
def log():
    configData = func_premenant_yaml_input_vars()
    logger = logging.getLogger('aws-cis')
    level = logging.getLevelName(configData['logLevel'])
    logger.setLevel(level)
    console_handler=logging.StreamHandler()
    console_format=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%a %b %d %Y %I:%M:%S %p %Z')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    return logger
log = log()
log.info("hiiiiiii")

def funcResName(varService,varResource):
    
    permConfigData = func_premenant_yaml_input_vars()
    varPrefix = permConfigData['prefix']
    ts = int(time.time())
    varName = varPrefix+ "_" +varService+ "_" +varResource+ "_" +str(ts)
    return varName


#resnmae= "gaovind"
#serv= "saraf"

var=funcResName("Govind","Saraf")
print("this is "+var) 
