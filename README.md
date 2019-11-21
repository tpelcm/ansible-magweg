# TPELCM Ansible Repository

This purpose of this repository is to automate Life Cycle Management (LCM) procedures using Ansible. 

Currently the following products are supported:
- [SonarQube](roles/internal/sonarqube)
- [Nexus](roles/internal/nexus)

The repository also includes plays / roles for test and development purposes. See for example 
- [opendj.yml](play/opendj.yml) play and [opendj/](roles/internal/opendj) role. This creates a simple LDAP server based on OpenDJ.
- [env.yml](play/env.yml) play and [env](roles/internal/env) role. This role was added to configure an environment for a [PetClinic](https://github.com/spring-projects/spring-petclinic) example project. At this point it creates for example LDAP groups and accounts.

This repository is created and maintained as a monolithic repository. External roles from Galaxy and GitHub are copied into this repository. Aside from that it tries to follow [Ansible Best Practices](ANSIBLEBESTPRACTICES.md) as much as possible.

## Getting Started

Install Ansible, Vagrant, VirtualBox on Ubuntu 18.04 machine.

### Ansible

Add the Ansible repository and install Ansible.

    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get install ansible

This repository has been used with Python 2.7.15 and Ansible 2.8.3.

### Vagrant

    sudo wget https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
    sudo dpkg -i vagrant_2.2.6_x86_64.deb

### VirtualBox

    sudo apt-get install virtualbox

### Setup project directory

Git clone this repository for example to `~/ansible`. Create a file `~/ansible/vpass` met content `secret` in de root of the repository directory. This is / can be used by Ansible vault for encrypting and decrypting secrets.

Cd into the __vagrant__ directory and provision the proxy node

    vagrant up proxy 

Vagrant up will fail at some point because the __group_vars__ directory is not found by Vagrant. Vagrant uses a dynamic inventory file `.vagrant/provisioners/ansible/inventory` and Ansible searches the location of this file for the __group_vars__ and __host_vars__.

Create two links for __group_vars__ and __host_vars__ directory in the directory where Vagrant created the dynamic inventory file . There is a rake task you can use to create these two links

    rake vagrant:group_host_vars 

### Provision

After creating the links you can setup SonarQube and Nexus

    vagrant up proxy postgresql sonarqube nexus env
    vagrant provision proxy postgresql sonarqube nexus env

If provision is succesful you can access SonarQube and Nexus using 
https://sh.1.1.1.3.nip.io/sonarqube/ and https://sh.1.1.1.3.nip.io/nexus/

You should be able to logon to SonarQube using for example account `akaufman` with password `supersecure`. Accounts en groups are in [host_vars/env.yml](host_vars/env.yml).

## License
MIT License.
