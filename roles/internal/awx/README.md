
# Ansible Role: AWX

An Ansible Role that installs [AWX](https://github.com/ansible/awx/) on RedHat/CentOS. This "internal" role is based on the [local docker](https://github.com/ansible/awx/tree/devel/installer/roles/local_docker) installer option. 

Note:
The local docker option of AWX is not 100% reliable. This is result of a bug in the [local docker](https://github.com/ansible/awx/tree/devel/installer/roles/local_docker) installer option which can cause AWX database migrations to fail. AWX database migrations started by container **awx_task** will run too soon - before the **awx_postgres** has completely finished setup. `docker logs -f awx_task` will show a lot of database errors in that case. 

To fix this stop **awx_web** and restart **awx_task**. The Docker logs should show **awx_task** migrations running and completing after which logs no longer show error messages. Then start **awx_web**.

## Requirements

## Role Variables

## Dependencies

## Troubleshooting

If setup is consistently failing, provision **awx** without starting containers:

    awx_compose_start_containers: false

Then create containers without starting.

    cd /opt/awx/compose
    docker-compose -f docker-compose.yml up --no-start

Start **awx_postgres** **awx_redis** and **awx_memcached** and check for errors.

    docker start awx_postgres awx_redis awx_memcached
    docker logs -f awx_postgres

Start **awx_task** check logs for errors. 

    docker start awx_task && docker logs -f awx_task

Start **awx_web**

    docker start awx_web

