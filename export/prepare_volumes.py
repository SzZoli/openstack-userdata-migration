#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:06:17 2018

@author: zoli
"""

from export.filter_volumes import filter_volumes

def get_server_name(server_id:str,instances:list) -> str:
    
    for instance in instances:
        if instance.id == server_id:
            return instance.name
    return ""

def volumes_prepare(volumes:list,instances:list,projects:dict) -> list:
    """
    Convert volumes to dictionary and add extra parameters like server name and project name.
    """
    v2 = []
    
    for volume in volumes:
        
        volume_dict = volume.to_dict()
        
        volume_dict["project_name"] = projects[volume_dict["os-vol-tenant-attr:tenant_id"]]
        
        if volume_dict["name"] == "None" or volume_dict["name"] == None:
            volume_dict["name"] = ""

        if volume_dict["name"] != "": #replace space to _ so its usable in the volume name, if it has volume name
            volume_dict["name"] = str(volume_dict["name"]).replace(" ","_") 

        #check if volume is attached to an instance and act accordingly
        if volume_dict["attachments"] != [] :
            volume_dict["server_id"] = volume_dict["attachments"][0]["server_id"]
            volume_dict["server_name"] = get_server_name(volume_dict["attachments"][0]["server_id"],instances)
            volume_dict["mountpoint"] = volume_dict["attachments"][0]["device"].split('/')[-1]
            if volume_dict["mountpoint"] == "vda":
                volume_dict["mountpoint"] = "root"
        else:
            volume_dict["server_id"] = "not attached"
            volume_dict["server_name"] = ""
            volume_dict["mountpoint"] = ""
        
        volume_dict["volume_migration_name"] = volume_dict["id"]+"-"+volume_dict["name"]+"-"+volume_dict["server_name"]+"-"+volume_dict["mountpoint"]
        v2.append(volume_dict)
        
    v2 = filter_volumes(v2)
    return v2
