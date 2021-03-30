#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:27:59 2018

@author: zoli
"""

import json
import subprocess
import datetime

def query_usage_data(nova_session, project_id, start, end) -> dict:
    
    return nova_session.usage.get(project_id,start,end).to_dict()


def export_usage_data(usage_data, location, start:datetime, interval:str = "glob"):
    
    subprocess.call(["mkdir", "-p", location])
    
    if interval == "month":
        file = location+str(start.year)+"-"+str(start.month)+".json"
    elif interval == "year":
        file = location+str(start.year)+"-all.json"
    else:
        file = location+"global.json"
        
    with open(file, 'w') as file:
        file.write(json.dumps(usage_data,indent=4, separators=(',', ': ')))
    
    return