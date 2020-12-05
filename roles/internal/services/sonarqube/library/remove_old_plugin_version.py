#!/usr/bin/python

from ansible.module_utils.basic import *
import glob, os

def remove_old_plugin_version(data):
	has_changed = False
	glb = os.path.join(os.path.sep,data['plugin_dir'],data['pattern']) 
	plgns = []
	# https://stackoverflow.com/questions/58007184/why-does-my-ansible-module-fail-with-typeerror-itertools-imap-object-has-no-a
	for plgn in map(os.path.basename, glob.glob(glb)):
		plgns.append(plgn)
	if len(plgns) > 1:
		raise ValueError('Multiple version of plugin installed: ' + ', '.join(plgns))
	if len(plgns) == 0:
		meta = { "Not installed" }
	if len(plgns) == 1:
		plgn_installed = plgns[0]
		if plgn_installed == os.path.basename(data['url']):
			meta = { "Installed and current" }
		else:
			has_changed = True
			path_plgn = os.path.join(os.path.sep,data['plugin_dir'],plgn_installed) 
			os.remove(path_plgn)
			meta = { "Removed " + plgn_installed }
	return (has_changed, meta)

def main():

	fields = {
		"pattern": {"required": True, "type": "str"},
		"url": {"required": True, "type": "str" },
		"plugin_dir": {"required": True, "type": "str" },		
        "state": {
        	"default": "execute", 
        	"choices": ["execute"],  
        	"type": "str" 
        },        
			}
	choice_map = {
		"execute": remove_old_plugin_version,
	}

	module = AnsibleModule(argument_spec=fields)
	has_changed, result = choice_map.get(module.params['state'])(module.params)
	module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()