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
    datefmt = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    varName = varPrefix+ "-" +varService+ "-" +varResource+ "-" +datefmt
    return varName

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



