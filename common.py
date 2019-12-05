import os
import sys
import json
import logging
import datetime
import yaml
import boto3
import time

#Global variables
cloudTrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')
client = boto3.client('ec2')

#This function provides regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    data = [region['RegionName'] for region in region_response['Regions']]
    yield data

#This function fetches data from config.yaml file
def func_yaml_input():
   with open(r'config.yaml') as file:
       data = yaml.safe_load(file)
       return data

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

#Epoch function to get resource name
def funcResName(varService,varResource):
    
    configData = func_premenant_yaml_input_vars()
    varPrefix = configData['prefix']
    datefmt = int(time.time())    
    varName = varPrefix+ "-" +varService+ "-" +varResource+ "-" +str(datefmt)
    return varName

#Function to reset config.yaml file
def func_reset_config ():
    f = open("config.yaml", "w")
    line1 = '# This file is used to configure the behaviour for the scripts at runtime'
    line2 = '# Please update the values of the variables very carefully.'
    line3 = 'mode:'
    line4 = 'deleteExistingResources:'
    line5 = 'updateExistingResources:'
    
    f.write("%s\n%s\n\n\n%s\n%s\n%s\n"%(line1,line2,line3,line4,line5))
    f.close()

#Function to validate the input from users
def func_user_input_validation():
    data=func_yaml_input()
    if data['mode'] == 'compliant' :
        if data['updateExistingResources'] is True and data['deleteExistingResources'] is False :
            varUserInput = "compliantUpdate"
        elif data['updateExistingResources'] is False and data['deleteExistingResources'] is True :
            varUserInput = "compliantDelete"
        elif data['updateExistingResources'] is False and data['deleteExistingResources'] is False:
            varUserInput = "createcompliant"
        else:
            log.error("Please enter valid inputs in config file, exiting the script.")
            sys.exit()
    elif data['mode'] == 'non-compliant' :
        if data['updateExistingResources'] is True and data['deleteExistingResources'] is False :
            varUserInput = "nonCompliantUpdate"
        elif data['updateExistingResources'] is False and data['deleteExistingResources'] is True :
            varUserInput = "nonCompliantDelete"
        elif data['updateExistingResources'] is False and data['deleteExistingResources'] is False:
            varUserInput = "createnoncompliant"
        else:
            log.error("Please enter valid inputs in config.yaml file, exiting the script")
            sys.exit()
    else:
         log.info('Invalid argument, Please enter valid inputs in config.yaml file')
         varUserInput = "Invalid Argument"
         sys.exit()
    return varUserInput


#This function creates and writes data to Json file
def func_write_to_json(varScriptName):
    data=func_yaml_input()
    varMode = data['mode']
    varUpdate = data['updateExistingResources']
    varDelete = data['deleteExistingResources']
    data = {}
    data['resourceDetails'] = []

    data['resourceDetails'].append({
        'ScriptName': varScriptName,
        'Mode': varMode,
        'Update': varUpdate,
        'Delete': varDelete,
        'Resources': ''
    })

    with open(varScriptName +'.json', 'w') as outfile:
        json.dump(data, outfile)

##Function describing All Cloudtrails in all regions
def func_cloudTrails_resources_details ():
    for i in get_regions():
        for j in i:
            client = boto3.client('cloudtrail')
            cloudTrail = boto3.client('cloudtrail', region_name=j)
            cloudTrail_response = cloudTrail.describe_trails()
            for k in cloudTrail_response['trailList']:
                yield (k)

#The following function creates non-compliant cloud trail
bucket = funcResName("s3","bucket")
print (bucket)
cloudTrail_name = funcResName("cloudTrail","trail")
print(cloudTrail_name)

def func_create_non_comp_cloudTrail():
    try:
        # Create a bucket policy
        s3 = boto3.client('s3')
        response = s3.create_bucket(
            ACL='public-read-write',
            Bucket=bucket
            )


        # Create the bucket policy and convert to json
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck20150319",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::%s" % bucket
                },
                {
                    "Sid": "AWSCloudTrailWrite20150319",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::%s/*" % bucket ,
                    "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
                }
            ]
        }

        bucket_policy = json.dumps(bucket_policy)


        ## Set the new policy on the given bucket
        s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)

        response=cloudTrail.create_trail(
            Name=cloudTrail_name,
            S3BucketName=bucket,
            IncludeGlobalServiceEvents=True,
        #    IsMultiRegionTrail=True
        #    EnableLogFileValidation=True|False,
        #    CloudWatchLogsLogGroupArn='string',
        #    CloudWatchLogsRoleArn='string',
        #    KmsKeyId='string',
        #    IsOrganizationTrail=True|False
        )
        return response

    except Exception as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print ('hhahahahahahahaahah')
