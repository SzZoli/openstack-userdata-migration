#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:00:57 2018

@author: zoli
"""

import requests

def get_openstack_token(version:str, cred, scope = "admin", usern = "", passw = ""):

    
    if version == "new":
        username=cred["username_2.5"]
        password=cred["password_2.5"]
        domain='default'
        projectname = username=cred["username_2.5"]
        token_endpoint=cred["auth_url_2.5"]+"/auth/tokens"
        verif = cred["openstack_cert_location_2.5"]
    else:
        username=cred["username_2.0"]
        password=cred["password_2.0"]
        domain='default'
        projectname = username=cred["username_2.0"]
        token_endpoint=cred["auth_url_2.0"]+"/auth/tokens"
        verif = "" #no cert in the old cloud deployment
        
    if scope != "admin":
        scope_domain = cred["new_openstack_user_domain"]
        projectname = scope
    else:
        scope_domain = "default"
        
    if usern != "":  #get a specific scoped user token, for the purpose of cinder volume creation
        domain = cred["new_openstack_user_domain"]
        username = usern
        password = passw
        
    json_token_data={
        "auth":{
            "identity":{
                "methods":["password"],
                "password":{
                    "user":{
                        "domain":{"name":domain},
                        "name":username,
                        "password":password
                    }
                }
            },
            "scope":{
                "project":{
                    "domain":{"name":scope_domain},
                    "name": projectname
                }
            }
        }
    }

    get_token=requests.post(token_endpoint,json=json_token_data,verify=verif)
    return get_token.headers["X-Subject-Token"]

def revoke_openstack_token(token,version:str, cred):
    
  
    if version == "new":
        token_endpoint=cred["auth_url_2.5"]+"/auth/tokens"
        verif=cred["openstack_cert_location_2.5"]
    else:
        token_endpoint=cred["auth_url_2.0"]+"/auth/tokens"
        verif=""
    
    requests.delete(token_endpoint,verify=verif,headers={"X-Auth-Token":token,"X-Subject-Token":token})
    



