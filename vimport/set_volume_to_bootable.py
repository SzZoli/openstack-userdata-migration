#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:54:06 2018

@author: zoli
"""

import requests

def set_volume_to_bootable(volume_json, token, project_id, cred):

    volume_id = volume_json["volume"]["id"]
    cinder_endpoint="https://openstack.cloud.local:13776/v3/"+project_id+"/volumes/"+volume_id+"/action"
        
    json_data={
        "os-set_bootable": {
            "bootable": "True"
        }
    }
    
    volume_post_response = requests.post(cinder_endpoint,json=json_data,verify=cred["openstack_cert_location_2.5"],headers={"X-Auth-Token":token})
    
    return volume_post_response.status_code