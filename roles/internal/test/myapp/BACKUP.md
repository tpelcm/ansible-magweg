# Incremental and snapshot backups

The [backup](../backup) rol also supports incremental backups and backups using snapshots. Incremental backups can be used when there is a lot of data to backup. Snapshots can be used for zero or near zero downtime backups.

The [../myapp](../myapp) role is used to explain how this works. If you want to use this role yourself to test drive the features you should enable the **myapp** node in the [Vagrantfile](../../../../vagrant/Vagrantfile)

## Provision MyApp

    vagrant up myapp

## Default

First we take a look at an ordinary default backup. Ssh into the myapp machine and take a look at the `/etc/backup/models/myapp.rb`. It configures the backup to:

1. Backup the database `myapp_0_1_0`.
2. Backup the home directory `/opt/myapp/myapp-0.1.0`.
3. Store it on the NFS backup share using path `/backup/archives/myapp`.
4. Run *before* and *after* hooks which stop and start the myapp service. See `/etc/backup/hooks/myapp.sh`.

We can run the backup using the alias `tpelcm-myapp-daily-backup`. This creates a tar on the backup NFS share for example `/backup/archives/myapp/myapp_daily_0_1_0/2020.07.15.04.03.54/myapp_daily_0_1_0.tar`

```bash
[root@myapp ~]# tpelcm-myapp-daily-backup 
[root@myapp ~]# tree /backup/archives/myapp
/backup/archives/myapp
└── myapp_daily_0_1_0
    └── 2020.07.15.04.03.54
        └── myapp_daily_0_1_0.tar

2 directories, 1 file
[root@myapp ~]# tar tvf /backup/archives/myapp/myapp_daily_0_1_0/2020.07.15.04.03.54/myapp_daily_0_1_0.tar 
drwxr-xr-x root/root         0 2020-07-14 21:03 myapp_daily_0_1_0/
drwxr-xr-x root/root         0 2020-07-14 21:03 myapp_daily_0_1_0/databases/
-rw-r--r-- root/root       637 2020-07-14 21:03 myapp_daily_0_1_0/databases/PostgreSQL.sql.gz
drwxr-xr-x root/root         0 2020-07-14 21:03 myapp_daily_0_1_0/archives/
-rw-r--r-- root/root       346 2020-07-14 21:03 myapp_daily_0_1_0/archives/home.tar.gz
[root@myapp ~]# 
```

## Snapshots

The use of snapshots is enabled using `snapshot: yes` which you can configure for example in `host_vars/myapp.yml`. 

```yaml
backup_roles:
  myapp:
    keep: { daily: 3, weekly: 2, monthly: 1, manual: 0 }
    snapshot: yes
    # incremental: yes
```

Now provision the myapp node and take another look at `/etc/backup/models/myapp.rb`. Notice the differences with an ordinary backup:

1. The database changed to `myapp_0_1_0_snapshot`.
2. The home directory changed to `/opt/myapp-snapshot/myapp-0.1.0`. 
3. The hooks file `/etc/backup/hooks/myapp.sh` changed significantly.

The *before* hook now also contains code to:

1. Create a LVM snapshot `myapp-snapshot`.
2. Create a PostgreSQL snapshot `myapp_0_1_0_snapshot` of the database `myapp_0_1_0` to backup.
3. Start the *myapp* service.

```bash
  echo "myapp before hook $(date)" >> $BACKUP_LOGFILE 2>&1
  try mountpoint -q /backup >> $BACKUP_LOGFILE 2>&1
  try systemctl stop myapp >> $BACKUP_LOGFILE 2>&1
  umount /opt/myapp-snapshot 2> /dev/null | true
  lvdisplay data/myapp-snapshot &>/dev/null
  if [ $? -eq 0 ]
  then
    echo "Snapshot volume still exists!" >> $BACKUP_LOGFILE 2>&1
    try lvremove -f /dev/data/myapp-snapshot  >> $BACKUP_LOGFILE 2>&1
  fi
  try lvcreate -prw -L1G -s -n myapp-snapshot /dev/mapper/data-myapp >> $BACKUP_LOGFILE 2>&1
  try mkdir -p /opt/myapp-snapshot >> $BACKUP_LOGFILE 2>&1
  try mount /dev/data/myapp-snapshot /opt/myapp-snapshot >> $BACKUP_LOGFILE 2>&1
  try psql -v v1=myapp_0_1_0 -v v2=myapp_0_1_0_snapshot -v v3=myapp -h 1.1.1.2 -p 5432 -U ansible postgres < /etc/backup/scripts/db_snapshot.sql >> $BACKUP_LOGFILE 2>&1
  try systemctl start myapp >> $BACKUP_LOGFILE 2>&1
```

In the *after* hook the snapshots are remove again.

```bash
  echo "myapp after hook $(date)" >> $BACKUP_LOGFILE 2>&1
  try umount /opt/myapp-snapshot >> $BACKUP_LOGFILE 2>&1
  try lvremove -f /dev/data/myapp-snapshot  >> $BACKUP_LOGFILE 2>&1
  try mkdir -p /opt/myapp-snapshot >> $BACKUP_LOGFILE 2>&1
  try psql -v v1=myapp_0_1_0_snapshot -h 1.1.1.2 -p 5432 -U ansible postgres < /etc/backup/scripts/db_snapshot_drop.sql >> $BACKUP_LOGFILE 2>&1
```

To create a backup using snapshots use the alias `tpelcm-myapp-daily-backup` same as before. 

## Incremental using snapshots

In addition to snapshots for backup with minimal downtime we can now also use incremental backups. This is configured with `incremental: yes`. For example in `host_vars/myapp.yml`. 

```yaml
backup_roles:
  myapp:
    keep: { daily: 3, weekly: 2, monthly: 1, manual: 0 }
    snapshot: yes
    incremental: yes
```

Now provision the myapp node and take another look at `/etc/backup/models/myapp.rb`. Notice the differences with an snapshot backup:

1. The home directory is no longer in the model file `/opt/myapp-snapshot/myapp-0.1.0`. 
3. A backup of the database `myapp_0_1_0_snapshot` is still created but now it is stored in the snapshot directory `/opt/myapp-snapshot/myapp-0.1.0/db`.
3. The hooks file `/etc/backup/hooks/myapp.sh` also changed a lot as shown below.

The hook file contains extra code for rsnapshot which is used to create incremental backups.

```bash
case $3 in
  "daily") rsnapshot_level=alpha;;
  "weekly") rsnapshot_level=beta;;
  "monthly") rsnapshot_level=gamma;;
  "manual") rsnapshot_level=alpha;;
esac

case $rsnapshot_level in
  "alpha") rsnapshot_level_runs=(alpha);;
  "beta") rsnapshot_level_runs=(beta alpha);;
  "gamma") rsnapshot_level_runs=(gamma beta alpha);;
esac
```

The *before* hook is the same as before. The *after* hook is different. It calls the `rsnapshot` utility.

```bash
  for rlr in ${rsnapshot_level_runs[*]}
  do
    try /bin/rsnapshot -c /etc/backup/rsnapshot/myapp.conf $rlr >> $BACKUP_LOGFILE 2>&1
  done
```
The rsnapshot config file `/etc/backup/rsnapshot/myapp.conf` contains amongst other things the following:

    snapshot_root   /backup/snapshots/myapp/myapp-0.1.0
    retain  alpha   3
    retain  beta    2
    retain  gamma   1
    backup  /opt/myapp-snapshot/myapp-0.1.0 ./

### Rsnapshot backup levels

Rsnapshot backup levels differ a lot from schedules with a tar backup. 

1. Backup levels are sorted *alphabetically*! The **alpha** level is the first level, **beta** second and **gamma** third.
2. Only **alpha** will backup the current data. Higher levels will only perform recycling of existing snapshot folders.
3. To correctly perform a higher level backup, you run that level and then all lower levels in descending sequence. For a monthly backup for example run **gamma**, then **beta**, then **alpha**.
4. The first directory which is **alpha.0** always contains the most recent backup.

To elaborate this further as before create backup same as before using alias `tpelcm-myapp-daily-backup`. In directory `/backup/snapshots` we have a first backup of our application. Notice the `db` folder. It containers our database. 

```bash
[root@myapp ~]# tpelcm-myapp-daily-backup 
[root@myapp ~]# tree -L 3 /backup/snapshots/myapp
/backup/snapshots/myapp
└── myapp-0.1.0
    └── alpha.0
        ├── data
        ├── db
        ├── delete.sh
        ├── insert.sh
        ├── myapp.txt
        ├── select.sh
        ├── start.sh
        ├── stop.sh
        └── VERSION
```

The we run daily another two times and then weekly using alias `tpelcm-myapp-daily-backup`. The weekly backup executed `rsnapshot` with level **beta** and then **alpha**. 

The **beta** level did not backup anything. It just renamed `alpha.2` to `beta.0`. Two alpha levels remained. Then **alpha** was executed. This does the following:

1. `alpha.1` renamed to `alpha.2`
2. `alpha.0` renamed to `alpha.1` 
3. Backup data to a new `alpha.0`

```
[root@myapp ~]# tree -L 2 /backup/snapshots/myapp
/backup/snapshots/myapp
└── myapp-0.1.0
    ├── alpha.0
    ├── alpha.1
    ├── alpha.2
    └── beta.0
```

## Incremental without snapshots

Of course it is also possible to create incremental backups without snapshots. Configure `snapshots: no` and provision again. Notice the following differences compare to before - incremental with snapshots:

1. Rsnapshot config `/etc/backup/rsnapshot/myapp.conf` now has `/opt/myapp/myapp-0.1.0` configered for backup.
2. The backup model `/etc/backup/models/myapp.rb` now has database `myapp_0_1_0` configured. This database is stored in the `opt/myapp/myapp-0.1.0/db`.
3. The hooks file `/etc/backup/hooks/myapp.sh` of course is much simpler. The *before* hook stops the myapp service. The *after* hook calls `rsnapshot` and starts the service. 




