
An Ansible Role that configures the backup utility for supported roles for example __myapp__. This role can also be used to restore a backup.

## Backup

Installs the backup utility and configures backup models for supported roles (`backup_roles_supported`).

- If the role has a `<role>_home` fact, this will be part of the backup.
- If the role has `<role_database_name` fact, this will be part of the backup.

Database and file system are archived together in a file for example similar to 

    /backup/archives/sonarqube/sonarqube_daily/2019.10.03.05.21.29/sonarqube_daily.tar`. 

The path is created as follows 

    {{ backup_archives }}/{{ inventory_hostname }}/{{ role }}_{{ schedule }}/{{ date-time }}/{{ role }}_{{ schedule }}.tar`. 

## Restore

To support restore a `backup_restore` fact should be configured for example as follows

    ---
    backup_restore: 
      myapp:
        path_pattern: '*'
        folder: data
        force: false  

A custom ansible module __restore_info.py__ is used to gather restore facts to enable subsequent tasks to perform the restore.

- `myapp` is the Ansible role selected for restore.
- `path_pattern` `*` will select the most recent backup file for restore. This pattern will be expanded to for example `/backup/archives/*/myapp_*/*/*.tar`. Alternatively use a full path for example `/backup/archives/myapp2/myapp_*/*/*.tar`. This will select only backups from node with `inventory_hostname` equal to `myapp2`.
- Leave `folder` empty to restore complete home directory ( `<role>_home` ). Enter a subdirectory or path to limit restore to a specific directory.
- Use `force` to force restore even if restored has already been performed. 

## Issues 

Ansible module `postgresql_db` ignores any and all errors during execution of PostgreSQL commands. As a workaround for this bug, `failed_when` is used.

      register: db_restore
      failed_when: "'ERROR' in db_restore.stderr"  
