#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:36:07 2018

@author: zoli
"""

import sys

def query_yes_no(question):
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    
    prompt = " [Y/n]"
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def filter_volumes(volumes:list):
    v2 = volumes.copy()
    
    for volume in v2:
        print("---------------")
        print("Volume ID: ", volume["id"])
        print("Volume name: ", volume["name"])
        print("Server name: ", volume["server_name"])
        print("Mountpoint: ", volume["mountpoint"])
        if not query_yes_no("Do you want to migrate volume?"):
            volumes.remove(volume)
    return volumes
    
    