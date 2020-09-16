
# Ansible Role: oracle

An Ansible Role that can creates an Oracle 12.2 Database Enterprise Edition server using a [Docker image](https://hub.docker.com/_/oracle-database-enterprise-edition). Pull of Oracle database image requires 1) checkout and 2) login. Go to [hub.docker.com](https://hub.docker.com/_/oracle-database-enterprise-edition) and proceed to checkout. 

## Configure hub.docker.com credentials

After checkout you can add your credentials for example to file `local_stuff.yml` ( so it won't end up in Git ).

    oracle:
      docker_login:
        user_name: <hub.docker.com account>
        password: <personal access token or password - use token!>

If you run this _oracle_ role without 1) providing credentials and 2) performing checkout, provision will fail with something similar to 

    TASK [oracle : docker_image] ***************************************************
    fatal: [oracle]: FAILED! => {"changed": false, "msg": "Error pulling image store/oracle/database-enterprise:12.2.0.1 - 404 Client Error:
    Not Found (\"{\"message\":\"pull access denied for store/oracle/database-enterprise, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\"}\")"}

## Connect as sysdba

To connect to the database as `sysdba` for example

```bash
docker exec -it oracle bash # enter container
sqlplus "/as sysdba"
```

## Create a database

To create pluggable database with an admin account, you can configure for example something like

    oracle_pluggable_databases:
      - name: JIRA
        admin: jira_dba
        password: supersecret

After provision you can connect to this database for example as follows:

    vagrant ssh oracle
    sqlplus jira-dba/supersecret@jira

