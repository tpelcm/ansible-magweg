# LCM

An Ansible Role that helps with automating specific LCM operations. 

Downgrade is typically not an operation that products support so a provision that requests a earlier version than the one currently installed, performs a __install__ operation.

This role will create Ansible facts for the type of operation that is requested.

| Operation         | Conditions           | 
| ----------------- |:-------------:|
| install           | The desired version is not installed yet. There is not current version or current version is a higher version (downgrade not supported). |
| update            | The desired version is installed and current.      | 
| upgrade           | The desired version is a higher version than the current version.      |   
| rollback          | The desired and current version are installed and the desired version is lower.      |
| rollforward       | The desired and current version are installed and the desired version is higher.      |
| prepare-upgrade       | The desired and current version are equal and we are preparing for upgrade to `bitbucket_version_prepare` |

In Ansible console logging you should see LCM info for roles that use / support this role. The example below shows LCM info for a Jira upgrade.

    TASK [lcm : LCM info facts] ****************************************************
    ok: [jira] => (item=jira) => {
        "msg": [
            "jira_lcm['operation']: upgrade", 
            "jira_lcm['version-file']: /opt/jira/jira-8.5.5/VERSION", 
            "jira_lcm['operation-description']: Upgrade 7.12.1 to 8.5.5", 
            "jira_version: 8.5.5", 
            "jira_home: /opt/jira", 
            "jira_database_name_version: jira_8_5_5", 
            "jira_database_template: jira_7_12_1", 
            "jira_home_version: /opt/jira/jira-8.5.5", 
            "jira_home_version_current: /opt/jira/jira-7.12.1", 
            "jira_home_version_home: /opt/jira/jira-8.5.5/home", 
            "jira_home_version_home_current: /opt/jira/jira-7.12.1/home", 
            "jira_home_version_app: /opt/jira/jira-8.5.5/app", 
            "jira_home_version_app_current: /opt/jira/jira-7.12.1/app", 
            "jira_home_link: /opt/jira/jira", 
            "jira_home_link_home: /opt/jira/jira/home", 
            "jira_home_link_app: /opt/jira/jira/app"
        ]
    }

To clarify how this role helps you automate LCM operations, consider the following snippet from the bitbucket role.

    + name: stop for upgrade, rollback or rollfoward
      service: name=bitbucket state=stopped
      when: bitbucket_lcm['operation'] in ['upgrade','rollback','rollforward'] 

This snippet shuts down the bitbucket service when we are performing for example an upgrade.

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
