"""backup filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import json, os

# Return backup name without . or -
# e.g. myapp_0_1_0_daily
def backup_name_underscored(role,vars,schedule = None):
    bmn = '_'.join([role,vars[role+'_version']])
    if schedule is not None:
        bmn = '_'.join([bmn,schedule])
    return bmn.replace('.','_').replace('-','_')

# string - Transform python dict to line - Stack Overflow
# https://stackoverflow.com/questions/63682683/transform-python-dict-to-line
# .join(f'{key}={value}' for (key, value) in opts.items()) # python3
def expdp_options(role, vars):
    opts = {
      'schemas': role_schema_name(role,vars),
      'directory': role_dump_dir_name(role,vars),
      'dumpfile':  role_dump_file(role),
      'logfile':  role_dump_log_file(role,vars),
      'reuse_dumpfiles': 'Y',
      'filesize': '500M'
    }
    return pump_options(role,vars,opts)

def impdp_options(role, vars):
    opts = {
        'directory': role_dump_dir_name(role,vars),
        'dumpfile':  role_dump_file(role),
        'logfile':  role_dump_log_file(role,vars),
        'remap_schema': '$dump_schema:' + role_schema_name(role,vars),
        'remap_tablespace': '$dump_schema:' + role_schema_name(role,vars),
        'schemas': '$dump_schema'         
    }
    return pump_options(role,vars,opts, 'import')

def pump_options(role,vars,opts,imp_exp = 'export'):
    opts3 = {}
    opts2 = vars['backup_oracle_pump_options_' + imp_exp]
    for (key,value) in opts.items():
        if not key in opts2:
            opts3[key] = value
    for (key,value) in opts2.items():
        if opts2[key] != False:
          opts3[key] = value
    return ' '.join('%s=%s' % (key, value) for (key, value) in opts3.items())

def role_script_path(role, script = None):
    if script == None:
        return os.path.join(os.path.sep, '/etc/backup/hooks/',role)
    else:
        return os.path.join(os.path.sep, '/etc/backup/hooks/',role, script)

def role_dump_file(role):
    return (role + '_%U.dmp').upper()

def role_dump_log_file(role,vars):
    return vars['inventory_hostname'] + '.log'

def role_dump_dir(role, vars):
    return os.path.join(os.path.sep,
        vars['backup_tmp'],
        role_database_type(role, vars),
        vars['inventory_hostname'])

def role_database_type(role, vars):
    try:
        return vars[role + '_database_type']
    except KeyError:
        return 'postgresql'

def role_dump_dir_tar(role, vars):
    return os.path.join(os.path.sep, role_dump_dir(role,vars),'database.tar.gz')

def role_dump_dir_tar_tmp(role, vars):
    return os.path.join(os.path.sep, role_dump_dir(role,vars),"../",role+".tar.gz")

def role_dump_dir_name(role, vars):
    return (vars['inventory_hostname'] + '_dump_dir').upper().replace('-','_').replace(' ','_')

def role_dump_dir_remote(role, vars):
    return os.path.join(os.path.sep, vars['backup_oracle']['dump_dir_remote'],vars['inventory_hostname'])

def role_scn_file(role, vars):
    return os.path.join(os.path.sep, role_dump_dir(role,vars), 'SCN')

def role_schema_file(role, vars):
    return os.path.join(os.path.sep, role_dump_dir(role,vars), 'SCHEMA')

def role_schema_name(role, vars):
    return vars[role+'_database_username'].upper()

def role_tns_name(role, vars):
    return vars[role+'_database_name'].upper().split('.')[0]

def role_log_file_path(role, vars):
    return os.path.join(os.path.sep, vars['backup_logs'],role_log_file_name(role,vars))

def role_log_file_name(role, vars):
    return '%s-%s.log' % (vars['inventory_hostname'], role)

def role_rsnapshot_config_path(role, vars):
    return role_script_path(role, 'rsnapshot.conf')

def role_rsnapshot_root(role, vars):
    return os.path.join(os.path.sep, vars['backup_snapshots'],
      vars['inventory_hostname'],
      backup_name_underscored(role,vars))

def role_oracle_connect(role, vars):
    u = vars['backup_oracle']['backup_admin_user']
    p = vars['backup_oracle']['backup_admin_user_password']
    if 'backup_admin_user' in vars['backup_roles'][role]:
        u = vars['backup_roles'][role]['backup_admin_user']
    if 'backup_admin_user_password' in vars['backup_roles'][role]:
        p = vars['backup_roles'][role]['backup_admin_user_password']    
    s = role_tns_name(role,vars)
    return '%s/%s@%s' % (u,p,s)

def role_archive_root(role, vars):
    try:
        if vars['backup_roles'][role]['snapshot'] == True:
            return vars[role + '_home_backup_version']
        else:
            return vars[role + '_home_version']
    except KeyError:
        return vars[role + '_home_version']


def role_home_db_folder(role, vars):
    try:
      if vars['backup_roles'][role]['snapshot'] == True:
          return os.path.join(os.path.sep, vars[role + '_home_backup_version'],
            vars['backup_rsnapshot_backup_db_folder'])
      else:
          return os.path.join(os.path.sep, vars[role + '_home_version'],
            vars['backup_rsnapshot_backup_db_folder'])
    except KeyError:
          return os.path.join(os.path.sep, vars[role + '_home_version'],
            vars['backup_rsnapshot_backup_db_folder'])

class FilterModule(object):
    """backup filters."""

    def filters(self):
        return {
            'backup_name_underscored': backup_name_underscored,
            'expdp_options': expdp_options,
            'impdp_options': impdp_options,
            'role_script_path': role_script_path,
            'role_dump_dir': role_dump_dir,
            'role_dump_dir_remote': role_dump_dir_remote,
            'role_dump_dir_name': role_dump_dir_name,
            'role_scn_file': role_scn_file,
            'role_schema_file': role_schema_file,
            'role_log_file_path': role_log_file_path,
            'role_log_file_name': role_log_file_name,
            'role_rsnapshot_config_path': role_rsnapshot_config_path,
            'role_rsnapshot_root': role_rsnapshot_root,
            'role_archive_root': role_archive_root,
            'role_home_db_folder': role_home_db_folder,
            'role_oracle_connect': role_oracle_connect,
            'role_dump_file': role_dump_file,
            'role_dump_log_file': role_dump_log_file,
            'role_schema_name': role_schema_name,
            'role_tns_name': role_tns_name,
            'role_dump_dir_tar': role_dump_dir_tar,
            'role_dump_dir_tar_tmp': role_dump_dir_tar_tmp
        }
