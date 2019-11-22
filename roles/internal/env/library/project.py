#!/usr/bin/python

from ansible.module_utils.basic import *

def project_info(data):
  has_changed = False
  fcts = {}
  fcts['env_project_groups'] = {}
  for grp_nm in ['admins', 'users', 'members']:
    grp_cn = data['key'] + '-' + grp_nm
    fcts['env_project_groups'][grp_cn] = {}
    fcts['env_project_groups'][grp_cn]['cn'] = grp_cn
    fcts['env_project_groups'][grp_cn]['member'] = []
    for m in data[grp_nm]:
      fcts['env_project_groups'][grp_cn]['member'].append('uid=' + m + ',' + data['people_base_dn'])
  return (has_changed, fcts)

def main():

  fields = {"key": {"required": True, "type": "str"},
    "name": {"required": True, "type": "str"},
    "admins": {"required": True, "type": "list"},
    "members": {"required": True, "type": "list"},
    "users": {"required": False, "type": "list"},
    "people_base_dn": {"required": True, "type": "str"}}

  module = AnsibleModule(argument_spec=fields)
  has_changed, fcts = project_info(module.params)
  module.exit_json(changed=has_changed, ansible_facts=fcts)
if __name__ == '__main__':
    main()