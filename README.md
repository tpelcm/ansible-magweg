# TPELCM Ansible Repository

This purpose of this repository is to automate Life Cycle Management (LCM) procedures using Ansible. 

Currently one product is automated:
- [SonarQube](../roles/internal/sonarqube)

This repository is created and maintained as a monolithic repository. External roles from Galaxy and GitHub are copied into this repository. Aside from that it tries to follow [Ansible Best Practices](ANSIBLEBESTPRACTICES.md) as much as possible.

## Getting Started

Install Ansible, Vagrant and VirtualBox. Git clone this repository. Cd into the __vagrant__ directory and run `vagrant up proxy`. Ignore failures.

With the first machine running create two links for __group_vars__ and __host_vars__ directory in the directory where Vagrant created the dynamic inventory file `.vagrant/provisioners/ansible/inventory`.

Vagrant uses a dynamic inventory file and Ansible searches the location of this file for the __group_vars__ and __host_vars__.

## License
MIT License.
