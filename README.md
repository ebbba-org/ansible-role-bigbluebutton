# BigBlueButton

[![Ansible Deployment Test](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml)
[![Ansible Lint](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml)
[![Release and Changelog Builder](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml)

This ansible role installs and configures [BigBlueButton](https://github.com/bigbluebutton/bigbluebutton) on a [suitable](https://docs.bigbluebutton.org/administration/install/#minimum-server-requirements) Ubuntu server. Many [customizations](https://docs.bigbluebutton.org/administration/customize/) are covered as well.

Ansible deployments are best suited for large cluster deployments with may BBB nodes. If you just want to install BBB on a single server, we recommend to follow the [official install instructions](https://docs.bigbluebutton.org/administration/install/) instead.

### Install, configure or upgrade BBB

For a first-time install, this role assumes to be applied to a fresh and unmodified Ubuntu 22.04 Server that meets [minimum requirements](https://docs.bigbluebutton.org/administration/install/#minimum-server-requirements) and has no conflicting services (e.g. webservers) already installed. See below for a comprehensive list of available configuration options and customizations.

You can re-apply this role on an empty server (with no running meetings) to deploy config changes or install patch-level upgrades.

### Upgrading from previous releases

**In-place upgrades from previous minor or major releases are not supported**. Those are hard to test properly and may break in subtile ways. Complex config changes may also leave artefact behind that cause issues. We **strongly** suggest to reset your operating system to a fresh and unmodified state before upgrading and start from scratch.

**Configuration for this role is also not backwards compatible between releases**. Variable names and defaults may change, features may be added or removed. Please check and revise your role configuration and test your deployment thoroughly before upgrading your cluster to a new release.


## Configuration

All role variables are prefixed with `bbb_` and most of them are optional. See `defaults/main.yaml` for a full list.

This role tries to focus on [customizations](https://docs.bigbluebutton.org/administration/customize/) that require changes in multiple places or additional steps to deploy. Most settings not explicitly covered by this role can be added to the *Config override* maps (`bbb_config_*`) described below. Do not edit config files directly, and do not rely on `apply-config.sh` for post-install modifications. This role will completely overwrite config files and does not use `bbb-conf`, so `apply-config.sh` won't be triggered.

If there is a feature or customizations missing from this role that can not easily be archived with *Config override*, feel free to open an issue or pull request.

### Basic configuration

**`bbb_hostname`** (default: `ansible_fqdn`)\
Public hostname for this BBB instance (e.g. `bbb.example.com`).

**`bbb_secret`** (required)\
The shared secret for API access. Should not contain any funny characters.

**`bbb_secret_seed`** (default: `bbb_secret`)\
A secret seed used to generate other host-local secrets and passwords. Override this if you feel paranoid.

**`bbb_version`** (default: `jammy-300`) \
  Install a specified BigBlueButton version (e.g. `jammy-300-3.0.1`). The version should of cause match whatever this role supports, or stuff may break.

**`bbb_upgrade`** (default: `false`)\
  Upgrade all installed packages (including BBB packages) every time this role is applied.

**`bbb_apt_mirror`** (default: `https://ubuntu.bigbluebutton.org`)\
  BBB repository server. Usefull if you want to switch to a local mirror (e.g. [this one](https://ftp.gwdg.de/pub/linux/misc/bigbluebutton/ubuntu/)). The *actual* repository is assumed to be located at `{{bbb_apt_mirror}}/{{bbb_version}}/`, so the mirror should follow upstream naming conventions.

**`bbb_apt_key`** (default: `{{ bbb_apt_mirror }}/repo/bigbluebutton.asc`)\
  Download URL for the BBB repository signing key.


### SSL/TLS

You can either use ACME (e.g. letsencrypt) to auto-generate certificates, or copy existing files to the host, or tell the role to do nothing and just assume the certificate files are already in the right place. 

**`bbb_acme_enable`** (default: `true`)\
  If true, automatically generate TLS certificates via ACME (e.g. letsencrypt). If you have a lot of servers you may need to throttle your deployments or switch to an ACME provider with higher rate limits.

**`bbb_acme_email`** (required if `bbb_acme_enable` is true)\
  E-mail address to use when registering an account with the ACME provider.

**`bbb_acme_api`** (default: `https://acme-v02.api.letsencrypt.org/directory`)\
  Change the ACME provider (example: `https://acme-staging-v02.api.letsencrypt.org/directory`)

**`bbb_acmesh_download`** (default: `https://raw.githubusercontent.com/acmesh-official/acme.sh/refs/heads/master/acme.sh`)\
  Download URL for `acme.sh`.

**`bbb_acmesh_update`** (default: `false`)\
  Download acme.sh every time the role is applied, instead of just once.

**`bbb_ssl_cert_file`** (no default)\
  Custom ssl cert file to upload to `bbb_ssl_cert` instead of using ACME.

**`bbb_ssl_key_file`** (required if `bbb_ssl_cert_file` is defined)\
  Custom ssl private key file to upload to  `bbb_ssl_key`. 

**`bbb_ssl_cert`** (default: `/etc/bigbluebutton/ssl/fullchain.cer`)\
  Location of the ssl fullchain file. Must exist or be created by one of the means above. 

**`bbb_ssl_key`** (default: `/etc/bigbluebutton/ssl/private.key`)\
  Location of the ssl private key file. Must exist or be created by one of the means above. 


### Firewall

**`bbb_ufw_enable`** (default: `false`)\
  Enable firewall (ufw).

**`bbb_ufw_policy`** (default: `deny`)\
  Default firewall input policy (allow/deny).

**`bbb_ufw_logging`** (default: `false`)\
  Enable excessive firewall logging for debugging purposes.

**`bbb_ufw_rules`** (default: `{}`)\
  A hash of named rules. Each rule can define `rule` (default: allow), `direction` (default: in), `from` (default: any), `to` (default: any) and `port` (required) properties. There are a bunch of default rules for BBB that can be overridden by using the same rule-name. Take special care to the `ssh` rule, which allows traffic from any IP to port 22 by default.
  To remove a named rule, set it to `false`. Just removing the named rule from config will not actually remove the rule in ufw.

**`bbb_ufw_reject_networks`** (default: `[]`)\
  Block outgoing traffic to these networks in addition to `bbb_ufw_reject_networks_default`, which contains all non-routeable (LAN) networks by default. This prevets a certain group of security issues where the BBB server is tricked into accessing non-public services on the private LAN.

**`bbb_ufw_allow_networks`** (default: `[]`)\
  Allow outgoing traffic to these networks in addition to `bbb_ufw_allow_networks_default`, which contains localhost and the internal docker nentwork by default, because those are required for BBB to function. Allowed networks will override rejected networks. 


### STUN/TURN Servers (NOT IMPLEMENTED YET)

**`bbb_coturn_enable`** (default: `false`)\
  Install a TURN server (coturn) alongside BBB.

**`bbb_stun_servers`** (default: `[]`)\
  A list of STUN Server URLs. Example: `["stun:stun.freeswitch.org"]`

**`bbb_ice_servers`** (default: `[]`)\
  A list of RemoteIceCandidate for STUN. Example: Not provided because I have no idea.

**`bbb_turn_servers`** (default: `[]`)\
  A list of TURN Server URLs and secrets. Example: `[{url: "turns:turn.example.com:443?transport=tcp", secret: "1234"}]`


### Cluster Proxy mode

For large deployments, it is common to run multiple BBB servers behind a scaler (e.g. Scalelite). New meetings are distributed across BBB servers and users are redirected to the server that hosts the meeting they are tyring to join. However, this creates a new problem: Users have to grant microphone, webcam and screen sharing permissions for each server individually and user settings are also not shared, which can be a real pain for large clusters. [Cluster Proxy mode](https://docs.bigbluebutton.org/administration/cluster-proxy/) allows you to serve the web client from a single domain and avoid most of those issues. This role coveres all configuration needed on the BBB node. **Additional changes are required on the font-end server**. Those are not covered by this role. See [Cluster Proxy Configuration](https://docs.bigbluebutton.org/administration/cluster-proxy/) for details.

**`bbb_cluster_proxy`** (no default)\
  If set, enable [Cluster Proxy](https://docs.bigbluebutton.org/administration/cluster-proxy/) mode and assume this host is configured as the front-end proxy (e.g `frontend.example.com`)

**`bbb_cluster_node`** (default: `{{ bbb_hostname | split('.') | first }}`)\
  Name of this cluster node. The front-end proxy must listen to requests for `https://{{bbb_cluster_proxy}}/{{bbb_cluster_node}}/*` and forward those to the matching back-end node via `https://{{bbb_hostname}}/`.


### Freeswitch

**`bbb_freeswitch_socket_password`** (default: auto-generated)\
  Freeswitch access password.

**`bbb_freeswitch_default_password`** (default: auto-generated)\
  Freeswitch default password.

**`bbb_freeswitch_ipv6`** (default: `true`)\
  Enable IPv6 support in FreeSWITCH. Disable to fix [FreeSWITCH IPv6 error][bbb_freeswitch_ipv6] 

**`bbb_freeswitch_local_ip`** (default: `127.0.0.1`)\
  Local IP address for FreeSWITCH websocket and other local bindings.

**`bbb_freeswitch_external_ip`** (default: `{{ ansible_default_ipv4.address }}`)\
  Either the public IP of the server, or a `stun:` server URL (e.g. `stun:stun.freeswitch.org`)

**`bbb_freeswitch_muted_sound`** (default: `true`)\
  Play `you are now muted` and `you are now unmuted` sounds.

**`bbb_dialplan_quality`** (default: `cdquality`)\
  Set the default dialplan for all conferences.

**`bbb_dialplan_energy_level`** (default: `100`)\
  Set target energy level for the default dialplan.

**`bbb_dialplan_comfort_noise`** (default: `1400`)\
  Set comfort noise for the default dialplan. Allowed values: (0-10000); 0 disables comfort-noise.


### Dial-in via SIP

**`bbb_dialin_enable`** (default: `false`)\
  Enable dial-in via phone. You need an external SIP provider for this to work.

**`bbb_dialin_provider_proxy`** (required if `bbb_dialin_enable` is true)\
  IP of your external SIP provider, also known as registrar.

**`bbb_dialin_provider_ip`** (required if `bbb_dialin_enable` and `bbb_firewall_enable` are true)\
  IP or network of your SIP provider.

**`bbb_dialin_provider_username`** (required if `bbb_dialin_enable` is true)\
  SIP account username

**`bbb_dialin_provider_password`** (required if `bbb_dialin_enable` is true)\
  SIP account password

**`bbb_dialin_provider_extension`** (required if `bbb_dialin_enable` is true)\
  Extension (external phone number) of your SIP account

**`bbb_dialin_default_number`** (default: `bbb_dialin_provider_extension`)\
  Number to present to users for dial-in. Used to replace `%%DIALNUM%%` in welcome messages.

**`bbb_dialin_pin_minlen`** (default: `5`)\
  Minimum conference PIN length. BBB generates 5-digit PINs by default, but front-ends may define their own PINs.

**`bbb_dialin_pin_maxlen`** (default: `5`)\
  Maximum conference PIN length. Must be equal or larger than `bbb_dialin_pin_minlen`.

**`bbb_dialin_pin_timeout`** (default: `10000`)\
  Timeout (ms) for entering the full pin number.

**`bbb_dialin_pin_maxwait`** (default: `5000`)\
  Maximum number of milliseconds to wait for the next digit. This is helpful if you have variable length PINs and users forget to terminate a short pin with `#`.

**`bbb_dialin_pin_retries`** (default: `3`)\
  Number of retries to enter a valid pin before freeswitch gives up and terminates the call.

**`bbb_dialin_mask_caller`** (default: `false`)\
  Hide parts of the caller ID for dial-in users to avoid privacy issues. Only the last couple of digits will be shown.
  Example: Masked users will show up as `tel-789` instead of their full caller ID.

**`bbb_dialin_mask_digits`** (default: `3`)\
  Number of digits to show if `bbb_dialin_mask_caller` is true.

**`bbb_dialin_mask_prefix`** (default: `tel-`)\
  Prefix added to masked caller IDs.


### Common customizations

**`bbb_default_welcome_message`** (default: `Welcome to <b>%%CONFNAME%%</b>!`)\
  Default welcome message. May contain simple HTML tags and certain wildcards (e.g. `%%CONFNAME%%`).

**`bbb_default_welcome_message_footer`** (default: `""`)\
  Default welcome message footer. Will be added to the welcome message even if the front-end overrides it.

**`bbb_default_presentation`** (default: `"${bigbluebutton.web.serverURL}/default.pdf"`)\
  Download link for the default presentation.

**`bbb_custom_presentation`** (no default)\
  Deploy a custom presentation file to replace `default.pdf`. Example: `path/to/default.pdf` 

**`bbb_use_default_logo`** (default: `false`)\
  Show a default-logo in the top left corner.

**`bbb_default_logo_url`** (default: `${bigbluebutton.web.serverURL}/logo.png`)\
  URL for the default logo.  

**`bbb_custom_logo`** (no default)\
  Deploy a custom default logo. Example `path/to/logo.png` 


### Config overrides

This role generates configuration with sensible defaults out of the box and covers lots of features that would otherwise be hard to configure manually. There are still lots of settings and possible customizations that are not covered by this role and may require some custom tweaking from your side. The following variables allow you to *override* or *extend* parts of the generated configuration. They are (deep-)merged into the role-managed config objects, just before they are written to disk. But be careful, there are no sanity or consistency checks. Test your deployment if you use those overrides.

**`bbb_config_web`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/bbb-web.properties`. This will be merged into the role-managed configuration. Example: `{muteOnStart: true, defaultMeetingLayout: SMART_LAYOUT}`

**`bbb_config_html5`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/bbb-html5.yml`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.

**`bbb_config_etherpad`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/etherpad.json`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.

**`bbb_config_presentation`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/recording/presentation.yml`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.


### Other stuff not full migrated to BBB 3.0 yet.

> [!warning]
This is a junkyard of old BBB 2.7 configs that are not fully migrated yet. They may work, but some are also broken, have no effect, or will be removed soon. Do not rely on these!!!

**`bbb_nginx_privacy`** (default: `false`)\
  Reduce nginx logging to just error logs.

**`bbb_web_logouturl`** (default: `default`)\
  set logout URL  Instead of using `bigbluebutton.web.serverURL` as default logout page, set another URL or customize logout page e.g. ${bigbluebutton.web.serverURL}/logout.html. API create call with the `logoutURL` parameter overwrite this setting 

**`bbb_allow_request_without_session`** (default: `false`)\
  Enable or disable allow request without session  Allow requests without JSESSIONID to be handled 

**`bbb_disable_recordings`** (default: `no`)\
  Disable options in gui to have recordings  [Recordings are running constantly in background](https://github.com/bigbluebutton/bigbluebutton/issues/9202) which is relevant as privacy relevant user data is stored 

**`bbb_api_demos_enable`** (default: `no`)\
  enable installation of the api demos   

**`bbb_mute_on_start`** (default: `no`)\
  start with muted mic on join   

**`bbb_app_log_level`** (default: `DEBUG`)\
  set bigbluebutton log level   

**`bbb_freeswitch_log_level`** (default: `warning`)\
  set freeswitch log level   

**`bbb_etherpad_log_level`** (default: `INFO`)\
  set etherpad log level   

**`bbb_fsels_akka_log_level`** (default: `ERROR`)\
  set the loglevel between freeswitch and bbb-apps   

**`bbb_apps_akka_log_level`** (default: `ERROR`)\
  set the loglevel for bbb-apps-akka   

**`bbb_kurento_interfaces`** (default: `{{ [ansible_default_ipv4.interface, 'lo'] }}`)\
  Specify the listening interfaces for kurento   

**`bbb_system_locale`** (default: `en_US.UTF-8`)\
  the system locale to use   

**`bbb_config_presentation`** (default: `{}`)\
  overwrite recording settings  See [Enable playback of recordings on iOS](https://docs.bigbluebutton.org/admin/customize.html#enable-playback-of-recordings-on-ios). 

**`bbb_webhooks_enable`** (default: `no`)\
  install bbb-webhooks   

**`bbb_check_for_running_meetings`** (default: `true`)\
  Check server and stop playbook in case of running meetings.   

**`bbb_guestpolicy`** (default: `ALWAYS_ACCEPT`)\
  How guest can access  acceptable options: ALWAYS_ACCEPT, ALWAYS_DENY, ASK_MODERATOR  |

**`bbb_cron_history`** (default: `5`)\
  Retention period for presentations, kurento, and freeswitch caches   

**`bbb_cron_unrecorded_days`** (default: `14`)\
  Retention period of recordings for meetings with no recording markers   

**`bbb_cron_published_days`** (default: `14`)\
  Retention period of recordings’ raw data   

**`bbb_cron_log_history`** (default: `28`)\
  Set the retention period of old log files   

**`bbb_html5_node_options`** (default: unset)\
  Allow to set extra options for node for the html5-webclient  Could be used for example with <https://github.com/bigbluebutton/bigbluebutton/issues/11183> ; `--max-old-space-size=4096 --max_semi_space_size=128` 

**`bbb_html5_backend_processes`** (default: 1)\
  amount of html5 backend processes  min = 1; max = 4 

**`bbb_html5_frontend_processes`** (default: 1)\
  amount of html5 frontend processes  min = 1; max = 4; or 0 to let the same process do front- and backend (2.2 behavior) 

**`bbb_html5_frontend_max_old_space_size`** (default: `2048`)\
  max-old-space-size in frontends   

**`bbb_container_compat`** (default: `false`)\
  Compatibility with unprivileged containers  Enabling this option allows to deploy BBB into a unprivileged container 

**`bbb_max_file_size_upload`** (default: 30000000)\
  Maximum file size for an uploaded presentation (default 30MB - number must be in byte)   

**`bbb_http_session_timeout`** (default: `14400`)\
  Timeout (seconds) to invalidate inactive HTTP sessions.  4 Hours 

**`bbb_default_max_users`** (default: `0`)\
  Default maximum number of users a meeting can have  Meeting doesn't have a user limit 

**`bbb_default_meeting_duration`** (default: `0`)\
  Default duration of the meeting in minutes  Meeting doesn't end 

**`bbb_max_num_pages`** (default: `200`)\
  Maximum number of pages allowed for an uploaded presentation   

**`bbb_max_conversion_time`** (default: `5`)\
  Number of minutes the conversion should take  If it takes more than this time, cancel the conversion process 

**`bbb_num_conversion_threads`** (default: `5`)\
  Number of threads in the pool to do the presentation conversion   

**`bbb_num_file_processor_threads`** (default: `2`)\
  Number of threads to process file uploads   

**`bbb_office_to_pdf_conversion_timeout`** (default: `60`)\
  Timeout(secs) to wait for conversion script execution   

**`bbb_office_to_pdf_max_concurrent_conversions`** (default: `4`)\
  Max concurrent of conversion script execution   

**`bbb_breakout_rooms_record`** (default: `false`)\
  Enable or disable recording in breakout rooms   

**`bbb_breakout_rooms_privatechat_enable`** (default: `true`)\
  Enable or disable private chat in breakout rooms   

**`bbb_docker_config`** (default: `{"log-driver": "journald"}`)\
  Docker daemon config  Set to `False` to keep original file 

**`bbb_docker_user`** (default: Not defined (default: disabled))\
  Username to Docker Hub login  Set a Docker Hub user. When defined is used to avoid rate limits 

**`bbb_docker_passwd`** (default: Not defined (default: disabled))\
  Password to Docker Hub login  Set a Docker Hub password. When defined is used to avoid rate limits 

**`bbb_user_inactivity_inspect_timer`** (default: `0`)\
  User inactivity audit timer interval in minutes  If `0` inactivity inspection is deactivated 

**`bbb_user_inactivity_threshold`** (default: `30`)\
  Number of minutes to consider a user inactive  A warning message is send to client to check if really inactive 

**`bbb_webcams_only_for_moderator`** (default: `false`)\
  Allow webcams streaming reception only to and from moderators   

**`bbb_allow_mods_to_eject_cameras`** (default: `false`)\
  Allow moderators to eject webcams   

**`bbb_user_activity_sign_response_delay`** (default: `5`)\
  Number of minutes for user to respond to inactivity warning before being logged out   

**`bbb_meeting_camera_cap`** (default: `0`)\
  Per meeting camera share limit, if 0, there's no limit   

**`bbb_user_camera_cap`** (default: `3`)\
  Per user camera share limit, if 0, there's no limit   

**`bbb_pinned_cameras`** (default: `3`)\
  Maximum number of cameras pinned simultaneously   

**`bbb_end_when_no_moderator`** (default: `false`)

**`bbb_end_when_delay_in_minutes`** (default: `1`)

**`bbb_notify_recording_is_on`** (default: `false`)

**`bbb_allow_reveal_of_bbb_version`** (default: `false`)

**`bbb_default_meeting_layout`** (no default)\
  Default Meeting Layout. Valid values are `CUSTOM_LAYOUT`, `SMART_LAYOUT`, `PRESENTATION_FOCUS`, `VIDEO_FOCUS`, `SMART_LAYOUT`

**`bbb_disabled_features`** (default: `[]`)\
  List of features to disable. See https://docs.bigbluebutton.org/development/api#create for options 


### LXD/LXC compatibility

To run BigBlueButton in unprivileged LXD/LXC containers, you have to set `bbb_container_compat` to `true`.


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
