
# Ansible Role: AWX

An Ansible Role that installs [AWX](https://github.com/ansible/awx/) on RedHat/CentOS. This "internal" role is based on the [local docker](https://github.com/ansible/awx/tree/devel/installer/roles/local_docker) installer option. 

## Requirements

## Role Variables

## Dependencies

__lcm__ 

awx_compose_start_containers: false

cd /opt/awx/compose
docker-compose -f docker-compose.yml up --no-start

docker start awx_postgres awx_redis awx_memcached
docker start awx_task && docker logs -f awx_task
docker start awx_web