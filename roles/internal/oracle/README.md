
# Ansible Role: oracle

An Ansible Role that can creates an Oracle 12.2 Database Enterprise Edition server using a [Docker image](https://hub.docker.com/_/oracle-database-enterprise-edition). Pull of Oracle database image requires 1) checkout and 2) login. Go to [hub.docker.com](https://hub.docker.com/_/oracle-database-enterprise-edition) and proceed to checkout. 

After checkout you can add your credentials for example to file `local_stuff.yml` ( so it won't end up in Git ).

    oracle:
      docker_login:
        user_name: <hub.docker.com account>
        password: <personal access token or password - use token!>

If you run this _oracle_ role without providing credentials and performing checkout, provision will fail with something similar to 

    TASK [oracle : docker_image] ***************************************************
    fatal: [oracle]: FAILED! => {"changed": false, "msg": "Error pulling image store/oracle/database-enterprise:12.2.0.1 - 404 Client Error:
    Not Found (\"{\"message\":\"pull access denied for store/oracle/database-enterprise, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\"}\")"}

To connect to the database as `sysdba` for example

```bash
docker exec -it oracle bash # enter container
sqlplus "/as sysdba"
```
