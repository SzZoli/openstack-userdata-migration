#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:16:44 2018

@author: zoli
"""

import getpass

def get_token_user():
        
    print("Please give your username and password for the new cloud")
    print("(you need to have a role in the project you migrate to in the new cloud)")
    user = input("Username: ")
    password = getpass.getpass(prompt="Password: ")
    
    return user,password