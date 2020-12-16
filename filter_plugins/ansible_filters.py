"""ansible filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import json, os

# Return a logical name based on inventory file
# e.g. development (from /somepath/development.ini)
def ansible_environment(inv_file):
    bn = os.path.basename(inv_file)
    return bn.split('.',1)[0]

class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'ansible_environment': ansible_environment
        }
