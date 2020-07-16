"""backup filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import json

# Return backup name without . or -
# e.g. myapp_0_1_0_daily
def backup_name_underscored(role,vars,schedule = None):
    bmn = '_'.join([role,vars[role+'_version']])
    if schedule is not None:
        bmn = '_'.join([bmn,schedule])
    return bmn.replace('.','_').replace('-','_')

class FilterModule(object):
    """backup filters."""

    def filters(self):
        return {
            'backup_name_underscored': backup_name_underscored
        }
