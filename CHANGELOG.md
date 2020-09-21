# Ansible TPELCM repository CHANGELOG

This file is used to list changes made in each version of the Ansible TPELCM repository.

## 0.1.0 (2020-09-17)

### Bug

### Improvement

- jira fresh install of 7.12.1, 7.13.14 and 8.5.5
- jira tested upgrade 7.12.1 → 7.13.14 and 7.12.1 → 8.5.5
- jira robust with download first - tested with 8.5.5
- confluence 6.14.3 - added oracle support
- backup & restore - incremental and snapshot backup restore tested with confluence 6.14.3 - Oracle and PostgreSQL 

## 0.1.1 (YYYY-MM-DD)

### Bug

- jira bug jira_database_type "TemplateNotFound: ./templates/_env_postgres72.sh.j2" - renamed jira_database_type to jira_database_type_config
- jira bug "Destination directory /etc/backup/hooks/jira does not exist"

### Improvement
