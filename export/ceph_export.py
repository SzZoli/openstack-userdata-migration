#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 10:33:26 2018

@author: zoli
"""


import subprocess
import io
import time
import sys
import os.path

def ceph_export(volumes:list,cred):
    for volume in volumes:
        ceph_volume_export(volume,cred)
    print("All export succesfully completed!")
    return

def ceph_volume_export(volume:dict,cred):
    

    volume_id = volume["id"]
    volume_name = volume["name"]
    project_name = volume["project_name"]
    server_id = volume["server_id"]
    server_name = volume["server_name"]
    mountpoint = volume["mountpoint"]
    
    client = cred["ceph_client_2.0"]
    directory = str(cred["volume_export_dir"])
    
    volume_migration_name = volume_id+"-"+volume_name+"-"+server_name+"-"+mountpoint
    
    #check whether the volume is already exported from old cloud, if it is dont export again
    if os.path.isfile(directory+project_name+"/"+volume_migration_name+".volume"):
        print("Volume is already exported from old cloud: ", volume_migration_name, " Skipping export.")
        return
    
    print("-----------------")    
    print("Exporting volume:")
    print("Volume ID: ", volume_id)
    print("Volume name: ", volume_name)
    print("Server ID: ", server_id)
    print("Server name: ", server_name)
    print("Mountpoint: ", mountpoint)
    #print("Project name: ", project_name)
    
    file_path = directory+project_name+"/"+volume_migration_name+".volume"
    
    print("To: ", file_path)
               
    command = "rbd --name client.cinder export -p volumes volume-"+str(volume_id)+" "+file_path
    subprocess.call(["ssh", "root@"+str(client), "mkdir -p "+directory+str(project_name)])

    filename = '/tmp/test.log'
    with io.open(filename, 'w') as writer, io.open(filename, 'r', 1) as reader:
         process = subprocess.Popen(["ssh", "root@"+str(client), command], stdout=writer)
         while process.poll() is None:
             sys.stdout.write(reader.read())
             time.sleep(5)
         process.wait()
    print("Exporting volume "+volume_name+" done")
    return
