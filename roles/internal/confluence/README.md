# Ansible Role: Confluence	

An Ansible Role that installs [Confluence](https://www.atlassian.com/software/confluence/) on RedHat/CentOS.

## Requirements

## Role Variables

## Dependencies

__lcm__ 

## Response file documentation


# Response file documentation 
* app.confHome	
	- This is the path to your target local home directory.

* app.install.service$Boolean	(true|false)
    - Determines whether Confluence should be installed as a service.

* portChoice	(custom|default)
    - Determines whether Confluence should be installed with default ports.

* httpPort$Long	
	- If portChoice is custom, this sets the HTTP connector port in Tomcat.

* rmiPort$Long	
	- If portChoice is custom, this sets the Tomcat server port.

* launch.application$Boolean	(true|false)
    - Determines whether the installer should start Confluence once installation is complete

* sys.adminRights$Boolean=true	
    - Indicates whether the user running the installer has admin privileges on the machine.

* sys.confirmedUpdateInstallationString (true|false)
    - Set this to false for a fresh unattended installation. Set to true to perform an unattended upgrade.
    - Always back up your existing site before attempting to upgrade.

* sys.installationDir	path to install directory	
    - This is the path to your target installation directory for a new install, or existing installation directory to be upgraded.

* sys.languageId	
	- Default application language.

* example of response varfile created af the installation of 6.14.3
```
# install4j response file for Confluence 6.14.3
app.confHome=/opt/confluence/confluence-6.14.3/home
app.install.service$Boolean=false
existingInstallationDir=/opt/confluence/confluence-6.14.3/home
httpPort$Long=8090
launch.application$Boolean=false
portChoice=custom
rmiPort$Long=8000
sys.adminRights$Boolean=true
sys.confirmedUpdateInstallationString=false
sys.installationDir=/opt/confluence/confluence-6.14.3/app
sys.languageId=en

```

* [atlassian doc](https://confluence.atlassian.com/doc/unattended-installation-838416261.html?_ga=2.204823440.183061960.1588272359-998721950.1513692947)