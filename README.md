BigBlueButton
=========

Ansible role for a bigbluebutton installation (following the documentation on http://docs.bigbluebutton.org/install/install.html)


Role Variables
--------------

| Variable Name | Function | Default value | Comment |
| ------------- | -------- | ------------- | ------- |
| `bbb_hostname` | Hostname for this BigBlueButton instance _(required)_ | {{ ansible_fqdn_hostname }} |
| `bbb_letsencrypt_enable` | Enable letsencrypt/HTTPS | `yes` |
| `bbb_letsencrypt_email` | E-mail for use with letsencrypt _(required when using LE)_|  |
| `bbb_coturn_enable` | enable installation of the TURN-server | `yes` |
| `bbb_turn_enable` | enable the use uf TURN in general | `yes` |
| `bbb_turn_server` | the adress for the TURN-Server to use | `{{ bbb_hostname }}` | has to be a fully qualified domain name
| `bbb_turn_secret` | Secret for the TURN-Server  _(required)_ | | can be generated with `openssl rand -hex 16`
| `bbb_greenlight_enable` | enable installation of the greenlight client | `yes` |
| `bbb_greenlight_secret` | Secret for greenlight _(required when using greenlight)_ |  | can be generated with `openssl rand -hex 64`
| `bbb_greenlight_db_password` | Password for greenlight's database  _(required when using greenlight)_ | | can be generated with `openssl rand -hex 16`
| `bbb_api_demos_enable` | enable installation of the api demos | `no` |
| `bbb_nodejs_version` | version of nodejs to be installed | `8.x` |
| `bbb_system_locale` | the system locale to use | `en_US.UTF-8` |

Dependencies
------------

- geerlingguy.nodejs

Example Playbook
----------------

This is an example, of how to use this role. Warning: the value of bbb_turn_secret should be changed!

    - hosts: servers
      roles:
         - { role: n0emis.bigbluebutton, bbb_turn_secret: 'ee8d093109a9b273eb69cce6c965e1d3' }

License
-------

MIT
