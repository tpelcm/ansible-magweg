# Ansible Role: SonarQube

An Ansible Role that installs [SonarQube](http://www.sonarqube.org/) on RedHat/CentOS and Debian/Ubuntu Linux servers.

## Requirements

Requires the `unzip` utility to be installed on the server. 

## Role Variables

Available variables are listed below, along with default values:

    workspace: /root

Directory where downloaded files will be temporarily stored.

    sonarqube_download_validate_certs: true

Controls whether to validate certificates when downloading SonarQube.

    sonarqube_download_url: http://dist.sonar.codehaus.org/sonarqube-4.5.4.zip
    sonarqube_version_directory: sonarqube-4.5.4

The URL from which SonarQube will be downloaded, and the resulting directory name (should match the download archive, without the archive extension).

    sonarqube_web_context: ''

The value of `sonar.web.context`. Setting this to something like `/sonar` allows you to set the context where Sonar can be accessed (e.g. `hostname/sonar` instead of `hostname`).

    sonarqube_mysql_username: sonar
    sonarqube_mysql_password: sonar
    
    sonarqube_mysql_host: localhost
    sonarqube_mysql_port: "3306"
    sonarqube_mysql_database: sonar
    
    sonarqube_mysql_allowed_hosts:
      - 127.0.0.1
      - ::1
      - localhost

JDBC settings for a connection to a MySQL database. Defaults presume the database resides on localhost and is only accessible on the SonarQube server itself.

## Dependencies

__lcm__ role sets facts to "version-enable" home directory and database e.g. 

    sonarqube_home_version: /opt/sonarqube/sonarqube_6_7
    sonarqube_database_name_version: sonarqube_6_7

## Example Playbook

    - hosts: all
      roles:
        - geerlingguy.sonar

Using the defaults, you can view the SonarQube home at `http://localhost:9000/` (default System administrator credentials are `admin`/`admin`).

## License

MIT / BSD

## Author Information

This role was created in 2019 by [Onno van der Straaten](https://www.onknows.com/) as a fork of the sonar role created in in 2014 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).  
