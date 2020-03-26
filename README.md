# TPELCM Ansible Repository

This purpose of this repository is to automate Life Cycle Management (LCM) procedures using Ansible.

Currently the following products are supported:

- [SonarQube](roles/internal/sonarqube)
- [Nexus](roles/internal/nexus)

The repository also includes plays / roles for test and development purposes. See for example 
- [opendj.yml](plays/opendj.yml) play and [opendj/](roles/internal/opendj) role. This creates a simple LDAP server based on OpenDJ.
- [env.yml](plays/env.yml) play and [env](roles/internal/env) role. This role was added to configure an environment for a [PetClinic](https://github.com/spring-projects/spring-petclinic) example project. At this point it creates for example LDAP groups and accounts.

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

Git clone this repository for example to `~/ansible`. Create a file `~/ansible/vpass` with content `secret` in root of the repository directory. This is used by Ansible vault for encrypting and decrypting [secrets](SECRETS.md). 

Cd into the __vagrant__ directory and provision the proxy node

    vagrant up proxy 

Vagrant up will fail at some point because the __group_vars__ directory is not found by Vagrant. Vagrant uses a dynamic inventory file `.vagrant/provisioners/ansible/inventory` and Ansible searches the location of this file for the __group_vars__ and __host_vars__.

Create two links for __group_vars__ and __host_vars__ directory in the directory where Vagrant created the dynamic inventory file . There is a rake task you can use to create these two links

    rake vagrant:group_host_vars 

Creating the proxy first and correctly is a critical first step because all outbound internet traffic goes through this proxy. If there are issues in provision phase, you can disable the proxy server temporarily by disabling the proxy configuration in [proxy.yml](group_vars/all/proxy.yml).

    ---
    proxy_port: 3128
    proxy_host: '1.1.1.3'
    proxy_no_proxy: 'nip.io' # comma separated list


### Provision

After creating the links you can start provisioning one ore more services:

| Service   | Link      | Accounts|
|----------|-------------|-------------|
| SonarQube |[https://sh.1.1.1.3.nip.io/sonarqube/](https://sh.1.1.1.3.nip.io/sonarqube/)| default `admin` with pw `admin` or `akaufman` |
| Nexus     |[https://sh.1.1.1.3.nip.io/nexus/](https://sh.1.1.1.3.nip.io/nexus/)   | `admin` with pw `secret` or `akaufman`|
<<<<<<< HEAD
| Jenkins   |[https://sh.1.1.1.3.nip.io/jenkins/](https://sh.1.1.1.3.nip.io/jenkins/)| `admin` with pw `supersecret` |
| Dimension |[https://sh.1.1.1.3.nip.io/jenkins/](https://sh.1.1.1.3.nip.io/dimension/)| `admin` with pw `supersecret` |
=======
| Jenkins | [https://sh.1.1.1.3.nip.io/jenkins/](https://sh.1.1.1.3.nip.io/jenkins/)| `admin` with pw `supersecret` |
| Bitbucket | [https://sh.1.1.1.3.nip.io/bitbucket/](https://sh.1.1.1.3.nip.io/bitbucket/)| `admin` with pw `secret` |
>>>>>>> 8088f1648252cce884838729c770bbd83f4838bb

LDAP accounts
| Account   | Password | Role |
|----------|-------------|-------------|
| `akaufman`   | `secrets` | admin |

Accounts en groups are in [host_vars/env.yml](host_vars/env.yml).

#### Proxy & Env

The __env__ node is currently only used to create LDAP groups, accounts on the __proxy__. After __env__ provision it can be destroyed.

    vagrant up proxy env
    vagrant destroy env

#### SonarQube ( optional )

    vagrant provision postgresql sonarqube

#### Nexus ( optional )

    vagrant provision nexus

#### Jenkins ( optional )

    vagrant provision jenkins

#### Bitbucket ( optional )

    vagrant provision bitbucket

### LDAP

The __proxy__ node includes a simple LDAP server based on OpenDJ. If you want to connect to the LDAP directory using a tool like [Apache Directory Studio](https://directory.apache.org/studio/) use for example ldap://1.1.1.3:389 and `cn=admin` with password `secret`.

## License

MIT License.
