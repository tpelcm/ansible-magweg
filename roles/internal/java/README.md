# Ansible Role: AdoptOpenJDK

A simple Ansible Role that installs [AdoptOpenJDK](https://adoptopenjdk.net/) on Linux servers. Java home will be made available as fact `adoptopenjdk_java_home`. 

## Requirements

## Role Variables

Available variables are listed below, along with default values:

Version to install 

    adoptopenjdk:
      version: "jdk8u222b10_oj9"

Vars for available versions to install

    ---
    adoptopenjdk:
      versions:
        jdk8u222b10_oj9:
          url: https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u222-b10_openj9-0.15.1/OpenJDK8U-jdk_x64_linux_openj9_8u222b10_openj9-0.15.1.tar.gz
          checksum: 20cff719c6de43f8bb58c7f59e251da7c1fa2207897c9a4768c8c669716dc819

To add `JAVA_HOME` to `/etc/environment` use `adoptopenjdk_java_home_etc_environment: true`. Default is false.

## Dependencies

## Example Playbook

## License

MIT / BSD

## Author Information

This role was created in 2019 by [Onno van der Straaten](https://www.onknows.com/).
