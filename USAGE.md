# Usage

Before executing a playbook, you need to perform some configuration.

## Prerequisites & Assumptions

* Ansible 2.7+
* The infrastricture resources will be created on the Melbourne Univeristy Research cloud using the openstack sdk
* The playbook initiator has access to the nectar cloud and has downloaded the necessary files (API key and openrc.sh file)

## General Configuration

### Prepare Playbook and Scripts

1. Edit the [run.sh](ansible/run.sh) file. Update the file to point to the correct location of the openrc.sh file:
    * hosts : inventory file name
    * assignment2.yaml : the anisble playbook name

2. If you need to update the inventory file, only do so by adding more variables to [SWARM:vars] group. Do not change the file structure in any other way

3. Update the vars files under the [host_vars directory](ansible/host_vars) with the necessary vars

### Assignment 2 Configuration

The following configuration are specific to the [Assignment2](ansible/assignment2.yaml) playbook.

#### Volume Setup for Application State

Volume mounts are used to store the application data on a separate disk, usually mounted in `/opt`.

#### Volume Setup for Docker

As a best practice, Docker can also be optionally configured to use a block device for its storage. This block device can be referenced directly in role variables and should not be mounted beforehand.

#### Execution

To run the playbook, execute:

``` bash
./run.sh
```

from within the ansible directory
