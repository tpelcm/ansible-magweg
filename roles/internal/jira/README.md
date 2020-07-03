# Jira

Installs [Atlassian Jira](https://www.atlassian.com/software/jira/) on RedHat/CentOS.

Default Jira will be configured to be used via a reverse proxy server. So after the first / fresh provision navigate to https://sh.1.1.1.3.nip.io/jira to complete the setup.

## Requirements

## Role Variables

`jira_manual_upgrade` 
To perform an upgrade manually set to `yes` and provision. The role will prepare upgrade but not run the installer and start services. The installer will be downloaded to `/opt/jira` and a response file '/opt/jira/reponse.varfile'.

    /opt/jira/atlassian-jira-software-8.5.5-x64.bin -q -varfile /opt/jira/response.varfile

Note: the application directory `/opt/jira/jira/app` is not configured when performing a manual upgrade. This is because the installer creates the application directory. To configure the application directory just run the jira play again.

## Dependencies

* [lcm](../lcm)

## Related

* [backup](../backup) 




