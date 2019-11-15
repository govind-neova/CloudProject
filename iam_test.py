#!/usr/bin/python
import boto3
import json

statusclient = boto3.client('iam')
statusresponse = statusclient.get_account_password_policy()
#status=(statusresponse['PasswordPolicy']['RequireUppercaseCharacters'])
status=(statusresponse)
#print (status)
print json.dumps({'Resource': True,'data': status['PasswordPolicy']})


#if status == True:
#    print("status is true")
#elif status == False:
#    print("status is false")
#
