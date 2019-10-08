#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib

def tar_sha256sum(tar):
  tsf = tar_sha256sum_file(tar)
  if not os.path.isfile(tsf):
    sha256_hash = hashlib.sha256()
    with open(tar,"rb") as f:
      for byte_block in iter(lambda: f.read(4096),b""):
          sha256_hash.update(byte_block)
    open(tsf,'w').write(sha256_hash.hexdigest()) 
  return open(tsf, 'r').read()

def tar_sha256sum_file(tar):
  return tar + '.sha256sum'

# Sort tars descending creation
def sorted_tars(trs):
  trs.sort(key=os.path.getmtime)
  trs.reverse()
  return trs

# /backup/tmp/myapp-myapp/myapp_daily/archives/home.tar.gz
def home_tar(tmp,tar):
  return os.path.join(os.path.sep,tar_extracted(tmp,tar),'archives','home.tar.gz')

# /backup/tmp/myapp-myapp/myapp_daily/databases/PostgreSQL.sql.gz
def db_tar(tmp,tar):
  return os.path.join(os.path.sep,tar_extracted(tmp,tar),'databases','PostgreSQL.sql.gz')

# /backup/tmp/myapp-myapp/myapp_daily
def tar_extracted(tmp, tar):
  bn = os.path.basename(tar) 
  fldr = os.path.splitext(bn)[0]
  return os.path.join(os.path.sep,tmp,fldr) 

def get_restore_info(data):
  has_changed = False
  if '/' not in data['path_pattern']:
    ptrn = os.path.join(os.path.sep,data['backup_archives'],'*/' + data['role'] + '_*/' + data['path_pattern'] + '/*.tar') 
  else:
    ptrn = data['backup_archives']
  trs = []
  restore_info = []
  for tr in glob.glob(ptrn):
    trs.append(tr)
  #raise ValueError('trs'+trs[0]+'sorted'+sorted_tars(trs)[0]) 
  for tr in sorted_tars(trs):
    s256 = tar_sha256sum(tr)
    if s256 not in data['restored'] or data['force'] == True:
      restore_info.append({"path":tr, "sha256sum": s256})
      has_changed = True
  if has_changed:
    fcts = restore_facts(data, restore_info, ptrn)
    tr = restore_info[0]['path']
  else:
    fcts = {'backup_restore':{"path_pattern_expanded": ptrn}}
  return (has_changed, fcts, tr)

def restore_facts(data, restore_info, ptrn):
  hm_extracted = os.path.join(os.path.sep, data['tmp'], 'home')
  tr_extracted = tar_extracted(data['tmp'], restore_info[0]['path'])
  fcts = { 'backup_restore': 
          {data['role']: {
            "tar_extracted": tr_extracted,
            "tar":restore_info[0]['path'],
            "sha256sum":restore_info[0]['sha256sum'],
            "path_pattern_expanded": ptrn,
            "tmp": data['tmp'],
            "home_extracted": hm_extracted,
            "tars": restore_info
          }}}
  if data['home_version']:
    fcts['backup_restore'][data['role']]['rsync-target'] = data['home_version'] + '/'
    fcts['backup_restore'][data['role']]['rsync-src'] = hm_extracted + '/'
    if data['folder']:
      fcts['backup_restore'][data['role']]['rsync-target'] =  os.path.join(os.path.sep, data['home_version'], data['folder']) + '/'
      fcts['backup_restore'][data['role']]['rsync-src'] =  os.path.join(os.path.sep, hm_extracted, data['folder']) + '/'
  if data['home_version']:
    fcts['backup_restore'][data['role']]['home_tar'] = home_tar(data['tmp'], restore_info[0]['path'])
  if data['database']:
    fcts['backup_restore'][data['role']]['db_tar'] = db_tar(data['tmp'], restore_info[0]['path'])
  return fcts

def main():

  fields = {
    "backup_archives": {"required": True, "type": "str"},
    "role": {"required": True, "type": "str"},
    "path_pattern": {"required": True, "type": "str"},
    "force": {"required": True, "type": "bool"},
    "restored": { "required": True, "type": "list"},
    "folder": { "required": False, "type": "str"},
    "database": { "required": True, "type": "bool"},
    "home_version": { "required": True, "type": "str"},
    "tmp": {"required": True, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts, tr = get_restore_info(module.params)
  if has_changed:
    module.exit_json(changed=has_changed, ansible_facts=fcts, msg=tr)
  else:
    module.exit_json(changed=has_changed, ansible_facts=fcts)

if __name__ == '__main__':
    main()