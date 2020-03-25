# BigBlueButton

Ansible role for a bigbluebutton installation (following the documentation on http://docs.bigbluebutton.org/install/install.html)

## Variables to specify
| Variable Name | Function | Default value | Comment |
| ------------- | -------- | ------------- | ------- |
| `bbb_hostname` | Hostname for this BigBlueButton instance _(required)_ | |
| `bbb_letsencrypt_enable` | Enable letsencrypt/HTTPS | `yes` |
| `bbb_letsencrypt_email` | E-mail for use with letsencrypt |  |
| `bbb_enable_coturn` | enable installation of the TURN-server | `yes` |
| `bbb_turn_server` | the adress for the TURN-Server to use | `{{ bbb_hostname }}`
| `bbb_turn_secret` | Secret for the TURN-Server  _(required)_ | | can be generated woth `openssl rand -hex 16`
| `bbb_enable_greenlight` | enable installation of the greenlight client | `yes` |
| `bbb_enable_api_demos` | enable installation of the api demos | `no` |
| `bbb_nodejs_version` | version of nodejs to be installed | `8.x` |
| `bbb_system_locale` | the system locale to use | `en_US.UTF-8` |
