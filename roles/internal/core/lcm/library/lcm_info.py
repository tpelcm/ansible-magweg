#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib

# Determine operation: install, update, upgrade, 
#   rollback of rollforward or prepare upgrade
def operation(data, vsn_file_current, vsn_file):
  cv = current_version(vsn_file_current)
  if cv:
    seq = data['versions_sequence']
    if version_equal(data, vsn_file_current, vsn_file):
      if data['version_prepare'] is not None:
        if prepare_version_higher(data, vsn_file_current, vsn_file):
          operation = 'prepare-upgrade'
          descr = 'Prepare upgrade to ' + data['version_prepare']
        else:
          operation = 'update'
          descr = 'Current ' + cv + ' is same as requested'
      else: # 
        operation = 'update'
        descr = 'Current ' + cv + ' is same as requested'
    else:
      if version_lower(data, vsn_file_current, vsn_file):
        if installed(data,data['version']):
          operation = 'rollback'
          descr = 'Rollback ' + cv + ' to ' + data['version'] 
        else:
          operation = 'install'
          descr = 'Install ' + data['version'] + ' - downgrades are not supported' 
      elif version_higher(data, vsn_file_current, vsn_file):
        if os.path.isfile(vsn_file):
          operation = 'rollforward'
          descr = 'Rollforward ' + cv + ' to ' + data['version']
        else:
          operation = 'upgrade'
          descr = 'Upgrade ' + cv + ' to ' + data['version']
  else:
    operation = 'install'
    descr = 'Install ' + data['version']
  return operation, descr, cv

def current_version(vsn_file_current):
  if os.path.isfile(vsn_file_current):
    return open(vsn_file_current, 'r').read().rstrip()
  else:
    return None

# Return true if version is already present on filesystem
# - when a version file can be found
def installed(data,version):
  vsn_file = version_file(data,version) 
  return os.path.isfile(vsn_file)

# Return true when current and requested version are equal
def version_equal(data, vsn_file_current, vsn_file):
  cv = current_version(vsn_file_current)
  return cv == data['version']

# Return true when requested version is higher
def version_higher(data, vsn_file_current, vsn_file):
  cv = current_version(vsn_file_current)
  seq = data['versions_sequence']
  cv_indx = seq.index(cv)
  v_indx = seq.index(data['version'])
  return cv_indx < v_indx

def prepare_version_higher(data, vsn_file_current, vsn_file):
  cv = current_version(vsn_file_current)
  seq = data['versions_sequence']
  cv_indx = seq.index(cv)
  v_indx = seq.index(data['version_prepare'])
  return cv_indx < v_indx

# Return true when requested version is lower
def version_lower(data, vsn_file_current, vsn_file):
  return not version_higher(data, vsn_file_current, vsn_file)

def database_version(data,vsn):
  if vsn is None:
    vsn = data['version'] 
  return data['database'] + '_' + vsn.replace('.', '_')

def database_version_backup(data,vsn):
  return database_version(data,vsn) + '_snapshot'

def home_version(data,vsn):
  return os.path.join(os.path.sep,data['home'],os.path.basename(data['home']) + '-' + vsn)

def home_backup(data,vsn):
  return data['home'] + '-snapshot'

def home_backup_version(data,vsn):
  return os.path.join(home_backup(data,vsn),os.path.basename(data['home']) + '-' + vsn)

def home_version_home(data,vsn):
  return os.path.join(home_version(data,vsn), 'home')

def home_version_app(data,vsn):
  return os.path.join(home_version(data,vsn), 'app')

def home_link(data):
  return os.path.join(os.path.sep, data['home'], os.path.basename(data['home']))

def home_link_home(data):
  return os.path.join(home_link(data), 'home')

def home_link_app(data):
  return os.path.join(home_link(data), 'app')

def version_file_link(data):
  return os.path.join(os.path.sep, home_link(data),'VERSION')

def version_file(data,vsn):
  return os.path.join(os.path.sep, home_version(data,vsn),'VERSION')

def lcm_info(data):
  has_changed = False
  role =  data['role']
  vsn_file_current = version_file_link(data)
  vsn_file = version_file(data,data['version'])   
  op, op_descr, cv = operation(data,vsn_file_current, vsn_file) 
  fcts = {role + '_lcm':{"operation": op,
  "operation-description": op_descr,
  "version-file": vsn_file},
  role + '_home_link': home_link(data)}
  fcts[role + '_lcm_operation'] = op
  if op in ['install', 'upgrade']:
    fcts['lcm_write_version_file'] = True
  fcts[role + '_home_backup'] = home_backup(data,data['version'])
  fcts[role + '_home_backup_version'] = home_backup_version(data,data['version'])
  fcts[role + '_home_version'] = home_version(data,data['version'])
  fcts[role + '_home_version_home'] = home_version_home(data,data['version'])
  fcts[role + '_home_version_app'] = home_version_app(data,data['version'])    
  fcts[role + '_home_link_home'] = home_link_home(data)
  fcts[role + '_home_link_app'] = home_link_app(data)
  if data['version_prepare'] is not None:
    fcts[role + '_home_version_prepare'] = home_version(data,data['version_prepare'])
    fcts[role + '_home_version_home_prepare'] = home_version_home(data,data['version_prepare'])
  if data['database'] is not None:
    fcts[role + '_database_name_version'] = database_version(data,data['version'])
    fcts[role + '_database_name_version_backup'] = database_version_backup(data,data['version'])
  if op == 'upgrade':
    if data['database'] is not None:
      fcts[role + '_database_template'] = database_version(data,cv)
    fcts[role + '_home_version_current'] = home_version(data,cv)
    fcts[role + '_home_version_home_current'] = home_version_home(data,cv)
    fcts[role + '_home_version_app_current'] = home_version_app(data,cv)
  return (has_changed, fcts)

def main():

  fields = {"role": {"required": True, "type": "str"},
    "home": {"required": True, "type": "str"},
    "version": {"required": True, "type": "str"},
    "version_prepare": {"required": False, "type": "str"},
    "versions_sequence": {"required": True, "type": "list"},
    "database": {"required": False, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts = lcm_info(module.params)
  module.exit_json(changed=has_changed, ansible_facts=fcts)
if __name__ == '__main__':
    main()