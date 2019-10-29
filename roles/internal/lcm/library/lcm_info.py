#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib

# Determine operation: install, update, upgrade, 
#   rollback of rollforward
def operation(data, vsn_file_current, vsn_file):
  cv = None
  if os.path.isfile(vsn_file_current):
    cv = open(vsn_file_current, 'r').read()
    if cv == data['version']:
      operation = 'update'
      descr = 'Current ' + cv + ' is same as requested'
    else:
      seq = data['versions_sequence']
      cv_indx = seq.index(cv)
      v_indx = seq.index(data['version'])
      if cv_indx > v_indx:
        if os.path.isfile(vsn_file):
          operation = 'rollback'
          descr = 'Rollback ' + cv + ' to ' + data['version'] 
        else:
          operation = 'install'
          descr = 'Install ' + data['version'] + ' - downgrades are not supported' 
      elif cv_indx < v_indx:
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

def database_version(data,vsn):
  if vsn is None:
    vsn = data['version'] 
  return data['database'] + '_' + vsn.replace('.', '_')

def home_version(data,vsn):
  return os.path.join(os.path.sep,data['home'],os.path.basename(data['home']) + '-' + vsn)

def home_link(data):
  return os.path.join(os.path.sep, data['home'], os.path.basename(data['home']))

def version_file_link(data):
  return os.path.join(os.path.sep, home_link(data),'VERSION')

def version_file(data,vsn):
  return os.path.join(os.path.sep, home_version(data,vsn),'VERSION')

def lcm_info(data):
  has_changed = False
  role =  data['role']
  vsn_file_current = version_file_link(data)
  vsn_file = version_file(data,data['version'])   
  if os.path.isdir(home_version(data,data['version'])):
    open(vsn_file,'w').write(data['version'])
  op, op_descr, cv = operation(data,vsn_file_current, vsn_file) 
  fcts = {role + '_lcm':{"operation": op,
  "operation-description": op_descr,
  "version-file": vsn_file},
  role + '_home_link': home_link(data)}
  fcts[role + '_home_version'] = home_version(data,data['version'])
  if data['database'] is not None:
    fcts[role + '_database_name_version'] = database_version(data,data['version'])
  if op == 'upgrade':
    if data['database'] is not None:
      fcts[role + '_database_template'] = database_version(data,cv)
    fcts[role + '_home_version_current'] = home_version(data,cv)    
  return (has_changed, fcts)

def main():

  fields = {"role": {"required": True, "type": "str"},
    "home": {"required": True, "type": "str"},
    "version": {"required": True, "type": "str"},
    "versions_sequence": {"required": True, "type": "list"},
    "database": {"required": False, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts = lcm_info(module.params)
  module.exit_json(changed=has_changed, ansible_facts=fcts)
if __name__ == '__main__':
    main()