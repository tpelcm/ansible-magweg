
Role that intends to supplement external role [geerlingguy.jenkins](../../external/geerlingguy.jenkins).

Currently it does the following in this repository:
1. Sets Jenkins system message to: "This system message is managed by Ansible, all changes will be lost."
2. Configures some JDK auto-installers.

This shows two ways to execute Groovy scripts using `jenkins_script`:
1. Simple scripts are stored in `scripts` directory and are provided simple key-value pair arguments. 
2. More complicated scripts are created on the controle node using a `template` so that Jinja templating language can be used. As an example JDK auto-installers are configured using this approach. These are configured in `group_vars/jenkins/auto_installers.yml`.
