Ansible OpenAM Role
=========

This role installs OpenAM on your target host.

Note: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Requirements
------------

Ansible

Role Variables
--------------



Dependencies
------------

- tomcat

This packets will automatically install on task preinstall.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      roles:
         - role: openam

Tomcat start on http://domain:8080
OpenAm available on http://domain:8080/openam
