#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:00:37 2018

@author: zoli
"""

def request_project_name(project_list:dict):
    
    print("Which project would you like to migrate today?")
    print("Leave project name empty if you want to give project ID instead.")
    project_name = input("Project name: ")
    project_id = ""
    
    if project_name == "":
        project_id = input("Project ID: ")
        project_name = project_list[project_id]
        print("Project to migrate name: ", project_name) #for testing if project id is valid
    else: #to test if name exists in the list of projects
        for proj_id, proj_name in project_list.items(): 
            if proj_name == project_name:
                project_id = proj_id
        print("Project ID to migrate: ", project_id)
        
    return project_id, project_name