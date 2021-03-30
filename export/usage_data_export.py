#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:49:59 2018

@author: zoli
"""


from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client

import datetime

from export.usage_data_functions import query_usage_data
from export.usage_data_functions import export_usage_data
from dateutil.relativedelta import relativedelta

def usage_export(project_id, project_name, cred, version = "new"):
    
    if version == "new":
        auth_url = cred["auth_url_2.5"]
        username = cred["username_2.5"]
        password = cred["password_2.5"]
        master_project_id = cred["project_id_2.5"]
        cert_loc = cred["openstack_cert_location_2.5"]
    else:
        auth_url = cred["auth_url_2.0"]
        username = cred["username_2.0"]
        password = cred["password_2.0"]
        master_project_id = cred["project_id_2.0"]
        cert_loc = ""
    
    auth = v3.Password(auth_url=auth_url, username=username, password=password, project_id=master_project_id, user_domain_id='default')
    sess = session.Session(auth=auth, verify=cert_loc)
    nova = client.Client(2,session=sess)
    
    global_start_year = int(cred["usage_start_year"])
    global_start_month = int(cred["usage_start_month"])
    global_end_year = int(cred["usage_end_year"])
    global_end_month = int(cred["usage_end_month"])
    
    global_start = datetime.datetime(global_start_year,global_start_month,1)
    global_end = datetime.datetime(global_end_year,global_end_month,1)
    
    usage_data = query_usage_data(nova, project_id, global_start, global_end)
    
    location = cred["usage_export_dir"]+project_name+"/usage/"
    
    #get actual useage: daily usage / 24 hours
    
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    
    yesterday = today - relativedelta(days=+1)
    
    actual_usage_data = query_usage_data(nova, project_id, yesterday, today)
    
    if actual_usage_data != {}:
        usage_data["actual_memory_mb_usage"] = int(actual_usage_data["total_memory_mb_usage"]) / 24
        usage_data["actual_vcpus_usage"] = int(actual_usage_data["total_vcpus_usage"]) / 24
        usage_data["actual_local_gb_usage"] = int(actual_usage_data["total_local_gb_usage"]) / 24
    else:
        usage_data["actual_memory_mb_usage"] = 0
        usage_data["actual_vcpus_usage"] = 0
        usage_data["actual_local_gb_usage"] = 0
    
    print("Location of usage export: ", location)
    export_usage_data(usage_data,location, global_start, "glob")
    
    start = global_start
    #print("Days difference: ",(global_end - start).days)
    
    while (global_end - start).days > 25:
        next_month = start + relativedelta(months=+1)
        
        usage_data = query_usage_data(nova, project_id, start, next_month)
        
        if usage_data != {}:
            usage_data.pop("server_usages") #remove server usage from the monthly breakdown
            export_usage_data(usage_data,location, start, "month")
        
        start = next_month
        
        
    start = datetime.datetime(global_start_year,1,1)
    
    while (global_end - start).days > 25:
        next_year = start + relativedelta(years=+1)
        
        usage_data = query_usage_data(nova, project_id, start, next_year)
        
        if usage_data != {}:
            usage_data.pop("server_usages") #remove server usage from the monthly breakdown
            export_usage_data(usage_data,location, start, "year")
        
        start = next_year
