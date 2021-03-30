#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:24:02 2018

@author: zoli
"""

import csv

def import_proj_list(file_loc:str = "proj_list.csv"):
    #using a csv file was nessesery due to a keystone problem in the legacy cloud
    #this is not a big problem, because we can assume no new projects are created in the old cloud while running the migration
    
    input_file = csv.reader(open(file_loc))
    
    d = {}
    for k, v in input_file:
        d[k] = v
    return d
        
