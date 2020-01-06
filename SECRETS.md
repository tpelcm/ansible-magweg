# Secrets

Secrets in this repository are encrypted using [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html).

You need to create a file `~/ansible/vpass` met content `secret` in de root of the repository directory to be able to descrypt the secrets file [secrets.yml](group_vars/all/secrets.yml) in an Ansible run.

To see or edit the contents of this secrets file [secrets.yml](group_vars/all/secrets.yml) 

    env EDITOR=nano ansible-vault edit group_vars/all/secrets.yml --vault-password-file vpass

This example uses two passwords `secret` and `supersecret` for normal and admin type accounts. For example 

    sonarqube_database_password: secret
    sonarqube_database_admin_password: supersecret