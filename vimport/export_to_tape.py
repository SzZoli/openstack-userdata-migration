#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:41:14 2018

@author: zoli
"""

import subprocess
import io
import time
import sys
import os.path

def export_to_tape(volume):

    project_name = volume["project_name"]
    volume_name = volume["volume_migration_name"]

    #check whether the volume is already exported to tape, if it is dont export again
    if os.path.isfile("/mnt/tape/cloud2export/"+project_name+"/"+volume_name+".volume"):
        print("Volume is already exported to tape: ", volume_name, " Skipping backup.")
        return
        

    subprocess.call(["mkdir", "-p", "/mnt/tape/cloud2export/"+str(project_name)])
    command = "pv /mnt/data/export/"+project_name+"/"+volume_name+".volume > /mnt/tape/cloud2export/"+project_name+"/"+volume_name+".volume"

    print("Exporting volume to tape: ",volume_name)

    filename = '/tmp/test.log'
    with io.open(filename, 'w') as writer, io.open(filename, 'r', 1) as reader:
         process = subprocess.Popen(command, stdout=writer, shell=True)
         while process.poll() is None:
             sys.stdout.write(reader.read())
             time.sleep(30)
         process.wait()
    print("Backup to tape of volume "+volume_name+" done")
    
    return
