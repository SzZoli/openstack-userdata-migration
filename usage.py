#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 07:57:40 2018

@author: zoli
"""

from credentials.handle_credentials import load_credentials
from export.import_proj_list import import_proj_list
from credentials.request_project_name import request_project_name
from export.usage_data_export import usage_export

if __name__== "__main__":
    
    credentials_file = "./credentials/credentials.json"
    cred = load_credentials(credentials_file)

    proj_list_old = import_proj_list("data/proj_list.csv")
    projectid, projectname = request_project_name(proj_list_old)
    
    usage_export(projectid, projectname, cred, "old")

