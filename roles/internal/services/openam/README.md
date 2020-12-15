Ansible OpenAM Role
=========

This role installs OpenAM 14.4.2 and Apache Tomcat on your target host.

Note: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Requirements
------------

Ansible

Role Variables
--------------



Dependencies
------------

- wget
- net-tools
- java-1.8.0-openjdk.x86_64
- unzip

This packets will automatically install on task preinstall.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      roles:
         - role: zemond.ansible_role_openam

Tomcat start on http://domain:8080
OpenAm available on http://domain:8080/openam

License
-------

------------------
