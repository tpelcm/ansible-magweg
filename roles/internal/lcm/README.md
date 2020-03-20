# Ansible Role: LCM

An Ansible Role that helps with automating specific LCM operations. 

Downgrade is typically not an operation that products support so a provision that requests a earlier version than the one currently installed, performs a __install__ operation.

This role will create Ansible facts regarding the type of operation that is requested for example a variable named `<role>_lcm.operation` will have the operation.

| Operation         | Conditions           | 
| ----------------- |:-------------:|
| install           | The desired version is not installed yet. There is not current version or current version is a higher version (downgrade not supported). |
| update            | The desired version is installed and current.      | 
| upgrade           | The desired version is a higher version than the current version.      |   
| rollback          | The desired and current version are installed and the desired version is lower.      |
| rollforward       | The desired and current version are installed and the desired version is higher.      |

In Ansible console logging you should see LCM info similar to

    TASK [lcm : LCM info] **********************************************************
    ok: [bitbucket] => (item=bitbucket) => {
        "ansible_loop_var": "item", 
        "bitbucket_lcm": {
            "operation": "rollback", 
            "operation-description": "Rollback 7.0.1 to 5.10.1", 
            "version-file": "/opt/bitbucket/bitbucket-5.10.1/VERSION"
        }, 
        "item": "bitbucket"
    }


## Requirements

This role assumes certain naming standards for variables in roles that are using it. Those variables need to use the roll name as prefix.

1. A home variable `<role>_home` e.g. `bitbucket_home`.
2. A version variable `<role>_version` e.g. `bitbucket_version`.
3. A version sequence variable `<role>_versions_sequence` e.g. `bitbucket_versions_sequence: ['5.10.1','7.0.1']`.

__Version file__

To allow this role to do its magic you need to trigger a handler to write a version file at the right time. The right time is the moment where you consider the version installed.

__Without a version file, this role cannot succesfully determine the LCM operation!!__

## Role Variables

To add Ansible LCM facts for your role, just add your role to `lcm_roles` e.g.

    lcm_roles: ['sonarqube', 'nexus', 'bitbucket', 'myapp']

## LCM Operation

If requirements of your role are met and the role is added to `lcm_roles` this Ansible role will determine a LCM operation Ansible fact `<role>_lcm`

## Version file

Take for example the __bitbucket__ role. When the installer has run we consider the version installed, so we notify handler `lcm-version-file`.

    + name: run installer 
      command: "{{ bitbucket_home }}/{{ bitbucket_versions[bitbucket_version]['url']|basename }} -q -varfile {{ bitbucket_home }}/reponse.varfile"
      become: yes
      become_method: sudo
      become_user: "{{ bitbucket_versions[bitbucket_version]['installer_user']|default('root') }}"
      # become_flags: '-s /bin/sh'
      notify:
        + lcm-version-file
        + bitbucket-systemctl-daemon-reload
        + bitbucket-systemctl-restart
      when: bitbucket_lcm['operation'] in ['upgrade','install']
