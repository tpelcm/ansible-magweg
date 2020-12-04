#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib, uuid

# Get checksum of backup tar file
def tar_sha256sum(tar):
  tsf = tar_sha256sum_file(tar)
  if not os.path.isfile(tsf):
    sha256_hash = hashlib.sha256()
    with open(tar,"rb") as f:
      for byte_block in iter(lambda: f.read(4096),b""):
          sha256_hash.update(byte_block)
    open(tsf,'w').write(sha256_hash.hexdigest())
  return open(tsf, 'r').read()

# Get id of the snapshot backup
# The snapshot id is created in the before hook e.g. /etc/backup/hooks/myapp.sh
def snapshot_id(ss, data):
  sid_file = snapshot_id_file(ss, data)
  return open(sid_file, 'r').read().rstrip()

# Path of file with checksum for tar /backup/archives/myapp/myapp_daily_0_1_0/2020.07.15.10.54.02/ 
def tar_sha256sum_file(tar):
  return tar + '.sha256sum'

# e.g. /backup/snapshots/myapp/myapp-0.1.0/alpha.0/.backup-id
# this file is created by the hooks file e.g. /etc/backup/hooks/myapp.sh 
def snapshot_id_file(ss, data):
  return os.path.join(os.path.sep,ss,'home',data['backup_rsnapshot_id_file'])

# Sort tars descending creation
def sorted_tars(trs):
  trs.sort(key=os.path.getmtime)
  trs.reverse()
  return trs

# Sort snapshots alphabetically
def sorted_snapshots(sns):
  return sorted(sns)

# e.g. /backup/tmp/myapp-myapp/myapp_daily/archives/home.tar.gz
def home_tar(tmp,tar):
  return os.path.join(os.path.sep,tar_extracted(tmp,tar),'archives','home.tar.gz')

# e.g. /backup/tmp/myapp-myapp/myapp_daily/databases/PostgreSQL.sql.gz or
# /backup/tmp/myapp-myapp/myapp_daily/archives/database.sql.gz for oracle
def db_tar(tmp,tar,db_type,snapshot=False):
  if db_type == 'postgresql': # default
      return os.path.join(os.path.sep,tar_extracted(tmp,tar),'databases','PostgreSQL.sql.gz')
  else: # oracle
      if snapshot == False:
          return os.path.join(os.path.sep,tar_extracted(tmp,tar),'archives','database.tar.gz')
      else:
          return tar

# e.g. /backup/tmp/myapp-myapp/myapp_daily
def tar_extracted(tmp, tar):
  bn = os.path.basename(tar) 
  fldr = os.path.splitext(bn)[0]
  return os.path.join(os.path.sep,tmp,fldr) 

# e.g /opt/myapp/RESTORED
def restored_file(data):
  return os.path.join(os.path.sep,data['home'],'RESTORED')

# Check if tar or snapshot has already been restored
def not_restored(s256,data):
  f = restored_file(data)
  if os.path.isfile(f):
    rstrd = open(f, 'r').read()
    if s256 in rstrd:
      return False
    else:
      return True
  else: # create restore file
    if os.path.isdir(data['home']):
      open(f,'w').write('Restored tar sha256sums / snapshot ids: ') 
    return True

def get_remove_folder(data):
  return os.path.join(os.path.sep,data['home_version'],data['remove_folder'])

# Get a search pattern for the backup folder name
# e.g. myapp_0_1_0* for tar backup
#  or plain myapp
def backup_name_underscored_pattern(data):
  if data['incremental']:
    return data['backup_name_underscored'] 
  else:
    return data['backup_name_underscored'] + '*'

# Get a search pattern for the backup tar or snapshot path e.g
# for a snapshot: /backup/snapshots/*/myapp_0_1_0/*
# for a tar: /backup/archives/*/myapp_0_1_0*/*/*.tar
# to find for example /backup/archives/myapp/myapp_0_1_0_daily/2020.07.16.05.44.20/myapp_0_1_0_daily.tar
# or snapshot /backup/snapshots/myapp/myapp_0_1_0/alpha.0
def expand_path_pattern(data):
  if '/' not in data['path_pattern']:
    if data['incremental']:
      ptrn = os.path.join(os.path.sep,data['backup_snapshots'],'*', backup_name_underscored_pattern(data), data['path_pattern'])
    else:
      ptrn = os.path.join(os.path.sep,data['backup_archives'],'*', backup_name_underscored_pattern(data), data['path_pattern'],'*.tar')
  else:
    ptrn = data['path_pattern']
  return ptrn

def get_restore_info_snapshot(data):
  tr = None
  has_changed = False
  ptrn = expand_path_pattern(data)
  snapshots = []
  restore_info = []
  for ss in glob.glob(ptrn):
    snapshots.append(ss)
  for ss in sorted_snapshots(snapshots):
    ssid = snapshot_id(ss, data)
    restore_info.append({"path":ss, "backup-id": ssid, "restored": not not_restored(ssid,data) }) 
  if len(restore_info) > 0 and (restore_info[0]["restored"] == False or data['force'] == True):
    has_changed = True
  if has_changed:
    fcts = restore_facts_snapshots(data, restore_info, ptrn)
    tr = restore_info[0]['path']
  else:
    fcts = { 'backup_restore': 
            {data['role']: {
              "path_pattern_expanded": ptrn,              
              "snapshots": restore_info
            }}}
  return (has_changed, fcts, tr)

def get_restore_info_tar(data):
  tr = None
  has_changed = False
  ptrn = expand_path_pattern(data)
  trs = []
  restore_info = []
  for tr in glob.glob(ptrn):
    trs.append(tr)
  for tr in sorted_tars(trs):
    s256 = tar_sha256sum(tr)
    restore_info.append({"path":tr, "backup-id": s256, "restored": not not_restored(s256,data)})
  if len(restore_info) > 0 and (restore_info[0]["restored"] == False or data['force'] == True):
    has_changed = True
  if has_changed:
    fcts = restore_facts(data, restore_info, ptrn)
    tr = restore_info[0]['path']
  else:
    fcts = { 'backup_restore': 
            {data['role']: {
              "path_pattern_expanded": ptrn,              
              "tars": restore_info
            }}}
  return (has_changed, fcts, tr)

def get_restore_info(data):
  if data['incremental']:
    return get_restore_info_snapshot(data)
  else:
    return get_restore_info_tar(data)

# Restore facts for snapshots
def restore_facts_snapshots(data, restore_info, ptrn):
  fcts = { 'backup_restore': 
          {data['role']: {
            "path": restore_info[0]['path'],
            "backup-id":restore_info[0]['backup-id'],
            "path_pattern_expanded": ptrn,
            "tmp": data['tmp'],
            "snapshots": restore_info,
            "restored-file": restored_file(data)
          }}}
  if data['home_version']:
      fcts['backup_restore_home'] = True
      fcts['backup_restore'][data['role']]['rsync-target'] = data['home_version'] + '/'
      fcts['backup_restore'][data['role']]['rsync-src'] = restore_info[0]['path'] + '/home/'
      if data['folder']:
          fcts['backup_restore'][data['role']]['rsync-target'] =  os.path.join(os.path.sep, data['home_version'], data['folder']) + '/'
          fcts['backup_restore'][data['role']]['rsync-src'] =  os.path.join(os.path.sep, restore_info[0]['path'], data['folder']) + '/home/'
  if data['database']:
      if data['database_type'] == 'postgresql':
          ptrn = os.path.join(restore_info[0]['path'],data['backup_rsnapshot_backup_db_folder'],'*.tar')
          # e.g. ptrn is /backup/snapshots/myapp/myapp-0.1.0/alpha.0/database/*.tar 
          # tar is for example confluence_6_14_3_daily.tar
      else:
          ptrn = os.path.join(restore_info[0]['path'],data['backup_rsnapshot_backup_db_folder'],'*.tar.gz')
          # e.g. ptrn is /backup/snapshots/myapp/myapp-0.1.0/alpha.0/database/*.tar.gz
      fcts['backup_restore'][data['role']]['snapshot-tar-pattern'] = ptrn
      trs = glob.glob(ptrn)
      if trs:
          tr = trs[0]
          # e.g. tr is /backup/snapshots/myapp/myapp-0.1.0/alpha.0/database/myapp_weekly_0_1_0.tar
          fcts['backup_restore'][data['role']]['tar'] = tr
          fcts['backup_restore'][data['role']]['db_tar'] = db_tar(data['tmp'], tr, data['database_type'], True)
          fcts['backup_restore_db'] = True
      else:
          fcts['backup_restore_db'] = False
  if data['remove_folder']:
      fcts['backup_restore'][data['role']]['remove_folder_expanded'] = get_remove_folder(data)
  return fcts

# Restore facts for tar files
def restore_facts(data, restore_info, ptrn):
  hm_extracted = os.path.join(os.path.sep, data['tmp'], 'home')
  tr_extracted = tar_extracted(data['tmp'], restore_info[0]['path'])
  fcts = { 'backup_restore': 
          {data['role']: {
            "tar_extracted": tr_extracted,
            "tar":restore_info[0]['path'],
            "backup-id":restore_info[0]['backup-id'],
            "path_pattern_expanded": ptrn,
            "tmp": data['tmp'],
            "home_extracted": hm_extracted,
            "tars": restore_info,
            "restored-file": restored_file(data)
          }}}
  if data['home_version']:
    fcts['backup_restore_home'] = True
    fcts['backup_restore'][data['role']]['rsync-target'] = data['home_version'] + '/'
    fcts['backup_restore'][data['role']]['rsync-src'] = hm_extracted + '/'
    if data['folder']:
      fcts['backup_restore'][data['role']]['rsync-target'] =  os.path.join(os.path.sep, data['home_version'], data['folder']) + '/'
      fcts['backup_restore'][data['role']]['rsync-src'] =  os.path.join(os.path.sep, hm_extracted, data['folder']) + '/'
  if data['home_version']:
    fcts['backup_restore'][data['role']]['home_tar'] = home_tar(data['tmp'], restore_info[0]['path'])
  if data['database']:
    fcts['backup_restore'][data['role']]['db_tar'] = db_tar(data['tmp'], restore_info[0]['path'], data['database_type'])
    fcts['backup_restore_db'] = True
  if data['remove_folder']:
    fcts['backup_restore'][data['role']]['remove_folder_expanded'] = get_remove_folder(data)
  return fcts

def main():

  fields = {
    "backup_name_underscored": {"required": True, "type": "str"},
    "backup_archives": {"required": True, "type": "str"},
    "backup_snapshots": {"required": True, "type": "str"},
    "backup_rsnapshot_id_file": {"required": True, "type": "str"},
    "backup_rsnapshot_backup_db_folder": {"required": True, "type": "str"},
    "role": {"required": True, "type": "str"},
    "path_pattern": {"required": True, "type": "str"},
    "force": {"default": False, "type": "bool"},
    "folder": { "required": False, "type": "str"},
    "remove_folder": { "required": False, "type": "str"},
    "database": { "required": True, "type": "bool"},
    "database_type": { "required": True, "type": "str"},
    "home_version": { "required": True, "type": "str"},
    "home_backup_version": { "required": True, "type": "str"},   
    "incremental": { "required": False, "type": "bool"},   
    "home": { "required": True, "type": "str"},
    "tmp": {"required": True, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts, tr = get_restore_info(module.params)
  module.exit_json(changed=has_changed, ansible_facts=fcts, msg=tr)

if __name__ == '__main__':
    main()