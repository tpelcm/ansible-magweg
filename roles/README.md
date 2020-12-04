
# Roles

External and internal Ansible roles. 

## External roles

External roles originate from Ansible Galaxy or GitHub. External roles should not be changed. They are updated from time to time. 

To update a role e.g. `galaxyproject.postgresql` just remove and then download using `ansible-galaxy install`.

    rm -rf roles/external/galaxyproject.postgresql
    ansible-galaxy install galaxyproject.postgresql --force --no-deps -p roles/external

## Internal roles

Internal roles are part of this open source project. They are categorized in folders to help you navigate them.

1. __Core__. Generic roles that are used by all or some other roles. These roles don't create services / processes on target node but are depedencies e.g. packages required by those packages. Or these roles help with Ansible provisioning for example offers generic Ansible modules, filters etc. 
2. __Platform__. These roles create services / processes on target nodes that are usefull or necessary for __services__. Examples are `reverse-proxy`, `proxy`, `postfix`.
3. __Middleware__. Services such as Tomcat, PostgreSQL etc. 
4. __Services__. The services that make up the essence of this open source project for example Jira, Confluence, Nexus etc.
5. __Test__. Roles intended for development / test only. An example is the role `oracle`. This role creates an Oracle Enterprise Edition database running as a container.
