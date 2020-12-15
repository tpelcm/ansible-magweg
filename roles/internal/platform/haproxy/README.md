# Ansible Role: HAProxy

Installs HAProxy on RedHat/CentOS 7 Linux servers.

**Note**: This role installs HAProxy _from source_ so you can install any version you want and you are not limited to the old and obsolete versions that are available for CentOS 6 and 7.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    haproxy_socket: /var/lib/haproxy/stats

The socket through which HAProxy can communicate (for admin purposes or statistics). To disable/remove this directive, set `haproxy_socket: ''` (an empty string).

    haproxy_chroot: /var/lib/haproxy

The jail directory where chroot() will be performed before dropping privileges. To disable/remove this directive, set `haproxy_chroot: ''` (an empty string). Only change this if you know what you're doing!

    haproxy_user: haproxy
    haproxy_group: haproxy

The user and group under which HAProxy should run. Only change this if you know what you're doing!

Use `haproxy_frontends` to configure frontends and `haproxy_backends` to configure the backends. See example below.

    haproxy_global_vars:
      - 'ssl-default-bind-ciphers ABCD+KLMJ:...'
      - 'ssl-default-bind-options no-sslv3'

A list of extra global variables to add to the global configuration section inside `haproxy.cfg`.

## Dependencies

None.

## Example configuration

The example config below configures the following
1. Redirect all traffic from 80 to 443.
2. SSL passthrough of all traffic on 443 to reverse proxy 1.1.1.2:443.
3. SSH passthrough of traffic on 7999 to Bitbucket SSH.

```yaml
---
haproxy_frontends:
  http:
    bind: "0.0.0.0:80 name 0.0.0.0:80"
    mode: "http"
    log: "global"
    option: "http-keep-alive"
    timeout client: "30000"
    default_backend: "redirect_http_https"
  https:
    bind: "*:443"
    mode: "tcp"
    default_backend: "rproxies"
  bitbucket:
    bind: "*:7999"
    mode: "tcp"
    default_backend: "bitbucket"

haproxy_backends:
  redirect_http_https:
    mode: "http"
    timeout connect: "30000"
    timeout server: "30000"
    retries: "3"
    option: "httpchk"
    redirect scheme: "https code 301"
  rproxies:
    mode: "tcp"
    server proxy: "1.1.1.2:443"
  bitbucket:
    mode: "tcp"
    server proxy: "1.1.1.4:7999"
```

## License

MIT / BSD

## Author Information

This role was created in 2020 by [Onno van der Straaten ](https://www.onknows.com/).
