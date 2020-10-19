"""java filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import json, os

# Return folder name for JDK 
# e.g. jdk8_222b10_oj9
def java_folder(version):
    return version.lower()

# Return Java home 
# e.g. /usr/lib/jvm/jdk8_222b10_oj9
def java_home(version):
    return os.path.join(os.path.sep,
        '/usr/lib/jvm',
        java_folder(version))

def java_keystore(version):
    return os.path.join(os.path.sep, 
        java_home(version),
        'jre/lib/security/cacerts')

def java_keytool(version):
    return os.path.join(os.path.sep, 
        java_home(version),
        'jre/bin/keytool')

class FilterModule(object):
    """java filters."""

    def filters(self):
        return {
            'java_folder': java_folder,
            'java_home': java_home,
            'java_keystore': java_keystore,
            'java_keytool': java_keytool,
        }
