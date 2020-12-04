
# PostgreSQL

Ansible rol for:

1. Creating an admin PostgreSQL user `ansible` for remote management of database users and databases.
2. Generic tasks for creation of database users, databases for products such as Jira, Confluence etc.

An example can be found in __jira__ role e.g.

    + include: ../../postgresql/tasks/database.yml 
      vars:
          lcm_role_upgrade: "jira"
      when: jira_database_custom == False


