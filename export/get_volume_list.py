#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:34:06 2018

@author: zoli
"""

from cinderclient import client
from keystoneauth1.identity import v3
from keystoneauth1 import session


def get_volume_list(project_to_migrate, cred, version = "new"):
    
    if version == "new":
        auth_url = cred["auth_url_2.5"]
        username = cred["username_2.5"]
        password = cred["password_2.5"]
        project_id = cred["project_id_2.5"]
        cert_loc = cred["openstack_cert_location_2.5"]
    else:
        auth_url = cred["auth_url_2.0"]
        username = cred["username_2.0"]
        password = cred["password_2.0"]
        project_id = cred["project_id_2.0"]
        cert_loc = ""
    
    
    auth = v3.Password(auth_url=auth_url, username=username, password=password, project_id=project_id, user_domain_id='default')
    sess = session.Session(auth=auth, verify=cert_loc)
    
    cinder = client.Client(2,session=sess)
    
    volumes = cinder.volumes.list(search_opts={'all_tenants': 1},detailed = True)
    
    
    volumes_to_migrate = []
    for volume in volumes:
        if project_to_migrate == volume.to_dict()['os-vol-tenant-attr:tenant_id']:
            volumes_to_migrate.append(volume)
    
  
    return volumes_to_migrate