
Purpose of this role that it to develop, demonstrate and test  internal roles such as [lcm](../lcm/), [lvm](../lvm/) and [backup](../backup/) that are created to support LCM procedures.
<!-- MarkdownTOC -->

- myapp Ansible role
- Vagrant up VMs
- MyApp2 VM
    - MyApp2 logical volume
    - Create MyApp2 data
    - Create MyApp2 backup
- MyApp VM
    - Create MyApp data
    - Restore MyApp
- Upgrade MyApp

<!-- /MarkdownTOC -->
## myapp Ansible role

The role __myapp__ creates an simple app with a home directory and database. The app consists of three scripts that can be run as user __myapp__ to add, view and delete "data". 

    [myapp@myapp ~]$ ls
    delete.sh  insert.sh  select.sh

This role is supported by internal roles:
- __lvm__ to create a logical volume.
- __backup__ to configure the backup.
- __lcm__ to support install, upgrade, update, rollback and rollforward LCM operations.

## Vagrant up VMs

Use `vagrant up` and `provision` to create the three VMs. 

    vagrant up postgresql myapp myapp2

## MyApp2 VM

The __myapp__ role creates the following in __myapp2__ VM:
- Emtpy database `myapp2_0_1_0` with table `myapp_table`.
- A "home" directory `/opt/myapp/myapp-0.1.0` with a single file `myapp.txt`. 
- A empty __data__ directory.

### MyApp2 logical volume

*If* there is a free disk `/dev/sdb` the __lvm__ role will create `/opt/myapp` as a mount of a LVM logical volume.

    [root@myapp ~]# df -h  | grep myapp
    /dev/mapper/data-myapp           976M  2.6M  907M   1% /opt/myapp

### Create MyApp2 data

Ssh into the machine and create some "data".

    vagrant ssh myapp2
    sudo su - myapp

__select.sh__ shows 0 "stories" - the database `myapp2_0_1_0` is empty. The __data-- folder is also still empty. 

    [myapp@myapp2 ~]$ ./select.sh
     story
    -------
    (0 rows)
    .
    /opt/myapp
    |-- myapp -> /opt/myapp/myapp-0.1.0
    `-- myapp-0.1.0
        |-- data
        |-- myapp.txt
        `-- VERSION

Create some data using __insert.sh__ and view it using __select.sh__. For example as below: three "story" records with three corresponding files in the root and in the __data__ folder.  

    [myapp@myapp2 ~]$ ./select.sh 
                                         story                                      
    --------------------------------------------------------------------------------
     My story MDBiYzYxMzg2ODc3M2Q5NjM5OWEzMzE3 on  myapp2 about myapp version 0.1.0
     My story MGU1MjgxMDliOTlkZDUyYWRiMzk2N2Yz on  myapp2 about myapp version 0.1.0
     My story NjgwYTUyNDFlNGM0NDNlYjY5NjM1YjUx on  myapp2 about myapp version 0.1.0
    (3 rows)
    .
    /opt/myapp
    |-- myapp -> /opt/myapp/myapp-0.1.0
    `-- myapp-0.1.0
        |-- data
        |   |-- MDBiYzYxMzg2ODc3M2Q5NjM5OWEzMzE3
        |   |-- MGU1MjgxMDliOTlkZDUyYWRiMzk2N2Yz
        |   `-- NjgwYTUyNDFlNGM0NDNlYjY5NjM1YjUx
        |-- MDBiYzYxMzg2ODc3M2Q5NjM5OWEzMzE3
        |-- MGU1MjgxMDliOTlkZDUyYWRiMzk2N2Yz
        |-- myapp.txt
        |-- NjgwYTUyNDFlNGM0NDNlYjY5NjM1YjUx
        `-- VERSION
        .
    4 directories, 8 files
    [myapp@myapp2 ~]$ 

### Create MyApp2 backup

As root run the backup manually using alias `tpelcm_myapp_daily`. This creates a tar `myapp_daily_0_1_0.tar` in NFS backup mount `/backup`.

    [root@myapp ~]# tpelcm_myapp_daily 
    [root@myapp ~]# tree /backup/
    /backup/
    |-- archives
    |   `-- myapp
    |       `-- myapp_daily_0_1_0
    |           `-- 2019.10.10.09.10.40
    |               `-- myapp_daily_0_1_0.tar
    |-- logs
    |   `-- myapp_myapp_daily_0_1_0.log
    `-- tmp
        `-- myapp
        .
    7 directories, 2 files
    [root@myapp ~]# 

## MyApp VM

The __MyApp__ VM is identical to __MyApp2__. The only difference is that it uses a different database schema.  

### Create MyApp data

As before with MyApp2 we create some data using __insert.sh__.

    [myapp@myapp ~]$ ./select.sh 
                                         story                                     
    -------------------------------------------------------------------------------
     My story YzY5MTBiMzQ2ZTEyYjRlOTE4Y2IzZjk4 on  myapp about myapp version 0.1.0
     My story OWFlYmFkMjE2YjcwYzkwZjczZmQ5M2Yw on  myapp about myapp version 0.1.0
    (2 rows)
    .
    /opt/myapp
    |-- myapp -> /opt/myapp/myapp-0.1.0
    `-- myapp-0.1.0
        |-- data
        |   |-- OWFlYmFkMjE2YjcwYzkwZjczZmQ5M2Yw
        |   `-- YzY5MTBiMzQ2ZTEyYjRlOTE4Y2IzZjk4
        |-- myapp.txt
        |-- OWFlYmFkMjE2YjcwYzkwZjczZmQ5M2Yw
        `-- YzY5MTBiMzQ2ZTEyYjRlOTE4Y2IzZjk4
        .
    3 directories, 5 files

### Restore MyApp

*Restore* is also part of the __backup__ role. To "restore" __MyApp__ using the __MyApp2__ backup we only need to run Ansible using 

    vagrant provision myapp

The reason for this is that the backup is configured as follows in [host_vars/myapp2.yml](../../../host_vars/myapp.yml)

    ---
    backup_restore: 
      myapp:
        path_pattern: '*'
        folder: data
        force: false

The `path_pattern` fact will be expanded by the __backup__ role to `/backup/archives/*/myapp_*/*/*.tar`. So this selects *the most recent backup* of the __myapp__ role, created on *any host*. The backup will be restored once untill a more recent backup becomes available. Attribute `force: true` can be used to run the restore each time.

It could also be configured as `2019.10.10.09.10.40` to select a specific backup file. Then it will be expanded `/backup/archives/*/myapp_*/2019.10.10.09.10.40/*.tar`. 

Or it can be configured as an expanded path directly for example `/backup/archives/myapp2/myapp_*/*/*.tar` to select only backup files created by `myapp2` host. 

After restore __myapp__ we see the database and the __data__ directory of __myapp2__. The home of __myapp__ however still has the same files for example `OWFlYmFkMjE2YjcwYzkwZjczZmQ5M2Yw`. This is because only the __data__ directory was configured to be restored using the `folder` attribute. 

    [myapp@myapp ~]$ ./select.sh 
                                         story                                      
    --------------------------------------------------------------------------------
     My story MDBiYzYxMzg2ODc3M2Q5NjM5OWEzMzE3 on  myapp2 about myapp version 0.1.0
     My story MGU1MjgxMDliOTlkZDUyYWRiMzk2N2Yz on  myapp2 about myapp version 0.1.0
     My story NjgwYTUyNDFlNGM0NDNlYjY5NjM1YjUx on  myapp2 about myapp version 0.1.0
    (3 rows)
    .
    /opt/myapp
    |-- myapp -> /opt/myapp/myapp-0.1.0
    |-- myapp-0.1.0
    |   |-- data
    |   |   |-- MDBiYzYxMzg2ODc3M2Q5NjM5OWEzMzE3
    |   |   |-- MGU1MjgxMDliOTlkZDUyYWRiMzk2N2Yz
    |   |   `-- NjgwYTUyNDFlNGM0NDNlYjY5NjM1YjUx
    |   |-- myapp.txt
    |   |-- OWFlYmFkMjE2YjcwYzkwZjczZmQ5M2Yw
    |   |-- VERSION
    |   `-- YzY5MTBiMzQ2ZTEyYjRlOTE4Y2IzZjk4
    `-- RESTORED
    .
    3 directories, 8 files

## Upgrade MyApp

