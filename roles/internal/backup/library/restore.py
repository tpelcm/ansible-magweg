#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os, hashlib

def restore(data):
  has_changed = False
  meta = { "tar": data['tar'],
  "role": data['role'],
  "restored": data['restored'] }
  if os.path.isfile(data['tar']['path']):
    raise ValueError('Tar ' + data['tar']['path'] + ' not found!')
  return (has_changed, meta)
def main():

  fields = {
    "tar": {"required": True, "type": "str"},
    "role": {"required": True, "type": "str"},
    "restored": { "required": True, "type": "list"},
    "state": {
          "default": "perform", 
          "choices": ["perform"],  
          "type": "str" 
        },        
      }
  choice_map = {
    "perform": restore,
  }

  module = AnsibleModule(argument_spec=fields)
  has_changed, result = choice_map.get(module.params['state'])(module.params)
  module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()