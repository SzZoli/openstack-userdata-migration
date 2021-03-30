#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 10:22:19 2018

@author: zoli
"""

import json

def load_credentials(file:str) -> dict :

    with open(file, 'r') as fp:
        data = json.load(fp)
    return data

def save_credentials(data:dict,file:str):
    with open(file, 'w') as fp:
        json.dump(data, fp)
        