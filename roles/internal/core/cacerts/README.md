# Ansible Role: cacerts

An Ansible Role that manages Java keystores using [java_cert](https://docs.ansible.com/ansible/latest/modules/java_cert_module.html) module.

This role can also be used to manage OS keystore.

## Add roles

Add keystore info using `cacerts_roles_supported` and `cacerts_roles`. For example for Jira. Add it as a supported role with

    cacerts_roles_supported: ['jira']

Add Jira keystore info

    cacerts_roles:
      jira:
        keystore_path: "{{ jira_home_version_app|default(omit) }}/jre/lib/security/cacerts"
        keystore_pass: "{{ cacerts_keystore_pass }}"
        notify: jira-systemctl-restart
        executable: "{{ jira_home_version_app|default(omit) }}/jre/bin/keytool"


## Add certificates

Configure certificates, CA bundles to import using `cacerts_import_certs_urls` for example:

    cacerts_import_certs_urls:
      - name: mycompanybundle
        url: https://example.com/SectigoRSADVBundle.crt

## Add trusted sites

Configure sites that should be trusted using `cacerts_trusted_sites` for example

Note: this does not seem to work. Bug in `java_cert` module.

    cacerts_trusted_sites:
      - url: google.com
        port: 443

## Add OS certs

Configure array of URLS to download into OS keystore:

    cacerts_os_ca_pem_urls:
      - https://example.com/SectigoRSADVBundle.crt