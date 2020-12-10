"""tomcat filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import json, os

# Return path to properties folder
# e.g. /etc/tomcat/myapp.properties
def tomcat_properties_file_path(app,properties_folder):
    return '/'.join([properties_folder, app + '.properties'])

def tomcat_domain(ansible_fqdn):
    return ansible_fqdn.split('.', 1)[1]

class FilterModule(object):
    """backup filters."""

    def filters(self):
        return {
            'tomcat_properties_file_path': tomcat_properties_file_path,
            'tomcat_domain': tomcat_domain
        }
