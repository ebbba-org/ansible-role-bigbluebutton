# BigBlueButton

[![Ansible Deployment Test](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml)
[![Ansible Lint](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml)
[![Release and Changelog Builder](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml)

> Ansible role for a BigBlueButton installation

This role is following the documentation on <https://docs.bigbluebutton.org/administration/install>

Also check [Before you install](https://docs.bigbluebutton.org/administration/install#before-you-install) and [Minimum server requirements](https://docs.bigbluebutton.org/administration/install#minimum-server-requirements) from the official documentation as they also apply here.

---

> [!NOTE]
> PR [#275](https://github.com/ebbba-org/ansible-role-bigbluebutton/pull/275) removed the option of installing Greenlight. Please checkout another project for Greenlight support

> [!NOTE]
> PR [#276](https://github.com/ebbba-org/ansible-role-bigbluebutton/pull/276) removed the option of installing coturn. Please checkout another project for coturn support

---


## Role Variables

> [!WARNING]
>  **WATCH OUT FOR _REQUIRED_ VARIABLES!**
>
> **IF NOT SET THIS ROLE WILL FAIL!**

| Required | Variable Name | Function | Default value | Comment |
| -------- | ------------- | -------- | ------------ | ------- |
| ⚠️ | `bbb_hostname` | Hostname for this BigBlueButton instance | `{{ ansible_fqdn }}` |
| | `bbb_version` | Install specified BigBlueButton version | `focal-250` | For installing specified BigBlueButton version e.g. `bionic-230-2.3.15` |
| | `bbb_state` | Install BigBlueButton to state | `present` | for updating BigBlueButton with this role use `latest` |
| | `bbb_apt_mirror` | apt repo server for BigBlueButton packages | `https://ubuntu.bigbluebutton.org` | other value would be e.g. `https://packages-eu.bigbluebutton.org` |
| | `bbb_letsencrypt_enable` | Enable letsencrypt/HTTPS | `yes` |
| ⚠️ when using letsencrypt| `bbb_letsencrypt_email` | E-mail for use with letsencrypt | | |
| | `bbb_letsencrypt_api` | Set letsencrypt api | `https://acme-v02.api.letsencrypt.org/directory` | Use this variable to change letsencrypt API URL (example: staging API `https://acme-staging-v02.api.letsencrypt.org/directory`) |
| | `bbb_letsencrypt_repo` | The github repo to use for renewal handling - default acme.sh | <https://github.com/acmesh-official/acme.sh.git> | |
| | `bbb_letsencrypt_dir` | The directory to store the acme.sh repo | `/opt/acme` | |
| | `bbb_letsencrypt_version` | Which version to clone | `master` | |
| | `bbb_letsencrypt_keep_updated` | Keep acme.sh updated | `true` | |
| | `bbb_letsencrypt_install_command` | The command to install acme.sh | See defaults/main.yaml | |
| | `bbb_letsencrypt_create_command` | The command to create certificate | See defaults/main.yaml | |
| | `bbb_own_cert` | Custom ssl cert file to deploy (instead of letsencrypt) | | |
| | `bbb_own_key` | Custom ssl private key file to deploy | | |
| | `bbb_nginx_privacy` | only log errors not access | `yes` |
| | `bbb_nginx_listen_https` | nginx: use https | `yes` | This is useful for a reverse proxy configuration where the BBB server is behind a load balancing server like haproxy that does SSL termination |
| | `bbb_nginx_root` | Default nginx www path of BigBlueButton | `/var/www/bigbluebutton-default` | Set the default nginx `www` path of BigBlueButton |
| | `bbb_ssl_cert` | Define the ssl cert location/name | `"/etc/letsencrypt/live/{{ bbb_hostname }}/fullchain.pem"` | |
| | `bbb_ssl_key` | Define the ssl key location/name | `"/etc/letsencrypt/live/{{ bbb_hostname }}/privkey.pem"` | |
| | `bbb_default_welcome_message` | Welcome Message in the client | Welcome to <b>%%CONFNAME%%</b>!<br><br>For help on using BigBlueButton see these (short) <a href="https://bigbluebutton.org/html5"><u>tutorial videos</u></a>.<br><br>To join the audio bridge click the phone button.  Use a headset to avoid causing background noise for others. | Needs to be encoded with `native2ascii -encoding UTF8`! |
| | `bbb_default_welcome_message_footer` | Footer of the welcome message | This server is running <a href="https://docs.bigbluebutton.org/" target="_blank"><u>BigBlueButton</u></a>. | Encoded as the welcome message |
| | `bbb_default_presentation` | Location of default presentation | `"${bigbluebutton.web.serverURL}/{{ bbb_custom_presentation_name \| default('default.pdf') }}"` |
| | `bbb_custom_presentation` | Overwrite the default.pdf | `None` | Location of a custom presentation will be renamed to `default.pdf` if `bbb_custom_presentation_name` is not defined - see [Ansible search paths](https://docs.ansible.com/ansible/latest/user_guide/playbook_pathing.html) for where to place your custom pdf - Example `playbooks/files/default.pdf` |
| | `bbb_custom_presentation_name` | Set a custom presentation name | `None` | Instead of overwriting the `default.pdf` setting the name will add for example the `customer.pdf` |
| | `bbb_use_default_logo` | Determines if a default-logo should be used if api-parameter "logo" is not used | `false` | The (default) logo is displayed at the top left corner. |
| | `bbb_default_logo_url` | Set a URL for the default logo | `${bigbluebutton.web.serverURL}/images/logo.png` | |
| | `bbb_custom_logo` | Overwrite default logo.png | `None` | Location of a custom presentation will be renamed to `logo.png` if `bbb_custom_logo_name` is not defined - see [Ansible search paths](https://docs.ansible.com/ansible/latest/user_guide/playbook_pathing.html) for where to place your custom png - Example `playbooks/files/logo.png` |
| | `bbb_custom_logo_name` | Set a custom logo name | `None` | Instead of overwriting the `logo.png` setting the name will add for example the `custom-logo.png` |
| | `bbb_web_logouturl` | set logout URL | `default` | Instead of using `bigbluebutton.web.serverURL` as default logout page, set another URL or customize logout page e.g. ${bigbluebutton.web.serverURL}/logout.html. API create call with the `logoutURL` parameter overwrite this setting |
| | `bbb_allow_request_without_session` | Enable or disable allow request without session | `false` | Allow requests without JSESSIONID to be handled |
| | `bbb_turn_enable` | enable the use uf TURN in general | `yes` | |
| | `bbb_stun_servers` | a list of STUN-Server to use | `{{ bbb_hostname }}` | an array with key `server` - take a look in defaults/main.yml |
| | `bbb_ice_servers` | a list of RemoteIceCandidate for STUN | `[]` | in array with key `server` |
| | `bbb_ignore_running_meetings` | install even if meetings are running | `no` | current meetings will be terminated |
| | `bbb_turn_servers` | a list of TURN-Server to use | `{}` | take a look in defaults/main.yml |
| | `bbb_mongodb_version` | version of mongodb to be installed | `4.2` | |
| | `bbb_mongodb_tmpfs_size` | tmpfs size for the mongodb | `512m` | |
| | `bbb_disable_recordings` | Disable options in gui to have recordings | `no` | [Recordings are running constantly in background](https://github.com/bigbluebutton/bigbluebutton/issues/9202) which is relevant as privacy relevant user data is stored |
| | `bbb_api_demos_enable` | enable installation of the api demos | `no` | |
| | `bbb_client_log_enable` | enable installation of the nginx-full and config for client logging according to [BBB Customization Docs](https://docs.bigbluebutton.org/admin/customize.html#collect-feedback-from-the-users). See "METEOR" Section below for needed `bbb_meteor` values. | `false` | |
| | `bbb_mute_on_start` | start with muted mic on join | `no` | |
| | `bbb_app_log_level` | set bigbluebutton log level | `DEBUG` | |
| | `bbb_freeswitch_log_level` | set freeswitch log level | `warning` | |
| | `bbb_etherpad_log_level` | set etherpad log level | `INFO` | |
| | `bbb_fsels_akka_log_level` | set the loglevel between freeswitch and bbb-apps | `ERROR` | |
| | `bbb_apps_akka_log_level` | set the loglevel for bbb-apps-akka | `ERROR` | |
| | `bbb_meteor` | overwrite settings in meteor | `{}` | |
| | `bbb_kurento_interfaces` | Specify the listening interfaces for kurento | `{{ [ansible_default_ipv4.interface, 'lo'] }}` | |
| | `bbb_nodejs_version` | version of nodejs to be installed | `18.x` | |
| | `bbb_system_locale` | the system locale to use | `en_US.UTF-8` | |
| | `bbb_secret` | define the shared secret for bbb | `none` | Set this if you want to define the bbb-secret. Otherwise the secret is generated by bbb. Supported characters are `[a-zA-Z0-9]` |
| | `bbb_freeswitch_ipv6` | Enable IPv6 support in FreeSWITCH | `true` | Disable to fix [FreeSWITCH IPv6 error][bbb_freeswitch_ipv6] |
| | `bbb_freeswitch_ip_address` | Set IP address for FreeSWITCH's wss-binding | `{{ ansible_default_ipv4.address }}` | Can be used when port 7443 is already in use on `{{ ansible_default_ipv4.address }}` or in IPv6-only setups. |
| | `bbb_freeswitch_external_ip` | Set stun server for sip and rtp on FreeSWITCH | `stun:{{ (bbb_stun_servers \| first).server }}` | WARNING: the value of the default freeswitch installation is `stun:stun.freeswitch.org` |
| | `bbb_recording_config` | overwrite recording settings | `{}` | See [Enable playback of recordings on iOS](https://docs.bigbluebutton.org/admin/customize.html#enable-playback-of-recordings-on-ios). It works like `bbb_meteor` by merging your custom config with the server config. |
| | `bbb_dialplan_quality` | Set quality of dailplan for FreeSWITCH | `cdquality` | |
| | `bbb_dialplan_energy_level` | Set energy level of dailplan for FreeSWITCH | `100` | only for selected profile `bbb_dialplan_quality` |
| | `bbb_dialplan_comfort_noise` | Set comfort noise of dailplan for FreeSWITCH | `1400` | Allowed values: (0-10000|true), 0 disables comfort-noise, true sets to default (1400), only for selected profile `bbb_dialplan_quality` |
| | `bbb_webhooks_enable` | install bbb-webhooks | `no` | |
| | `bbb_check_for_running_meetings` | Check server and stop playbook in case of running meetings. Attention: Currently the check is done only after Docker and NodeJS Roles have already run. | `true` | |
| | `bbb_monitoring_all_in_one_enable` | deploy [all in one monitoring stack](https://bigbluebutton-exporter.greenstatic.dev/installation/all_in_one_monitoring_stack/) (docker) | `no` |
| | `bbb_monitoring_all_in_one_version` | Deprecated, use `bbb_monitoring_exporter_version` instead | | |
| | `bbb_monitoring_all_in_one_directory` | Directory for the docker compose files | `/root/bbb-monitoring` | |
| | `bbb_monitoring_all_in_one_port` | Internal Port for the monitoring werbservice | `3001` | |
| | `bbb_monitoring_all_in_one_grafana` | Enable(true)/Disable(false) the Grafana container | `true` | |
| | `bbb_monitoring_all_in_one_prometheus` | Enable(true)/Disable(false) the prometheus container | `true` | |
| | `bbb_monitoring_all_in_one_external` | Deprecated, use `bbb_monitoring_external` instead | | Can be reached under `/mon/bbb` and `/mon/node` - requires `htpasswd` and `htpasswd_user` |
| | `bbb_monitoring_all_in_one_htpasswd_user` | Deprecated, use `bbb_monitoring_htpasswd_user` instead | | |
| | `bbb_monitoring_all_in_one_htpasswd` | Deprecated, use `bbb_monitoring_htpasswd` instead | | |
| | `bbb_monitoring_recordings_from_disk` | Collect recordings metrics by querying the disk instead of the API. See [this](https://bigbluebutton-exporter.greenstatic.dev/exporter-user-guide/#optimizations) for details. | `true` |
| | `bbb_monitoring_external` | Enable exposure to nginx | `false` | Can be reached under `/mon/bbb` and `/mon/node` - requires `htpasswd` and `htpasswd_user`. If `bbb_monitoring_systemd_enable` is enabled, no Node Exporter installation process is included |
| ⚠️ when using external monitoring | `bbb_monitoring_htpasswd_user` | The user for the htpasswd | `Undefined` | |
| ⚠️ when using external monitoring | `bbb_monitoring_htpasswd` | The password for the htpasswd | `Undefined` | |
| | `bbb_monitoring_exporter_version` | Version of the BigBlueButton Exporter for docker and systemd | `latest` if docker image is enabled or `HEAD` if systemd is enabled | If `bbb_monitoring_all_in_one_enable` is enabled, the [Docker images tags](https://hub.docker.com/r/greenstatic/bigbluebutton-exporter/tags?page=1&ordering=last_updated) can be used. If `bbb_monitoring_systemd_enable` is enabled, the [Git release tags](https://github.com/greenstatic/bigbluebutton-exporter/releases) can be used. |
| | `bbb_monitoring_systemd_enable` | Deploy monitoring as systemd service (not recommended) | `false` | Works only when `bbb_monitoring_all_in_one_enable` is `false` |
| | `bbb_monitoring_systemd_directory` | Installation directory for git repository | `"/opt/bigbluebutton-exporter"` | |
| | `bbb_monitoring_systemd_port` | Port of bbb-exporter | `9688` | default port 9866 is defined by the exporter [itself](https://github.com/greenstatic/bigbluebutton-exporter/blob/master/bbb-exporter/settings.py#L37) |
| | `bbb_monitoring_systemd_bind_ip` | Port of bbb-exporter | `0.0.0.0` | default bind IP 0.0.0.0 is defined by the exporter [itself](https://github.com/greenstatic/bigbluebutton-exporter/blob/master/bbb-exporter/settings.py#L38) |
| | `bbb_dialin_enabled` | enable phone dial-in, will also remove any previous dial-in configuration if set to `false`  | `false` | |
| | `bbb_dialin_provider_proxy` | IP or Domain of your SIP provider, also known as registrar | `sip.example.net` | |
| | `bbb_dialin_provider_username` | Username for authentication on the SIP-server | `provider-account` | |
| | `bbb_dialin_provider_password` | Password for authentication on the SIP-server | `provider-password` | |
| | `bbb_dialin_provider_extension` | Extension of your SIP account | `6135551234` | |
| | `bbb_dialin_default_number` | Number to present to users for dial-in. Enable `bbb_dialin_overwrite_footer` or use `%%DIALNUM%%` and `%%CONFNUM%%` in you footer (see `bbb_default_welcome_message_footer`) | `6135551234` | |
| | `bbb_dialin_mask_caller` | Mask caller-number in the BBB web-interface for privacy reasons (`01711233121` → `xxx-xxx-3121`) | |
| | `bbb_dialin_default_play_and_get_digits` | Phone dialin-pin entry voice dialog | `5 7 3 10000 # conference/conf-pin.wav ivr/ivr-that_was_an_invalid_entry.wav pin \\d+ 5000` | Usage `<min> <max> <tries> <timeout> <terminators>` See [this](https://freeswitch.org/confluence/display/FREESWITCH/mod_dptools%3A+play_and_get_digits) for more details |
| | `bbb_dialin_overwrite_footer` | Set the default dial-in footer instead of `bbb_default_welcome_message_footer` | `false` | |
| | `bbb_dialin_footer` | The default dial-in notice, if you want to customize it, it is recommended to change `bbb_default_welcome_message_footer` instead | `<br><br>To join this meeting by phone, dial:<br>  %%DIALNUM%%<br>Then enter %%CONFNUM%% as the conference PIN number.` | |
| | `bbb_guestpolicy` | How guest can access | `ALWAYS_ACCEPT` | acceptable options: ALWAYS_ACCEPT, ALWAYS_DENY, ASK_MODERATOR | |
| | `bbb_ntp_cron` | Disable automatic time synchronisation and instead configure a cronjob | `false` | |
| | `bbb_ntp_cron_day` | Day of the month the time-sync job should run | `*` | |
| | `bbb_ntp_cron_hour` | Hour when the time-sync job should run | `5` | |
| | `bbb_ntp_cron_minute` | Minute when the time-sync job should run | `0` | |
| | `bbb_cron_history` | Retention period for presentations, kurento, and freeswitch caches | `5` | |
| | `bbb_cron_unrecorded_days` | Retention period of recordings for meetings with no recording markers | `14` | |
| | `bbb_cron_published_days` | Retention period of recordings’ raw data | `14` | |
| | `bbb_cron_log_history` | Set the retention period of old log files | `28` | |
| | `bbb_html5_node_options` | Allow to set extra options for node for the html5-webclient | unset | Could be used for example with <https://github.com/bigbluebutton/bigbluebutton/issues/11183> ; `--max-old-space-size=4096 --max_semi_space_size=128` |
| ⚠️ | `bbb_freeswitch_socket_password` | set password for freeswitch | | Can be generated with `pwgen -s 16 1` |
| ⚠️ | `bbb_freeswitch_default_password` | set the default password for freeswitch | | Can be generated with `pwgen -s 16 1` |
| | `bbb_html5_backend_processes` | amount of html5 backend processes | 1 | min = 1; max = 4 |
| | `bbb_html5_frontend_processes` | amount of html5 frontend processes | 1 | min = 1; max = 4; or 0 to let the same process do front- and backend (2.2 behavior) |
| | `bbb_html5_frontend_max_old_space_size` | max-old-space-size in frontends | `2048` | |
| | `bbb_container_compat` | Compatibility with unprivileged containers | `false` | Enabling this option allows to deploy BBB into a unprivileged container |
| | `bbb_firewall_ufw` | A dict of rules for the ufw | see `defaults/main.yml` | can also be used to allow/deny more/less |
| | `bbb_ufw_allow_networks_custom` | List of additional networks to be allowed by UFW | Not defined | |
| | `bbb_ufw_reject_networks_custom` | List of additional networks to be rejected by UFW | Not defined | |
| | `bbb_ssh_port` | Allow and limit the port used for SSH access | `22` | |
| | `bbb_max_file_size_upload`| Maximum file size for an uploaded presentation (default 30MB - number must be in byte) | 30000000| |
| | `bbb_http_session_timeout` | Timeout (seconds) to invalidate inactive HTTP sessions. | `14400` | 4 Hours |
| | `bbb_default_max_users` | Default maximum number of users a meeting can have | `0` | Meeting doesn't have a user limit |
| | `bbb_default_meeting_duration` | Default duration of the meeting in minutes | `0` | Meeting doesn't end |
| | `bbb_max_num_pages` | Maximum number of pages allowed for an uploaded presentation | `200` | |
| | `bbb_max_conversion_time` | Number of minutes the conversion should take | `5` | If it takes more than this time, cancel the conversion process |
| | `bbb_num_conversion_threads` | Number of threads in the pool to do the presentation conversion | `5` | |
| | `bbb_num_file_processor_threads` | Number of threads to process file uploads | `2` | |
| | `bbb_office_to_pdf_conversion_timeout` | Timeout(secs) to wait for conversion script execution | `60` | |
| | `bbb_office_to_pdf_max_concurrent_conversions` | Max concurrent of conversion script execution | `4` | |
| | `bbb_freeswitch_muted_sound` | Enable muted sound (`you are now muted`) | `true` | |
| | `bbb_freeswitch_unmuted_sound` | Enable unmuted sound (`you are now unmuted`) | `true` | |
| Deprecated | `bbb_breakout_rooms_enabled` | Enable or disable breakout rooms | `true` | use `bbb_disabled_features` instead |
| | `bbb_breakout_rooms_record` | Enable or disable recording in breakout rooms | `false` | |
| | `bbb_breakout_rooms_privatechat_enabled` | Enable or disable private chat in breakout rooms | `true` | |
| | `bbb_docker_compose_version` | Set [docker-compose python package version](https://pypi.org/project/docker/#history) | see `defaults/main.yml` | Sets the version of the docker-compose python package |
| | `bbb_docker_passwd` | Password to Docker Hub login | Not defined (default: disabled) | Set a Docker Hub password. When defined is used to avoid rate limits |
| | `bbb_docker_user` | Username to Docker Hub login | Not defined (default: disabled) | Set a Docker Hub user. When defined is used to avoid rate limits |
| | `bbb_etherpad_disable_cursortrace_plugin` | Disable or enable cursortrace plugin for etherpad | `false` | Set to `true` if you want to avoid displaying names at cursor position in shared notes |
| | `bbb_user_inactivity_inspect_timer` | User inactivity audit timer interval in minutes | `0` | If `0` inactivity inspection is deactivated |
| | `bbb_user_inactivity_threshold` | Number of minutes to consider a user inactive | `30` | A warning message is send to client to check if really inactive |
| | `bbb_webcams_only_for_moderator` | Allow webcams streaming reception only to and from moderators | `false` |  |
| | `bbb_allow_mods_to_eject_cameras` | Allow moderators to eject webcams | `false` |  |
| | `bbb_user_activity_sign_response_delay` | Number of minutes for user to respond to inactivity warning before being logged out | `5` |  |
| | `bbb_meeting_camera_cap` | Per meeting camera share limit, if 0, there's no limit | `0` |  |
| | `bbb_user_camera_cap` | Per user camera share limit, if 0, there's no limit | `3` |  |
| | `bbb_pinned_cameras` | Maximum number of cameras pinned simultaneously | `3` |  |
| | `bbb_end_when_no_moderator` |  | `false` |  |
| | `bbb_end_when_delay_in_minutes` |  | `1` |  |
| | `bbb_notify_recording_is_on` |  | `false` |  |
| | `bbb_allow_reveal_of_bbb_version` |  | `false` |  |
| Deprecated | `bbb_learning_dashboard_enabled` | Enable `true` / Disable `false` the [Learning Dashboard](https://docs.bigbluebutton.org/2.4/new.html#learning-dashboard) | `true` | use `bbb_disabled_features` instead|
| `bbb_default_meeting_layout` | Default Meeting Layout. Default Meeting Layout. Valid values are CUSTOM_LAYOUT, SMART_LAYOUT, PRESENTATION_FOCUS, VIDEO_FOCUS | `SMART_LAYOUT` | |
| | `bbb_disabled_features` | List of features to disable | `[]` | See https://docs.bigbluebutton.org/development/api#create for options |

### METEOR

With settings `bbb_meteor` it is possible to overwrite / change settings of meteor.

The following example is from [infra.run](https://gitlab.com/infra.run/public/ansible-bigbluebutton-tiny/-/blob/bbb-2.3/defaults/main.yml)

```yaml
bbb_meteor:
  public:
    note:
      url: "https://{{ inventory_hostname }}/pad"
    app:
      skipCheck: false
      mirrorOwnWebcam: true
      enableMultipleCameras: true
      enableNetworkInformation: true
      breakoutRoomLimit: 16
    chat:
      typingIndicator:
        enabled: false
    media:
      sipjsHackViaWs: true
    kurento:
      wsUrl: "wss://{{ inventory_hostname }}/bbb-webrtc-sfu"
      cameraProfiles:
      - id: low-u30
        name: low-u30
        bitrate: 30
        hidden: true
        constraints:
          frameRate: 3
      - id: low-u25
        name: low-u25
        bitrate: 40
        hidden: true
        constraints:
          frameRate: 3
      - id: low-u20
        name: low-u20
        bitrate: 50
        hidden: true
        constraints:
          frameRate: 5
      - id: low-u15
        name: low-u15
        bitrate: 70
        hidden: true
        constraints:
          frameRate: 8
      - id: low-u12
        name: low-u12
        bitrate: 90
        hidden: true
        constraints:
          frameRate: 10
      - id: low-u8
        name: low-u8
        bitrate: 100
        hidden: true
        constraints:
          frameRate: 10
      - id: low
        name: Low quality
        default: false
        bitrate: 50
      - id: medium
        name: Medium quality
        default: true
        bitrate: 200
      - id: high
        name: High quality
        default: false
        bitrate: 500
      - id: hd
        name: High definition
        default: false
        bitrate: 1200
      cameraQualityThresholds:
        enabled: true
        thresholds:
          - threshold: 8
            profile: low-u8
          - threshold: 12
            profile: low-u12
          - threshold: 15
            profile: low-u15
          - threshold: 20
            profile: low-u20
          - threshold: 25
            profile: low-u25
          - threshold: 30
            profile: low-u30
      cameraTimeouts:
        baseTimeout: 30000
      pagination:
        enabled: true
        pageChangeDebounceTime: 2500
        desktopPageSizes:
          moderator: 16
          viewer: 16
        mobilePageSizes:
          moderator: 8
          viewer: 8
```

### Cluster proxy

This role is capable of configuring BigBlueButton for the (cluster proxy setup)[https://docs.bigbluebutton.org/administration/cluster-proxy/].
To use this feature you need to define both `bbb_proxy_host` to the url of your cluster proxy and
`bbb_proxy_name` to the name your BBB host should have in the proxy
(you can set this e.g. to the subdomain of your BigBlueButton host, as shown in the defaults).
This role should then take care of configuring your BigBlueButton host correctly.
However, you still need to set up the cluster proxy itself, which this role will not do for you.
If you set up a nginx proxy as described in the official docs,
you can specify the locations using the variables used in this role in a jinja template like this:

```jinja
{% for host in groups['bigbluebutton'] %}
{% if hostvars[host].get('bbb_proxy_host') %}
location /{{ hostvars[host].bbb_proxy_name }}/html5client/ {
    proxy_pass https://{{ host }};
}
{% endif %}
{% endfor %}
```

### User Feedback logging
To enable client logging and/or userfeedback, you need to set `bbb_client_log_enable` to `true` add the following keys here:

```yaml
bbb_meteor:
  public:
    app:
      askForFeedbackOnLogout: true
    clientLog:
      external:
        enabled: true
        url: "https://{{ bbb_hostname }}/html5log"
```

### Modification of `bbb_webrtc_sfu_multikurento`

To add new keys to `bbb_webrtc_sfu_multikurento`, the defaults are actually stored in `bbb_webrtc_sfu_multikurento_default` and then assigned to `bbb_webrtc_sfu_multikurento`.

That way you can add new keys like something like this:
```yaml
tempvar:
  conference-media-specs:
    OPUS:
      maxaveragebitrate: "64000"


bbb_webrtc_sfu_multikurento: "{{ bbb_webrtc_sfu_multikurento_default | combine(tempvar)  }}"
```

### LXD/LXC compatibility

To run BigBlueButton in unprivileged LXD/LXC containers, you have to set `bbb_container_compat` to `true`.

### Phone dial-in

Example configuration using [sipgate](https://sipgate.de) for dial-in. Be sure to check with your provider if this usage is permitted.

```yaml
bbb_dialin_enabled: true
bbb_dialin_provider_proxy: 'sipgate.de'
bbb_dialin_provider_username: '158d43584d'
bbb_dialin_provider_password: 'xxxx-secret-xxxx'
bbb_dialin_provider_extension: '133713374223'
bbb_dialin_default_number: '0133 713-337-4223'
bbb_dialin_mask_caller: true
bbb_dialin_overwrite_footer: true
```

## Dependencies

- [geerlingguy.nodejs](https://github.com/geerlingguy/ansible-role-nodejs)
- [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker)

## Example Playbook

This is an example of how to use this role. *Warning:* the values of the variables should be changed!

Assuming the following directory structure:

```tree
├── ansible
    ├── roles
    │   └── ebbba.bigbluebutton
    ├── playbooks
    │   └── bigbluebutton.yml
    └── inventory
        ├── hosts
        ├── group_vars
        │   └── bigbluebutton
        │       └── bbb.yml
        └── host_vars
            └── your-domain.example.com
                └── vars.yml
```

You can follow these steps inside your ansible directory to clone the repository and use the example playbook and variable configuration files:

1. Clone the repository in your roles directory. (`git clone https://github.com/ebbba-org/ansible-role-bigbluebutton.git roles/ebbba.bigbluebutton`)

2. Copy the sample inventory hosts file or append its containt to your already existing hosts file(`cp roles/ebbba.bigbluebutton/examples/hosts inventory/hosts`).

3. Edit the inventory hosts file (`inventory/hosts`) to include all the hosts you want in the `bigbluebutton` group.

4. Create a directory with the name of the group inside group_vars (`mkdir inventory/group_vars/bigbluebutton`).

5. Copy the group_vars sample configuration file to the directory you created (`cp roles/ebbba.bigbluebutton/examples/bbb.yml inventory/group_vars/bigbluebutton/bbb.yml`).

6. Edit the group configuration file (`inventory/group_vars/bigbluebutton/bbb.yml`) to your liking. You should put here all the options that are common among all your bbb servers.

7. Create a directory for each of your servers to hold its configuration (`mkdir inventory/host_vars/<your-domain>`).

8. Copy the sample configuration file to each of the servers configuration directory (`cp roles/ebbba.bigbluebutton/examples/vars.yml inventory/host_vars/<your-domain>/vars.yml`).

9. Edit the host configuration file (`inventory/host_vars/<your-domain>/vars.yml`) to your liking. You should put here all the host specific options. Setting a variable here will override its value set in `inventory/group_vars/bigbluebutton/bbb.yml`.

10. Copy the sample playbook (`cp roles/ebbba.bigbluebutton/examples/playbook/bigbluebutton.yml playbooks`).

11. Run the playbook using `ansible-playbook -i inventory/hosts playbooks/bigbluebutton.yml`.

## Event though all the variables are explained above, you may also take a look at `roles/ebbba.bigbluebutton/defaults/main.yml` and see if there's something you'd like to copy over and override in your `vars.yml` and `bbb.yml` configuration files.

## License

MIT

[bbb_freeswitch_ipv6]: https://docs.bigbluebutton.org/support/troubleshooting.html#freeswitch-fails-to-bind-to-port-8021
