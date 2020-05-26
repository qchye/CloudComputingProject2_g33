# Usage

Before executing a playbook, you need to perform some configuration.

## Prerequisites & Assumptions

* Ansible 2.7+
* The infrastructure resources will be created on the Melbourne Univeristy Research cloud using the openstack sdk for ansible
* The playbook initiator has access to the nectar cloud and has downloaded the necessary files (API key and openrc.sh file)

## General Configuration

### Prepare Playbook and Scripts

1. Edit the [run.sh](ansible/run.sh) file. Update the file to point to the correct location of the openrc.sh file. Additionally update (if required):
    * hosts : inventory file name
    * assignment2.yaml : the anisble playbook name

2. If you need to update the inventory file, only do so by adding more variables to [SWARM:vars] group. Do not change the file structure in any other way. Also ensure the ssh_key location is pointing to the correct location

3. Update the vars files under the [host_vars directory](ansible/host_vars) with the necessary vars

### Assignment 2 Configuration

This repository has configuration which is specific to the [Assignment2](ansible/assignment2.yaml) playbook.

#### Execution

To run the playbook, execute:

``` bash
./run.sh
```

from within the ansible directory
