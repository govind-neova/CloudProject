#!/usr/bin/env python

import boto3
import yaml
import sys
import os

def func_reset_config ():
    f = open("config.yaml", "w")
    line1 = '# This file is used to configure the behaviour for the scripts at runtime'
    line2 = '# Please update the values of the variables very carefully.'
    line3 = 'mode:'
    line4 = 'deleteExistingResources:'
    line5 = 'updateExistingResources:'
    
    f.write("%s\n%s\n\n\n%s\n%s\n%s\n"%(line1,line2,line3,line4,line5))
    f.close()

func_reset_config ()
