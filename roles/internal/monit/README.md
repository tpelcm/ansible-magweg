# Ansible Role: Monit

An Ansible Role the provides simple monitoring using Monit. Currently this role performs simple disk space monitoring of data and system volumes

## Role Variables

This role buils on __lvm__ role. It will automatically add monitoring to volumes managed by the __lvm__role.

Using var `monit_mounts` you can add monitoring to other volumes. To monitor for example `/` and `/vagrant` you could add.

    monit_mounts:
      - name: root
        path: /
      - name: vagrant
        path: /vagrant
