# Ansible Role: Monit

An Ansible Role the provides simple monitoring using Monit. This is used to perform simple disk space monitoring of data and system volumes.

This role can also be used to monitor log files for specific messages using POSIX regular expressions. The example below shows how we to monitor for [Editor fails to load in Confluence 6.x and later due to 'Could not initialize class org.xerial.snappy.Snappy' error](https://confluence.atlassian.com/confkb/editor-fails-to-load-in-confluence-6-x-due-to-could-not-initialize-class-org-xerial-snappy-snappy-error-859462192.html)

    monit_roles_supported: ['confluence']

    monit_roles:
      confluence:
        logs:
          synchrony:
            path: "/opt/confluence/confluence/home/logs/atlassian-synchrony.log"
            match: "^.*?java.lang.UnsatisfiedLinkError:.*?failed to map segment from shared object.*?$" # 


## Role Variables

This role buils on __lvm__ role. It will automatically add monitoring to volumes managed by the __lvm__role.

Using var `monit_mounts` you can add monitoring to other volumes. To monitor for example `/` and `/vagrant` you could add.

    monit_mounts:
      - name: root
        path: /
      - name: vagrant
        path: /vagrant
