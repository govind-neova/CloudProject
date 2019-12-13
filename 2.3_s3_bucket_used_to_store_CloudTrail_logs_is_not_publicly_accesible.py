#!/usr/bin/python

import boto3
import json
from common import *
import sys
import array
import re
from re import search


#Declairing user input variable
varUserInput = func_user_input_validation()

#Declairing scriptname for json file
varScriptName = sys.argv[0]

#Global variables
client = boto3.client('cloudtrail')
varFlag = ''

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

def get_cloudtrails():
    trails = dict()
    for n in get_regions():
        client = boto3.client('cloudtrail', region_name=n)
        response = client.describe_trails()
        temp = []
        for m in response['trailList']:
            if m['HomeRegion'] == n:
                temp.append(m)
        if len(temp) > 0:
            trails[n] = temp
    return trails


trails = dict()
for n in get_regions():
    client = boto3.client('cloudtrail', region_name=n)
    response = client.describe_trails()
    S3_CLIENT = boto3.client('s3') 
    temp = []
    for m in response['trailList']:
        if m['HomeRegion'] == n:
            #print (m['S3BucketName']+ ' :-----: ' +m['HomeRegion'])
            s3_response = S3_CLIENT.get_bucket_acl(Bucket=m['S3BucketName'])
            #print (s3_response['Grants'])
            for p in s3_response['Grants']:
                #print (p)
                #print (m['S3BucketName']+ ' :-----: ' +m['HomeRegion'])
                #print (p['Grantee'])
                #for i in p['Grantee']:
                #    if str(i) != str('URI'):
                #        #print('present')
                #        #print (p['Grantee']['URI'])
                #        #varPub1 = 'global/AllUsers'
                #        #varPub2 = 'global/AuthenticatedUsers'
                #        #if str(varPub1) not in (p['Grantee']['URI']) and str(varPub2) not in (p['Grantee']['URI']):
                #        print (m['S3BucketName']+ ' :-----: ' +m['HomeRegion'])
                #print(str(p['Grantee']))
                if  re.search(r'(global/AllUsers|global/AuthenticatedUsers)', str(p['Grantee'])):
                    log.info('public bucket')
                #    print (m['S3BucketName']+ ' :-----: ' +m['HomeRegion'])
                #    print (m['S3BucketName'])
                    temp.append(m)
                    if len(temp) > 0:
                        trails[n] = temp
#print (trails)

#for n in get_regions():
#    client = boto3.client('cloudtrail', region_name=n)
#    response = client.describe_trails()
#    S3_CLIENT = boto3.client('s3')
#    temp = []
#    for m in response['trailList']:
#        if m['HomeRegion'] == n:
#            #print (m['TrailARN'])
#            for i in trails:
#                for j in trails[i]:
#                    if (m['TrailARN']) == (j['TrailARN']):
#                        continue
#                    else:
#                        print (m['TrailARN'])

for n in get_regions():
    client = boto3.client('cloudtrail', region_name=n)
    response = client.describe_trails()
    S3_CLIENT = boto3.client('s3')
    temp = []
    for m in response['trailList']:
        if m['HomeRegion'] == n:
            #print (m['S3BucketName']+ ' :-----: ' +m['HomeRegion'])
            s3_response = S3_CLIENT.get_bucket_acl(Bucket=m['S3BucketName'])
            if not re.search(r'(global/AllUsers|global/AuthenticatedUsers)', str(s3_response)):
                print(m['S3BucketName'])
                print (s3_response)

#for i in trails:
#    for j in trails[i]:
#        s3_response = S3_CLIENT.get_bucket_acl(Bucket=m['S3BucketName'])
#        #print(s3_response)
#        if re.search(r'(global/AllUsers|global/AuthenticatedUsers)', str(s3_response)):
#            print (s3_response)
        #for p in s3_response['Grants']:
        #    print(p)

                #print("Grantee is " + str(p['Grantee']))
            #print (s3_response)

#cloud_trails = get_cloudtrails()
#for i in cloud_trails:
#    for j in  cloud_trails[i]:
#        print(j['S3BucketName'])
