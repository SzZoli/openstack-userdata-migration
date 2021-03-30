#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:30:49 2018

@author: zoli
"""


from credentials.handle_credentials import load_credentials
from credentials.get_token_user import get_token_user
from credentials.request_project_name import request_project_name

from export.get_volume_list import get_volume_list
from export.get_instance_list import get_instance_list
from export.import_proj_list import import_proj_list
from export.ceph_export import ceph_export
from export.prepare_volumes import volumes_prepare
from export.usage_data_export import usage_export

from vimport.ceph_import import ceph_import
from vimport.get_project_list_fromapi import get_projects_newcloud

import credentials.token_request #for testing user token
#dir
    

if __name__== "__main__":
    
    print("")
    #Phase 1 is about gathering data from the user and testing if all imput is correct
    print("==== Phase 1 : Gathering Data ====")
    print("")
    
    credentials_file = "./credentials/credentials.json"
    cred = load_credentials(credentials_file)
    
    
    proj_list_old = import_proj_list("data/proj_list.csv")
    proj_list_new = get_projects_newcloud(cred)

        
    projectid, projectname = request_project_name(proj_list_old)
    
    username, passw = get_token_user()
    
    print("Testing user credentials...")
    testtoken = credentials.token_request.get_openstack_token("new", cred, projectname, username, passw)
    credentials.token_request.revoke_openstack_token(testtoken, "new", cred)
    print("Credentials for the new cloud looks ok... :)")
    print("")
    
    print("")
    print("Gathering information from old cloud...")
    instances = get_instance_list(projectid, cred, "old")
    volumes = get_volume_list(projectid, cred, "old")

    volumes = volumes_prepare(volumes,instances,proj_list_old)
    print("")
    print("")

    #Phase 2 starts here: exporting volumes from the old cloud
    print("==== Phase 2 : Export ====")
    print("")
    ceph_export(volumes, cred)
    print("")
    print("")
    
    print("")
    print("==== Phase 3 : Import & Backup ====")
    print("")
    ceph_import(volumes, proj_list_new, cred, username, passw)
    print("")
    
    print("")
    print("==== Phase 4 : Save Usage Statistics ====")
    print("")
    
    usage_export(projectid, projectname, cred, "old")

    