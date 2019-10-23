#!/usr/bin/env python

import boto3
import logging

client = boto3.client('iam')
response = client.get_account_password_policy()
output = response['PasswordPolicy']['RequireNumbers']
print (output)

if output==True:
   print("No Need to do anything")
else:
   print("You have to change the output")

#input=raw_input('Enter your responce (compliant/noncompliant) : ') 
#if input == "compliant":
#    info_logging_function() 
#    response = account_password_policy.update(  
#    RequireLowercaseCharacters=True
#    )
   
#elif input == "noncompliant":
#  response = account_password_policy.update(
#    RequireLowercaseCharacters=False,
#    )
#else: 
#   print("Kindly provide valid input")
