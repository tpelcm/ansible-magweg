# TPELCM Ansible Repository

This purpose of this repository is to automate Life Cycle Management (LCM) procedures using Ansible.

Currently the following products are supported:

- [SonarQube](roles/internal/sonarqube)
- [Nexus](roles/internal/nexus)

This repository is created and maintained as a monolithic repository. External roles from Galaxy and GitHub are copied into this repository. Aside from that it tries to follow [Ansible Best Practices](ANSIBLEBESTPRACTICES.md) as much as possible.

## Getting Started

Install Ansible, Vagrant, VirtualBox on Ubuntu 18.04 machine.
[nip.io](https://nip.io) is used to DNS entries to IP addresses in the development environment.

### Ansible

Add the Ansible repository and install [Ansible](https://ansible.com).

    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get install ansible

This repository has been used with Python 2.7.15 and Ansible 2.8.3.

### Vagrant

    sudo wget https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
    sudo dpkg -i vagrant_2.2.6_x86_64.deb

### VirtualBox

    sudo apt-get install virtualbox

### Setup project directory

Git clone this repository for example to `~/ansible`.

Create a file `~/ansible/vpass` with for example the word `secret` in the root of the repository directory. This is / can be used by Ansible vault for encrypting and decrypting secrets. The secret word can be chosen by the user, but should be there.

Cd into the __vagrant__ directory and run `vagrant up proxy`.

Vagrant up will fail at some point because the __group_vars__ directory is not found by Vagrant. Vagrant uses a dynamic inventory file `.vagrant/provisioners/ansible/inventory` and Ansible searches the location of this file for the __group_vars__ and __host_vars__.

Create two links for __group_vars__ and __host_vars__ directory in the directory where Vagrant created the dynamic inventory file . There is a rake task you can use to create these two links

    rake vagrant:group_host_vars 

### Provision

After creating the links you can setup SonarQube and Nexus

    vagrant up proxy postgresql sonarqube nexus
    vagrant provision proxy postgresql sonarqube nexus

If provision is successful you can access SonarQube and Nexus using 
https://sh.1.1.1.3.nip.io/sonarqube/ and https://sh.1.1.1.3.nip.io/nexus/

## License

MIT License.
