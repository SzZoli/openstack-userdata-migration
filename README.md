# OpenStack User Data Migration

This program was created for the purpose of migrating user data and usage statistics from our old cloud to the new cloud platform at Wigner Datacenter (WDC).
It is not made for general use, but with small changes it can be adopted to other enviroments.

![Alt text](structure.jpeg?raw=true "Structure")

## Getting Started

The main part of the program is about migrating volumes that instances (virtual machines in OpenStack) use as data storage. One run can migrate data from one project, so you need to run it for each OpenStack project you want to migrate.

The program is divided into five phases:
* Phase 1: Gathering Data: at the start, the program gathers data from the old cloud deployment, and asks the user which project is the target , and in that project which volumes are marked to migrate.
* Phase 2: Export: Using the ceph storage backend we export the volumes that were selected from migration.
* Phase 3: Import and Backup: Imports the previously exported volume into OpenStack and saves a backup on tape. These two processes (import and tape backup) run in paralell, to reduce run time.
* Phase 4: Since the old cloud is about to be demolished, the backup of the usage statistics was also needed. This phase solves that problem, doing a global (and detailed) usage query, saves it in json, then a monthly breakdown, from the project start to finish.
* Phase 5: Cleanup

### Prerequisites

Assumptions about the enviroment:
* There is a central machine (Migration Orchestrator), with enough storage to store one projects user data.
* This machine will run the program, it can reach both clouds APIs, and can access ceph through cli commands.
* The OpenStack project is already created in the new cloud, and the credentials you supply at the start has an OpenStack role ( usually member )in that project. (Needed for scoped token creation.)
* Make sure you have enough volume quota allocated in the new cloud, otherwise the import might fail.
* Optional: tape backup, to store a copy of the exported volumes on tape backup

The credentials.json contains some of the necessary parameters that describe the cloud enviroments like:
* API URLs for both cloud deployments, and credentials for admin token generation.
* Directory paths to use as working directory and export directory.
* Start and end times for usage query.


This program uses the Python3 API libraries of OpenStack:

To install these:

```
pip3 install python-keystoneclient
pip3 install python-cinderclient
pip3 install python-novaclient
```

Also dateutil for easy timestep management in Phase 4.

```
pip3 install dateutil
```

## Author

* **Zoltan Szeleczky** -  [GitHub link](https://github.com/SzZoli) (2018)


## Acknowledgments

* Sébastien Han for the idea (https://www.sebastien-han.fr/blog/2014/12/09/openstack-import-existing-ceph-volumes-in-cinder/)
* The WDC IT team :)
* Hat tip to anyone who's code was used
* The OpenStack team
* The Ceph team
* The open source community in general
