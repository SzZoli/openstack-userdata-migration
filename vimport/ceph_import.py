#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 13:37:00 2018

@author: zoli
"""

import subprocess
import io
import time
import sys

import multiprocessing as mp

from vimport.create_cinder_volume import create_cinder_volume
#from vimport.get_project_list_fromapi import get_projects_newcloud
from vimport.export_to_tape import export_to_tape

def ceph_import(volumes:list, project_list, cred, usern, passwd):
    
    for volume in volumes:
        
        if (cred["backup_to_tape"] == "True" and cred["import_to_newcloud"] == "True"):
            #import and backup at the same time:
            p1 = mp.Process(target=ceph_volume_import, args = (volume, project_list, cred, usern, passwd))
            p2 = mp.Process(target=export_to_tape, args = (volume, ))
        
            p1.start()
            p2.start()
        
            p1.join()
            p2.join()
        else:
            if cred["import_to_newcloud"] == "True":
                ceph_volume_import(volume, project_list, cred, usern, passwd)
            if cred["backup_to_tape"] == "True":
                export_to_tape(volume)
                


def ceph_volume_import(old_volume, project_list:dict, cred, usern, passwd):
        
    new_volume, project_id = create_cinder_volume(old_volume, project_list, cred, usern, passwd)
    
    client = cred["ceph_client_new"]
    new_volume_id = new_volume["volume"]["id"]
    new_volume_name = new_volume["volume"]["name"]
    project_name = project_list[project_id]
    
    directory = str(cred["volume_export_dir"])
    
    fileloc = directory+project_name+"/"+old_volume["volume_migration_name"]+".volume"
    
    print("------------")
    print("Created new volume in new cloud:")
    print("New volume ID: ",new_volume_id)
    print("New volume project_id: ", project_id)
    print("New volume name: ",new_volume_name)
    
    command = "rbd -p cinder-volumes import "+fileloc+" volume-"+str(new_volume_id)
    
    #delete the dummy volume
    subprocess.call(["ssh", "root@"+str(client), "rbd -p cinder-volumes rm volume-"+str(new_volume_id)])
    
    #import the volume from the old cloud
    filename = '/tmp/test.log'
    with io.open(filename, 'w') as writer, io.open(filename, 'r', 1) as reader:
         process = subprocess.Popen(["ssh", "root@"+str(client), command], stdout=writer)
         while process.poll() is None:
             sys.stdout.write(reader.read())
             time.sleep(10)
         process.wait()
    print("Importing volume "+new_volume_name+" done")
    return