import os
import sys
import json
import logging
import datetime
import yaml


#This function fetches data from config.yaml file
def func_yaml_input():
   with open(r'config.yaml') as file:
       data = yaml.safe_load(file)
       return data

#Function to print the logs
def log():
    logger = logging.getLogger('aws-cis')
    logger.setLevel(logging.INFO)
    console_handler=logging.StreamHandler()
    console_format=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%a %b %d %Y %I:%M:%S %p %Z')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    return logger
log = log()


#Function to validate the input from users
def func_user_input_validation():
    data=func_yaml_input()
    if data['mode'] == 'compliant' :
        if data['updateExistingResources'] is True and data['deleteExistingResources'] is False :
            varUserInput = "compliantUpdate"
        elif data['updateExistingResources'] is False and data['deleteExistingResources'] is True :
            varUserInput = "compliantDelete"
        else:
            log.error("Please enter valid inputs in config file, exiting the script.")
            sys.exit()
    elif data['mode'] == 'non-compliant' :
         if data['updateExistingResources'] is True and data['deleteExistingResources'] is False :
             varUserInput = "nonCompliantUpdate"
         elif data['updateExistingResources'] is False and data['deleteExistingResources'] is True :
             varUserInput = "nonCompliantDelete"
         else:
             log.error("Please enter valid inputs in config file, exiting the script")
             sys.exit()
    else:
         log.info('Invalid argument, Please enter valid inputs in config file')
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



