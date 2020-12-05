# Ansible Role: LVM

An Ansible Role that helps with managment of data disks / volumes using LVM.

## Role Variables

The way this works is self explanatory. Configure a name of the volume group e.g. 

    lvm_vg: 'data'

A list of devices to use for this group

    lvm_vg_devices: ['/dev/sdb', '/dev/sd']

Add the Ansible role that uses the LVM role to `lvm_roles_supported`. And then configure how the volume should be created

    lvm_roles:
      bitbucket:
        size: '10g' 
        path: '{{ bitbucket_home if bitbucket_home is defined else "/opt/bitbucket" }}'
