#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 13:40:11 2018

@author: zoli
"""


import sys
import json
import requests

sys.path.append("../credentials/")
import credentials.token_request
from vimport.set_volume_to_bootable import set_volume_to_bootable

def get_project_id(projectname_in, project_list):
    for project_id, project_name in project_list.items():
        if project_name == projectname_in:
            return project_id
    raise ValueError("project_not_found")
    return "project_not_found"

def create_cinder_volume(old_volume,project_list:dict, cred, usern, passwd):
    token = credentials.token_request.get_openstack_token("new", cred, old_volume["project_name"], usern, passwd)
    
    project_id_destination = get_project_id(old_volume["project_name"], project_list)
    
    cinder_endpoint="https://openstack.cloud.local:13776/v3/"+project_id_destination+"/volumes"
    #print("Value type: ",type(cinder_endpoint))
    
    #https://developer.openstack.org/api-ref/block-storage/v3/#create-a-volume

    if old_volume["description"] == None :
        old_volume["description"] = ""
    
    #set volume name in the new cloud
    new_name = ""
    if old_volume["server_id"] != "not attached":
        new_name = old_volume["server_name"]+"."+ old_volume["mountpoint"]
    else:
        if old_volume["name"] != "":
            new_name = old_volume["name"]
        else:
            new_name = "old_id-"+old_volume["id"]
    
    
    json_data={
    "volume": {
        "size": old_volume["size"],
        "description": "migrated_from_2.0"+str(old_volume["description"]),
        "name": new_name,
        }
    }
    
    volume_post_response=requests.post(cinder_endpoint,json=json_data,verify=cred["openstack_cert_location_2.5"],headers={"X-Auth-Token":token})

    """ 
    Used for debugging:   
    print("Endpoint: ", cinder_endpoint)
    print("Data: ", json_data)
    print("Token: ", token)
    
    
    print("Response type: ",type(volume_post_response))
    print("Response code: ",volume_post_response.status_code)
    print("Response reason: ",volume_post_response.reason)
    print("Respons text: ", volume_post_response.text)
    """
    
    volume_json = json.loads(volume_post_response.text)

    #set bootable status if it was in the old
    if old_volume["bootable"] == "true":
        print("Setting volume to bootable status")
        set_volume_to_bootable(volume_json, token, project_id_destination, cred)
    else:
        print("Volume was not bootable...")
    
    credentials.token_request.revoke_openstack_token(token, "new", cred)
    
    return volume_json, project_id_destination
    
    

    
