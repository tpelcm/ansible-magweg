
An Ansible Role that configures the backup utility for supported roles for example __myapp__. This role can also be used to restore a backup.

## Backup

Installs the backup utility and configures backup models for supported roles (`backup_roles_supported`).

- If the role has a `<role>_home` fact, this will be part of the backup.
- If the role has `<role_database_name` fact, this will be part of the backup.

Database and file system are archived together in a file for example similar to 

    /backup/archives/sonarqube/sonarqube_daily/2019.10.03.05.21.29/sonarqube_daily.tar

The path is created as follows 

    {{ backup_archives }}/{{ inventory_hostname }}/{{ role }}_{{ schedule }}/{{ date-time }}/{{ role }}_{{ schedule }}.tar

For each supported role default settings are configured for example

    backup_roles:
      jira:
        stop_start_service: jira
        keep: { daily: 3, weekly: 1, monthly: 0, manual: 1 }

If you don't want to stop and start services or containers override default settings using `no` as follows

    backup_roles:
      jira:
        stop_start_service: no

If you want to skip the database backup use `skip_database` for example as shown below

    backup_roles:
      jira:
        stop_start_service: jira
        keep: { daily: 3, weekly: 2, monthly: 0, manual: 1 }
        skip_database: yes

## Restore

To support restore a `backup_restore` fact should be configured for example as follows

    ---
    backup_restore: 
      myapp:
        path_pattern: '*'
        folder: data
        force: false  

Additionally, you need to __confirm__ the restore by creating a file `/tmp/RESTORE` on the target node. If you don't create this file the restore will fail

    TASK [backup : Fail restore without confirmation] ******************************
    fatal: [bitbucket]: FAILED! => {"changed": false, "msg": "To perform the restore confirm it with touch /tmp/RESTORE"}

You can skip this confirmation requirement with `backup_restore_confirm: false`

A custom ansible module __restore_info.py__ is used to gather restore facts to enable subsequent tasks to perform the restore.

- `myapp` is the Ansible role selected for restore.
- `path_pattern` `*` will select the most recent backup file for restore. This pattern will be expanded to for example `/backup/archives/*/myapp_*/*/*.tar`. Alternatively use a full path for example `/backup/archives/myapp2/myapp_*/*/*.tar`. This will select only backups from node with `inventory_hostname` equal to `myapp2`.
- Leave `folder` empty to restore complete home directory ( `<role>_home` ). Enter a subdirectory or path to limit restore to a specific directory.
- Use `force` to force restore even if restored has already been performed. 

## LVM and database snapshots

It is possible to use LVM and database snapshots to create zero or near zero downtime backups. To backup Confluence using this feature configure for example:

    backup_roles:
      confluence:
        snapshot: yes
        backup_lvm_snapshot_size: 2G

## Incremental backups

Icremental backups using [rsnapshot](https://rsnapshot.org/) are supported. To use incremental backups use `incremental: yes` for example as follows:

    backup_roles:
      confluence:
        incremental: yes

Rsnapshots has the concept of backup levels to configure levels for rotation. __These levels must be unique and in ascending order__. Schedules are translated to a rsnapshot level.

    backup:
      rsnapshot_levels:
        daily: alpha
        weekly: beta
        monthly: gamma

The most recent backup is always __alpha.0__.

If you running a higher level backup e.g. *beta* or *gamma* this will not backup anything. It will just rename the highest / oldest alpha level to a beta level.

So to perform a weekly backup first run the higher level and then the lower level backup.

    /bin/rsnapshot -c /etc/backup/rsnapshot/test.conf beta # e.g. alpha.2 → beta.0
    /bin/rsnapshot -c /etc/backup/rsnapshot/test.conf alpha # e.g. → alpha.0

To perform a monthly backup you first run *gamma*, then *beta*, then *alpha*.

To understand in detail how this works see the [BACKUP.md](../myapp/BACKUP.md) in the [myapp](../myapp) role. 

## Troubleshooting

Script are setup in such a way to help troubleshooting. You can for example run script yourself. For example to run __confluence__ model before hook:

    /etc/backup/hooks/confluence.sh before daily


## Issues 

Ansible module `postgresql_db` ignores any and all errors during execution of PostgreSQL commands. As a workaround for this bug, `failed_when` is used.

      register: db_restore
      failed_when: "'ERROR' in db_restore.stderr"  
