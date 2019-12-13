import os
import sys
import json
import logging
import datetime
import yaml
import boto3
import time


# Global Variable Declaration
if len(sys.argv) < 3:
    varScriptName = sys.argv[0]
    print("Atleast 2 arguments are required.")
    print("usage: ")
    print("\t"+varScriptName+" <compliant|non-compliant> <create|update|delete>")
    sys.exit()
else:
    varMode=sys.argv[1]
    varAction=sys.argv[2]

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


#This function fetches data from perm_config.yaml file
def func_permanent_yaml_input_vars():
   with open(r'../perm_config.yaml') as file:
       configData = yaml.safe_load(file)
       return configData

#Function to print the logs
def log():
    configData = func_permanent_yaml_input_vars()
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
    configData = func_permanent_yaml_input_vars()
    varPrefix = configData['prefix']
    datefmt = int(time.time())
    varName = varPrefix+ "-" +varService+ "-" +varResource+ "-" +str(datefmt)
    return varName

#Function to validate the input from users
def func_user_input_validation():
    if varMode == "compliant" :
        if varAction =="update":
            varUserInput = "compliantUpdate"
        elif varAction == "delete":
            varUserInput = "compliantDelete"
        elif varAction == "create":
            varUserInput = "createcompliant"
        else:
            log.error("Invalid argument, Please provide valid inputs, exiting the script")
            func_Usage()
            sys.exit()
    elif varMode == "non-compliant" :
        if varAction =="update":
            varUserInput = "nonCompliantUpdate"
        elif varAction == "delete":
            varUserInput = "nonCompliantDelete"
        elif varAction == "create":
            varUserInput = "createnoncompliant"
        else:
            log.error("Invalid argument, Please provide valid inputs, exiting the script")
            func_Usage()
            sys.exit()
    else:
         log.info("Invalid argument, Please provide valid inputs, exiting the script")
         func_Usage()
         sys.exit()
    return varUserInput


#This function creates and writes data to Json file
def func_write_to_json(varResources):
    varScriptName=sys.argv[0]
    data = {}
    data['resourceDetails'] = []
    varScriptName = varScriptName[2:]  
    data['resourceDetails'].append({
        'ScriptName': varScriptName,
        'Mode': varMode,
        'Action': varAction,
        'Resources': varResources
    })
    varScriptName = varScriptName[:-3] 
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
            ACL='private',
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


def func_Usage():
    varScriptName=sys.argv[0]
    print("usage: ")
    print("\t"+varScriptName+" <compliant|non-compliant> <create|update|delete>")
