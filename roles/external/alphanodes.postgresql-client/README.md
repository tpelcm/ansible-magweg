# Ansible Role: PostgreSQL-Client

Installs PostgreSQL client on Debian and Ubuntu servers.

[![Build Status](https://travis-ci.org/AlphaNodes/ansible-postgresql-client.svg?branch=master)](https://travis-ci.org/AlphaNodes/ansible-postgresql-client)

## Dependencies

  none

## Example Playbook

    - hosts: db-client
      vars:
        postgresql_client_use_repo: yes
      roles:
        - AlphaNodes.postgresql-client

## License

GPL Version 3

## Author Information

This role was created in 2018 by [AlphaNodes](https://alphanodes.com/).
