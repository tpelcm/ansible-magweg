# Install Cronjob Steps Log

## 'Declare variables"
in `default\main.yml` file, declare
```yaml
bitbucket_scripts: /opt/bitbucket/scripts
bitbucket_mailto: "no-reply@example.com"
```
These variables must be declared explicitely in `<roles>/default/main.yml` for staging and for production


## Create templates 

### create job template - the script to be executed by cron
in `template\jobs` directory
```bash
#!/bin/bash
# {{ ansible_managed }}

{# variables #}
```

### now create the cron.job
in `tasks` folder, create `jobs.yaml`
```yaml
- name: Cron Job installation
  template:
    dest: "/opt/bitbucket/scripts/reposize.sh"
    src: jobs/bitbucket.reposize.sh.j2
    mode: 500

- name: Cron Job scheduling
  cron:
    name: "Displaying top 10 bitbucket reposize usage"
    minute: "0"
    hour: "5"
    day: 1-5
    user: root
    job: '/opt/bitbucket/scripts/reposize.sh | mailx -s "Bitbucket PROD reposizes" {{ bitbucket_mailto }}'
    cron_file: reposize
```

### provision the cron job
in `tasks\main.yml` include, the creation of the `bitbucket_scripts` folder and
include in the `jobs.yml` 
```yaml
- name: scripts directory
  file:
    path: "{{ bitbucket_scripts }}"
    state: directory
    group: "{{ bitbucket_owner }}"
    owner: "{{ bitbucket_group }}"
    
- include: jobs.yml
```

