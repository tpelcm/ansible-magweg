#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib

# Determine operation: install, update, upgrade, 
#   rollback of rollforward
def operation(data, vsn_file_current, vsn_file):
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
  return operation, descr

def lcm_info(data):
  has_changed = False
  role =  data['role']
  lnk = os.path.join(os.path.sep, data['home'], os.path.basename(data['home']))
  vsn_file_current = os.path.join(os.path.sep, lnk,'VERSION')
  vsn_file = os.path.join(os.path.sep, data['home_version'],'VERSION')
  if os.path.isdir(data['home_version']):
    open(vsn_file,'w').write(data['version'])
  op, op_descr = operation(data,vsn_file_current, vsn_file) 

  fcts = {role + '_lcm':{"operation": op,
  "operation-description": op_descr,
  "version-file": vsn_file},
  role + '_home_link': lnk}
  return (has_changed, fcts)

def main():

  fields = {"role": {"required": True, "type": "str"},
    "home": {"required": True, "type": "str"},
    "version": {"required": True, "type": "str"},
    "versions_sequence": {"required": True, "type": "list"},
    "home_version": {"required": True, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts = lcm_info(module.params)
  module.exit_json(changed=has_changed, ansible_facts=fcts)
if __name__ == '__main__':
    main()