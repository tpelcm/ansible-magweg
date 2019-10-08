# Backup

An Ansible Role that configures the backup utility for supported roles for example __sonarqube__. This role can also be used to restore a backup.

Database and file system are archived together in a file for example similar to 

    /backup/archives/sonarqube/sonarqube_daily/2019.10.03.05.21.29/sonarqube_daily.tar`. 

The path is created as follows 

    {{ backup_archives }}/{{ inventory_hostname }}/{{ role }}_{{ schedule }}/{{ date-time }}/{{ role }}_{{ schedule }}.tar`. 

## Restore

To restore a backup for example for the __sonarqube__ role using the backup file 

    backup_restore:
       sonarqube: '2019.10.03.05.21.29'

To _continuously_ restore the _latest_ backup use. For development purposes of course. This will perform a restore whenever a more recent created backup file becomes available. 

    backup_restore:
       sonarqube: '*'

## 

Ansible module `postgresql_db` ignores any and all errors during execution of PostgreSQL commands. As a workaround for this bug, use `failed_when`.

      register: db_restore
      failed_when: "'ERROR' in db_restore.stderr"  
