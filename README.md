# TPELCM Ansible Repository

This purpose of this repository is to automate Life Cycle Management (LCM) procedures using Ansible.

<!-- MarkdownTOC -->

- Products
- Getting Started
    - Ansible
    - Vagrant
    - VirtualBox
    - Setup project directory
    - Provision a first service
    - Provision
    - LDAP
- License

<!-- /MarkdownTOC -->

## Products

| Product   | Level | Link |Description | 
|----------|:-----:|---|---|
| [SonarQube](roles/internal/sonarqube)| III | [https://sh.1.1.1.3.nip.io/sonarqube/](https://sh.1.1.1.3.nip.io/sonarqube/) | default `admin` with pw `admin` or `akaufman` |
| [Nexus](roles/internal/nexus)| IV |[https://sh.1.1.1.3.nip.io/nexus/](https://sh.1.1.1.3.nip.io/nexus/) | `admin` with pw `secret` or `akaufman` |
| [Jira](roles/internal/jira)| II |[https://sh.1.1.1.3.nip.io/jira/](https://sh.1.1.1.3.nip.io/jira/) | `admin` with pw `secret`<sup>2</sup>  |
| [Bitbucket](roles/internal/bitbucket)| II | [https://sh.1.1.1.3.nip.io/bitbucket/](https://sh.1.1.1.3.nip.io/bitbucket/) ||
| [Confluence](roles/internal/confluence)| II |[https://sh.1.1.1.3.nip.io/confluence/](https://sh.1.1.1.3.nip.io/confluence/) | `admin` with pw `secret`<sup>2</sup> |
| [Jenkins](roles/internal/jenkins)| I |[https://sh.1.1.1.3.nip.io/jenkins/](https://sh.1.1.1.3.nip.io/jenkins/) | `admin` with pw `supersecret` |
| [Sites](roles/internal/sites)| II | [https://sh.1.1.1.3.nip.io/sites/](https://sh.1.1.1.3.nip.io/sites/) | Host static sites using Apache|
| [AWX](roles/internal/awx)| I | [https://awx.1.1.1.3.nip.io/](https://awx.1.1.1.3.nip.io/)<sup>1</sup> |Open Source Ansible Tower. AWX is very much work in progress, see [README](roles/internal/AWX) for info. Login `admin` with pw `secret`|
| [Guacamole](https://guacamole.apache.org/)| I | [https://sh.1.1.1.3.nip.io/desktop/](https://sh.1.1.1.3.nip.io/desktop/) | Use Docker based desktops in your browser.|

<sup><sub>1. AWX doesn't support changing web context - it needs to run from root.</sub></sup>  
<sup><sub>2. Jira and Confluence setup cannot be automated. You have to use the wizard to setup the database, admin account etc.</sub></sup>

_Capability Levels_

| Level   | Description | 
|----------|-----|
|I - Basic Install|Automated application provisioning and configuration management|
|II - Full Lifecycle|Upgrade,rollback, rollforward, backup, restore|
|III - Insights|Basic monitoring, JMX, etc|
|IV - Project Environment|Managed project creation, access etc|

This repository includes a number of supporting products / components that are typically used in conjunction with the products above:

| Component   |  Purpose | 
|----------|---|
| [reverse-proxy](roles/internal/reverse-proxy)| Reverse proxy server |
| [postgresql](roles/external/geerlingguy.postgresql)| Database for SonarQube, Jira, Bitbucket, Confluence |
| [cacerts](roles/internal/cacerts)| Import certificates, CA bundles in keystores |
| [lcm](roles/internal/lcm)| Support LCM operations install, upgrade, rollback, rollforward|
| [lvm](roles/internal/lvm)| Create, size, manage logical volumes |
| [monit](roles/internal/monit)| Basic monitoring e.g. disk space, CPU, swap etc |
| [postfix](roles/internal/postfix)| Mailrelay |
| [proxy](roles/internal/proxy)| Proxy server based on Squid |
| [swid](roles/internal/swid)| Create SWID tags |

The repository also includes plays / roles for test and development purposes. See for example 
- [opendj.yml](plays/opendj.yml) play and [opendj/](roles/internal/opendj) role. This creates a simple LDAP server based on OpenDJ.
- [env.yml](plays/env.yml) play and [env](roles/internal/env) role. This role was added to configure an environment for a [PetClinic](https://github.com/spring-projects/spring-petclinic) example project. At this point it creates for example LDAP groups and accounts.
- [oracle.yml](plays/oracle.yml) play creates Oracle Database 12c Enterprise Edition based on [Docker container](https://hub.docker.com/_/oracle-database-enterprise-edition). 

This repository is created and maintained as a monolithic repository. External roles from Galaxy and GitHub are copied into this repository. Aside from that it tries to follow [Ansible Best Practices](ANSIBLEBESTPRACTICES.md) as much as possible.

## Getting Started

Install Ansible, Vagrant, VirtualBox on Ubuntu 18.04 machine.
[nip.io](https://nip.io) is used to DNS entries to IP addresses in the development environment.

### Ansible

Add the Ansible repository and install [Ansible](https://ansible.com).

    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get install ansible

This repository has been used with:
1. Ansible 2.8.3 and Python 2.7.15. 
2. Ansible 2.10.3 and Python 3.6.9.  

### Vagrant

    sudo wget https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
    sudo dpkg -i vagrant_2.2.6_x86_64.deb

### VirtualBox

    sudo apt-get install virtualbox

### Setup project directory

Git clone this repository for example to `~/ansible`. 

git clone 
cd ~/ansible

Note: if you run a vagrant command for example `vagrant status` a [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) password stored in the file `~/ansible/vpass` with content `secret` in root of the repository directory. This is used by Ansible vault for encrypting and decrypting [secrets](SECRETS.md). 

### Provision a first service

To get started, create for example the __bitbucket__ service. For this you will also need the __proxy__ node and the __db__ node. So the command becomes 

    vagrant up proxy db bitbucket

The __db__ node contains the PostgreSQL database used by Bitbucket. The __proxy__ has a Apache2 reverse _proxy server_ that will be used to access Bitbucket using self-signed certificates. 

Note: the __proxy__ node also includes a _forward proxy_ server based on Squid. If you want to use this _forward proxy_ you can enable it by removing `proxy_skip` of by setting it to `false` as shown below in proxy.yml](group_vars/all/proxy.yml).

    proxy_skip: false # remove / false to enable forward proxy

If there are issues in provision phase, you can disable the proxy server temporarily by disabling the proxy configuration in [.

### Provision

Additionally create other nodes shown below. At a minimum you will need the `proxy` and `postgresql` node. 

| Node | Service(s)   | Link      | Comments|
|----------|-------------|-------------|-------------|
| __proxy__ | Forward and reverse proxy, NFS server, OpenDJ server, Mailrelay | | |
| __db__ | PostgreSQL server | | |
| __oracle__ | Oracle Database 12c Enterprise Edition | | See [role](roles/internal/oracle-database) for more information.|
| __sonarqube__ | SonarQube server |[https://sh.1.1.1.3.nip.io/sonarqube/](https://sh.1.1.1.3.nip.io/sonarqube/)| default `admin` with pw `admin` or `akaufman` |
| __nexus__ | Nexus     |[https://sh.1.1.1.3.nip.io/nexus/](https://sh.1.1.1.3.nip.io/nexus/)   | `admin` with pw `secret` or `akaufman`|
| __sites__ | Static "dimension" site |[https://sh.1.1.1.3.nip.io/dimension/](https://sh.1.1.1.3.nip.io/dimension/)| `admin` with pw `supersecret` |
| __jenkins__ | Jenkins | [https://sh.1.1.1.3.nip.io/jenkins/](https://sh.1.1.1.3.nip.io/jenkins/)| `admin` with pw `supersecret` |
| __confluence__ | Confluence | [https://sh.1.1.1.3.nip.io/confluence/](https://sh.1.1.1.3.nip.io/confluence/)| `admin` with pw `secret` |
| __jira__ | Jira | [https://sh.1.1.1.3.nip.io/jira/](https://sh.1.1.1.3.nip.io/jira/)| `admin` with pw `secret` |
| __bitbucket__ | Bitbucket | [https://sh.1.1.1.3.nip.io/bitbucket/](https://sh.1.1.1.3.nip.io/bitbucket/)| `admin` with pw `secret` |
| __awx__ | AWX | [https://awx.1.1.1.3.nip.io/](https://awx.1.1.1.3.nip.io/)| |
| __bastion__ | Guacamole | [https://sh.1.1.1.3.nip.io/desktop/](https://sh.1.1.1.3.nip.io/desktop/)|  |

_LDAP accounts_

| Account   | Password | Role |
|----------|-------------|-------------|
| `akaufman`   | `secrets` | admin |

Accounts en groups are in configured in [host_vars/proxy.yml](host_vars/proxy.yml).

To provision a node use standard Vagrant commands see `vagrant --help` for example to provision _SonarQube_ for a first time: 

```bash
    vagrant up proxy db sonarqube
```

To run the Ansible provisioner after nodes have been created using `vagrant up` you use `vagrant provision <node>`. See `vagrant --help` for more information.


### LDAP

The __proxy__ node includes a simple LDAP server based on OpenDJ. If you want to connect to the LDAP directory using a tool like [Apache Directory Studio](https://directory.apache.org/studio/) use for example ldap://1.1.1.3:389 and `cn=admin` with password `secret`.

## License

MIT License.
