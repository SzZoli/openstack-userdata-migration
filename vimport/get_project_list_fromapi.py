#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:37:09 2018

@author: zoli
"""

import sys
import json
import requests

sys.path.append("../credentials/")
import credentials.token_request as token_request

def get_projects_newcloud(cred) -> dict : 
    
    token = token_request.get_openstack_token(version="new", cred=cred)
    
    project_endpoint=cred["auth_url_2.5"]+"/projects"
    list_projects=requests.get(project_endpoint,verify=cred["openstack_cert_location_2.5"],headers={"X-Auth-Token":token})
    
    projects_json = json.loads(list_projects.text)
  
    project_list_dict = {}
    
    for project in projects_json["projects"]:
        project_list_dict[project["id"]] = project["name"]
        
    token_request.revoke_openstack_token(token, version="new", cred=cred)
    
    return project_list_dict

def get_projects_oldcloud(cred) -> dict : 
    
    #cant request project information (due to bug?):
    #{'error': {'code': 403, 'message': 'You are not authorized to perform the requested action:
    #identity:list_projects (Disable debug mode to suppress these details.)', 'title': 'Forbidden'}}
    #Using pre-generated csv instead :(
    
    token = token_request.get_openstack_token(version="old", cred=cred)
    
    project_endpoint=cred["auth_url_2.0"]+"/projects"
    list_projects=requests.get(project_endpoint,verify="",headers={"X-Auth-Token":token})
    
    projects_json = json.loads(list_projects.text)
    
    project_list_dict = {}
    
    for project in projects_json["projects"]:
        project_list_dict[project["id"]] = project["name"]
        
    token_request.revoke_openstack_token(token, version="old", cred=cred)
    
    return project_list_dict

        
if __name__== "__main__":

    projects = get_projects_newcloud()
    
    print(projects)
