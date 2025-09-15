# Ansible Role for BigBlueButton

[![Ansible Deployment Test](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/full_deployment.yml)
[![Ansible Lint](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/ansible-lint.yaml)
[![Release and Changelog Builder](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml/badge.svg)](https://github.com/ebbba-org/ansible-role-bigbluebutton/actions/workflows/changelog_builder.yml)

This ansible role installs and configures [BigBlueButton](https://github.com/bigbluebutton/bigbluebutton) with support for advanced [customizations](https://docs.bigbluebutton.org/administration/customize/) and configurations.

Installation requires a fresh and unmodified Ubuntu 22.04 Server that meets [minimum requirements](https://docs.bigbluebutton.org/administration/install/#minimum-server-requirements) an has no conflicting services (e.g. webservers) running. The role can be re-applied again on the same server to deploy config changes or install patch-level upgrades.

> [!note]
Ansible deployments are best suited for large cluster deployments with may BBB nodes or complex configurations. If you just want to install vanilla BBB on a single server, we recommend to follow the [official install instructions](https://docs.bigbluebutton.org/administration/install/) instead.


### Role compatibility with BigBlueButton releases

For this role we try our best to support the most recent patch-level of each BigBlueButton release currently supported by upstream. Here is a quick overview:

* The `main` branch usually targets the *next* BigBlueButton release. Use this for testing new release candidates or working on future versions of this role.
* The `bbb/X.Y` branches target a specific BigBlueButton release (e.g. `3.0`) and will install the latest patch release by default. Use these to keep up with new patches, features and workarounds. 
* Tags like `vX.Y.Z`  mark a version of this role that was tested against a specific BigBlueButton patch-release and published to ansible galaxy. We only do this if we had enough time to test and the role actually changed since the last published release, so releases may be skipped and delayed. We currently recommend watching the branches instead.

> [!warning]
BigBlueButton does not follow [SemVer](https://semver.org/) and sometimes intoduces breaking changes in minor releases or even patch releases. The only way to be sure everything still works is to actually test it, especially if you run configurations that are not properly tested by upstream. Be prepared, run your own test environment and test each release (including patch releases) before upgrading your production environment. Downgrading to a previous release is usually not possible without extra steps.


### Upgrading from previous releases

**In-place upgrades from previous minor or major releases are not fully supported**. Those are hard to test properly and may break in subtile ways. Complex config changes may also leave artefact behind that cause issues. We **strongly** suggest to reset your operating system to a fresh and unmodified state before upgrading.

**Configuration for this role is also not strictly backwards compatible across releases**. Variable names and defaults may change, features may be added or removed. Please check and test your role configuration thoroughly before upgrading your production environment to a new release. 


### Getting Started

Check out the [examples](https://github.com/ebbba-org/ansible-role-bigbluebutton/tree/master/examples) and start from there, or install this role into your existing environment directly from git via `ansible-galaxy role install git+https://github.com/ebbba-org/ansible-role-bigbluebutton.git,bbb/3.0`. Older releases are also published to [ansible galaxy](https://galaxy.ansible.com/ui/standalone/roles/ebbba/bigbluebutton/).


## Configuration

All role variables are prefixed with `bbb_` and most of them are optional. See `defaults/main.yaml` for a full list.

This role tries to focus on more complex [settings and features](https://docs.bigbluebutton.org/administration/customize/) that are difficult to apply or require additional steps to work properly. Everything else should be covered by *Config overrides* (see `bbb_config_*`). If you find a useful feature or setting not covered by this role and not suitable for config overrides, feel free to open a feature or pull request.

Note that this role does not use `bbb-install.sh` or `bbb-conf` and won't trigger `apply-config.sh` hooks.


### Basic configuration

* **`bbb_hostname`** (default: `ansible_fqdn`)\
Public hostname for this BBB instance (e.g. `bbb.example.com`).

* **`bbb_secret`** (required)\
The shared secret for API access. Should not contain any funny characters.

* **`bbb_secret_seed`** (default: `bbb_secret`)\
A secret seed used to generate other host-local secrets and passwords. Override this if you feel paranoid.

* **`bbb_version`** (default: `jammy-300`) \
  Install a specified BigBlueButton version (e.g. `jammy-300-3.0.1`). The version should of cause match whatever this role supports, or stuff may break.

* **`bbb_upgrade`** (default: `true`)\
  Upgrade all installed packages (including BBB packages) every time this role is applied.

* **`bbb_apt_mirror`** (default: `https://ubuntu.bigbluebutton.org`)\
  BBB repository server. Usefull if you want to switch to a local mirror (e.g. [this one](https://ftp.gwdg.de/pub/linux/misc/bigbluebutton/ubuntu/)). The *actual* repository is assumed to be located at `{{bbb_apt_mirror}}/{{bbb_version}}/`, so the mirror should follow upstream naming conventions.

* **`bbb_apt_key`** (default: `{{ bbb_apt_mirror }}/repo/bigbluebutton.asc`)\
  Download URL for the BBB repository signing key.

* **`bbb_check_running`** (default: `true`)\
  Fail if there are active meetings on the server. Set this to false on test servers where you do not care about forcefully ending meetings.


### Networking

* **`bbb_set_hostname`** (default: `{{ bbb_hostname }}`)\
  Set the local system hostname to match `bbb_hostname` by default. `False` will
  skip this step and not change the current local hostname.

* **`bbb_local_ip`** (default: `127.0.0.1`)\
  IP of your loopback device.

* **`bbb_bind_ip4`** (default: `{{ ansible_default_ipv4.address }}`)\
  IP (v4) address public services should bind to. This may be a LAN IP if your
  server is behind a NAT router and does not know its own public IP. Do not
  forget to set `bbb_public_ip4` in this case!

* **`bbb_public_ip4`** (default: `{{ ansible_default_ipv4.address }}`)\
  Public IPv4 address of your server. Required if ansible cannot detect your
  public IP automatically. This may happen if your server is behind a NAT router
  and your public IP is not assigned to the primary interface, or if your primary
  interface has multiple IPs assigned and the first one is not your public IP.

* **`bbb_bind_ip6`** (default: `{{ ansible_default_ipv6.address | default(None) }}`)\
  Same as `bbb_bind_ip4` but for IPv6. Set this to `None` to disable IPv6 even
  if your server technically supports it.

* **`bbb_public_ip6`** (default: `{{ ansible_default_ipv6.address | default(None) }}`)\
  Same as `bbb_public_ip4` but for IPv6. Set this to `None` to disable IPv6 even
  if your server technically supports it.

* **`bbb_net_mtu`** (default: `{{ ansible_default_ipv4.mtu | default(1500) }}`)\
  MTU (maximum transfer unit) for outgoing packets. Some cloud environments
  use a smaller MTU and docker needs extra configuration in that case.


### SSL/TLS

You can either use ACME (e.g. letsencrypt) to auto-generate certificates, or copy existing files to the host, or tell the role to do nothing and just assume the certificate files are already in the correct place.

* **`bbb_acme_enable`** (default: `true`)\
  Automatically generate TLS certificates via ACME (e.g. letsencrypt). If you have a lot of servers you may need to throttle your deployments or switch to an ACME provider with higher rate limits.

* **`bbb_acme_email`** (required if `bbb_acme_enable` is true)\
  E-mail address to use when registering an account with the ACME provider.

* **`bbb_acme_api`** (default: `https://acme-v02.api.letsencrypt.org/directory`)\
  Change the ACME provider (example: `https://acme-staging-v02.api.letsencrypt.org/directory`)

* **`bbb_acmesh_download`** (default: `https://raw.githubusercontent.com/acmesh-official/acme.sh/refs/heads/master/acme.sh`)\
  Download URL for `acme.sh`.

* **`bbb_acmesh_update`** (default: `false`)\
  Download `acme.sh` every time the role is applied, instead of just once.

* **`bbb_ssl_cert_file`** (no default)\
  Custom ssl cert file to upload to `bbb_ssl_cert` instead of using ACME.

* **`bbb_ssl_key_file`** (required if `bbb_ssl_cert_file` is defined)\
  Custom ssl private key file to upload to  `bbb_ssl_key`. 

* **`bbb_ssl_cert`** (default: `/etc/bigbluebutton/ssl/fullchain.cer`)\
  Location of the ssl fullchain file. Must exist or be created by one of the means above. 

* **`bbb_ssl_key`** (default: `/etc/bigbluebutton/ssl/private.key`)\
  Location of the ssl private key file. Must exist or be created by one of the means above. 

* **`bbb_ssl_owner`** (default: `root`)\
  Linux filesystem owner of the SSL files.

* **`bbb_ssl_group`** (default: `root`)\
  Linux filesystem group of the SSL files.

### Firewall

* **`bbb_ufw_enable`** (default: `false`)\
  Enable firewall (ufw). This is required if you use `bbb_coturn_enable` and `bbb_public_ip4` differs from `bbb_bind_ip4` (NAT).

* **`bbb_ufw_policy`** (default: `deny`)\
  Default firewall input policy (allow/deny).

* **`bbb_ufw_logging`** (default: `false`)\
  Enable excessive firewall logging for debugging purposes.

* **`bbb_ufw_rules`** (default: `{}`)\
  A hash of named rules. Each rule can define `rule` (default: allow), `direction` (default: in), `from` (default: any), `to` (default: any) and `port` (required) properties. There are a bunch of default rules for BBB that can be overridden by using the same rule-name. Take special care to the `ssh` rule, which allows traffic from any IP to port 22 by default.
  To remove a named rule, set it to `false`. Just removing the named rule from config will not actually remove the rule in ufw.

* **`bbb_ufw_reject_networks`** (default: `[]`)\
  Block outgoing traffic to these networks in addition to `bbb_ufw_reject_networks_default`, which contains all non-routeable (LAN) networks by default. This prevets a certain group of security issues where the BBB server is tricked into accessing non-public services on the private LAN.

* **`bbb_ufw_allow_networks`** (default: `[]`)\
  Allow outgoing traffic to these networks in addition to `bbb_ufw_allow_networks_default`, which contains localhost and the internal docker network by default, because those are required for BBB to function. Allowed networks will override rejected networks. 


### Storage

BigBlueButton stores state and recordings in `/var/bigbluebutton` and most of its logs in `/var/log/bigbluebutton`. If you have a large cluster you can reduce storage costs by moving those directories to an NFS server and deploy your BBB nodes with smaller root disks instead. `bbb_nfs_share` helps you with that. If you want to deploy other solutions (ceph, samba, extra block devices) then the `bbb_symlink_*` may still be helpful.

> [!note]
> This role won't move or remove existing data, which means you cannot change `bbb_nfs_share` or `bbb_symlink_*` once BBB is installed. Migrating data between storage locations at a later point is possible, but requires manual steps and is out of scope for this role.

* **`bbb_nfs_share`** (no default)\
  If defined, the role will install `nfs-common`, mount the specified NFS share to `bbb_nfs_mount`, create `var` and `log` subdirectories and set `bbb_symlink_var` and `bbb_symlink_log` to point to those directories. **Make sure that each BBB server has a dedicated directory on your NFS server**, and that the remove directory exists and can be mounted. It will not be created by this role. Example: `nfs.example.com:/exports/bbb/{{ bbb_hostname }}/`

* **`bbb_nfs_opts`** (default: `defaults,tcp,nofail,lookupcache=positive,_netdev`)\
  Mount options for `bbb_nfs_share`.

* **`bbb_nfs_mount`** (default: `/mnt/bigbluebutton`)\
  Target directory (mount point) for `bbb_nfs_share`.

* **`bbb_symlink_var`** (no default, conflicts with `bbb_nfs_share`)\
  If defined, create a symlink from `/var/bigbluebutton` to the specified directory before installing BBB. This is useful if you want to store BBB state and recordings in a different location. The role will fail if the target directory does not exist, or if `/var/bigbluebutton` is a non-empty directory. It won't move or remove any existing data.

* **`bbb_symlink_log`** (no default, conflicts with `bbb_nfs_share`)\
  Same as `bbb_symlink_var` but for `/var/log/bigbluebutton`.


### STUN/TURN Servers

* **`bbb_coturn_enable`** (default: True if `bbb_turn_servers` is empty)\
  Install a TURN server (coturn) alongside BBB, which helps clients behind restrictive firewalls to connect. You usually
  want TURN to listen on port 443 (HTTPS) for best compatibility. To avoid the need of a dedicated public IP just for TURN,
  this role installs `haproxy` to redirect traffic to either coturn or nginx based on the type of traffic.

* **`bbb_stun_servers`** (default: `[]`)\
  A list of STUN Server URLs. You do not need those if you have a TURN server. Example: `["stun:stun.freeswitch.org"]`

* **`bbb_ice_servers`** (default: `[]`)\
  A list of RemoteIceCandidate for STUN. If you do not know what this does, ignore it.

* **`bbb_turn_servers`** (default: `[]`)\
  A list of *external* TURN Server URLs and secrets. You do not need those if you run an embedded TURN server via `bbb_coturn_enable`. Example: `[{url: "turns:turn.example.com:443?transport=tcp", secret: "1234"}]`


### Cluster Proxy mode

For large deployments, it is common to run multiple BBB servers behind a scaler (e.g. Scalelite). New meetings are distributed across BBB servers and users are redirected to the server that hosts the meeting they are tyring to join. However, this creates a new problem: Users have to grant microphone, webcam and screen sharing permissions for each server individually and user settings are also not shared, which can be a real pain for large clusters. [Cluster Proxy mode](https://docs.bigbluebutton.org/administration/cluster-proxy/) allows you to serve the web client from a single domain and avoid most of those issues. This role coveres all configuration needed on the BBB node. **Additional changes are required on the font-end server**. Those are not covered by this role. See [Cluster Proxy Configuration](https://docs.bigbluebutton.org/administration/cluster-proxy/) for details.

* **`bbb_cluster_proxy`** (no default)\
  If defined, enable [Cluster Proxy](https://docs.bigbluebutton.org/administration/cluster-proxy/) mode and assume this host is configured as the front-end proxy (e.g `frontend.example.com`)

* **`bbb_cluster_node`** (default: `{{ bbb_hostname | split('.') | first }}`)\
  Name of this cluster node. The front-end proxy must listen to requests for `https://{{bbb_cluster_proxy}}/{{bbb_cluster_node}}/*` and forward those to the matching back-end node via `https://{{bbb_hostname}}/`.


### Freeswitch

* **`bbb_freeswitch_socket_password`** (default: auto-generated)\
  Freeswitch access password.

* **`bbb_freeswitch_default_password`** (default: auto-generated)\
  Freeswitch default password.

* **`bbb_freeswitch_muted_sound`** (default: `true`)\
  Play `you are now muted` and `you are now unmuted` sounds.

* **`bbb_dialplan_quality`** (default: `cdquality`)\
  Set the default dialplan for all conferences.

* **`bbb_dialplan_energy_level`** (default: `100`)\
  Set target energy level for the default dialplan.

* **`bbb_dialplan_comfort_noise`** (default: `1400`)\
  Set comfort noise for the default dialplan. Allowed values: (0-10000); 0 disables comfort-noise.


### Dial-in via SIP

When operating a cluster, you usually have a dedicated phone number per BBB
server, or you run your own SIP gateway (e.g. freeswitch) that routes calls from
your actual external SIP provider to the correct BBB server based on a phone
number extension or PIN. Such a setup can quickly become complicated and this
role can only help you with the configuration on the BBB node itself. For the
rest, you are on your own. Good luck!

* **`bbb_dialin_enable`** (default: `false`)\
  Enable dial-in via phone. You need an external SIP provider for this to work.

* **`bbb_dialin_provider`** (required if `bbb_dialin_enable` is true)\
  Domain or IP of your SIP provider, also known as registrar. Example: `sip.example.com`

* **`bbb_dialin_provider_ip`** (required if `bbb_dialin_enable` and `bbb_firewall_enable` are true)\
  IP or network of your SIP provider. Example: `1.2.3.4` or ``

* **`bbb_dialin_provider_username`** (required if `bbb_dialin_enable` is true)\
  SIP account username.

* **`bbb_dialin_provider_password`** (required if `bbb_dialin_enable` is true)\
  SIP account password.

* **`bbb_dialin_provider_extension`** (required if `bbb_dialin_enable` is true)\
  Extension (external phone number) of your SIP account.

* **`bbb_dialin_default_number`** (default: `bbb_dialin_provider_extension`)\
  Number to present to users for dial-in. Used to replace `%%DIALNUM%%` in welcome messages.

* **`bbb_dialin_pin_minlen`** (default: `5`)\
  Minimum conference PIN length. BBB generates 5-digit PINs by default, but front-ends may define their own PINs.

* **`bbb_dialin_pin_maxlen`** (default: `5`)\
  Maximum conference PIN length. Must be equal or larger than `bbb_dialin_pin_minlen`.

* **`bbb_dialin_pin_timeout`** (default: `10000`)\
  Timeout (ms) for entering the full pin number.

* **`bbb_dialin_pin_maxwait`** (default: `5000`)\
  Maximum number of milliseconds to wait for the next digit. This is helpful if you have variable length PINs and users forget to terminate a short pin with `#`.

* **`bbb_dialin_pin_retries`** (default: `3`)\
  Number of retries to enter a valid pin before freeswitch gives up and terminates the call.

* **`bbb_dialin_mask_caller`** (default: `false`)\
  Hide parts of the caller ID for dial-in users to avoid privacy issues. Only the last couple of digits will be shown.
  Example: Masked users will show up as `tel-789` instead of their full caller ID.

* **`bbb_dialin_mask_digits`** (default: `3`)\
  Number of digits to show if `bbb_dialin_mask_caller` is true.

* **`bbb_dialin_mask_prefix`** (default: `tel-`)\
  Prefix added to masked caller IDs.


### Common customizations

* **`bbb_default_welcome_message`** (default: `Welcome to <b>%%CONFNAME%%</b>!`)\
  Default welcome message. May contain simple HTML tags and certain wildcards (e.g. `%%CONFNAME%%`).

* **`bbb_default_welcome_message_footer`** (default: `""`)\
  Default welcome message footer. Will be added to the welcome message even if the front-end overrides it.

* **`bbb_default_presentation`** (default: `"${bigbluebutton.web.serverURL}/default.pdf"`)\
  Download link for the default presentation. This can be any URL, but is usually a `default.pdf` hosted on the BBB server itself.

* **`bbb_default_presentation_file`** (no default)\
  Replace `default.pdf` with a custom presentation file. Example: `path/to/default.pdf` 

* **`bbb_default_logo_enable`** (default: `false`)\
  Show a default logo in the top left corner, even if the frontend did not provide one. Usually no logo is shown unless the frontend asks for it.

* **`bbb_default_logo`** (default: `${bigbluebutton.web.serverURL}/images/logo.png`)\
  URL for the default logo. Frontends can override this.

* **`bbb_default_logo_file`** (no default)\
  Replace the default `logo.png` with a custom file. Example `path/to/logo.png` 

* **`bbb_default_darklogo`** (default: `${bigbluebutton.web.serverURL}/images/darklogo.png`)\
  URL for the default logo in dark mode. Frontends can override this.

* **`bbb_default_darklogo_file`** (no default)\
  Replace the default `darklogo.png` with a custom file. Example `path/to/darklogo.png` 

* **`bbb_virtual_backgrounds`** (default: `[home.jpg, coffeeshop.jpg, board.jpg]`)\
  List of virtual webcam background images. Provide just a filename for files that already exist on the server, or a local path for a file to upload. The filenames must be unique and must not contain any funny characters.

* **`bbb_html5_style`** (no default)\
  Change default colors or other visual aspects of the client with custom styles.
  If the variable is defined and contains `;` then its content is written
  directly to a `custom.css` on the server, otherwise it is assumed to be a local
  file with CSS code you want to upload. Frontends can override styles.
  It is currently not documented which CSS variables and colors are used by the
  client, but see [palette.js](https://github.com/bigbluebutton/bigbluebutton/blob/v3.0.x-release/bigbluebutton-html5/imports/ui/stylesheets/styled-components/palette.js).
  Example: `path/to/custom.css` or `:root { --color-primary: green; }`.

* **`bbb_fonts`** (default: `{{ bbb_fonts_base + bbb_fonts_extra }}`)\
  A list of font packages (without `fonts-` prefix) to install.
  The defaults in `bbb_fonts_base` should cover most languages and offer
  suitable replacements for common proprietary windows or mac fonts. Add your
  own fonts to `bbb_fonts_extra`. You only need to override this variable if you
  do not want to install fonts from the `bbb_fonts_base` list (see `vars/main.yml`).
  Note that the role won't uninstall any fonts.

* **`bbb_fonts_extra`** (default: `[]`)\
  Additional font packages (without `fonts-` prefix) to install. Add your own
  fonts here. See `bbb_fonts`.


### Recordings

* **`bbb_recording_enable`** (default: `true`)\
  Enable recordings. This will allow users to start recordings in meetings started with `record=true`.

* **`bbb_recording_formats`** (default: `[presentation]`)
  List of recording formats to render. This configures `process` and `publish` steps for each format and installs additional packages for the built-in formats: `presentation`, `video`, `screenshare` and `podcast`.

* **`bbb_recording_mp4`** (default: `False`)\
  Generate additional mp4-encoded videos for supported recording formats as a fallback for older iOS devices.

* **`bbb_cron_history`** (default: `5`)\
  Days to keep raw presentation files, caches and media streams.

* **`bbb_cron_unrecorded_days`** (default: `14`)\
  Days to keep raw recording data for meetings without recording markers.

* **`bbb_cron_published_days`** (default: `14`)\
  Days to keep raw recording data for published recordings.

* **`bbb_cron_log_history`** (default: `28`)\
  Days to keep logfiles.


### Optional components

* **`bbb_venv`** (default: `/opt/venv`)\
  Install path for Python tools or helpers fetched from [pypi.org](https://pypi.org/)

* **`bbb_bbbctl_enable`** (default: `true`)\
  Install [bbbctl](https://pypi.org/project/bbbctl/).

* **`bbb_webhooks_enable`** (default: `false`)\
  Install bbb-webhooks. This is required by some frontends and recommended.


### Docker

* **`bbb_docker_config`** (default: `{"log-driver": "journald", "mtu": bbb_net_mtu}`)\
  Docker daemon config. Set to `False` to keep original file 

* **`bbb_docker_user`** (no default)\
  DockerHub account username. Useful to avoid rate limits.

* **`bbb_docker_passwd`** (required if `bbb_docker_user` is defined)\
  DockerHub account password.


### Config overrides

This role generates configuration with sensible defaults out of the box and covers lots of features that would otherwise be hard to configure manually. There are still some settings and possible customizations that are not covered by this role and may require some custom tweaking from your side. The following variables allow you to *override* or *extend* parts of the generated configuration. They are (deep-)merged into the role-managed configuration objects, just before they are written to disk. But be careful, there are no sanity or consistency checks. Test your deployment if you use those overrides.

* **`bbb_config_web`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/bbb-web.properties`. This will be merged into the role-managed configuration. Example: `{muteOnStart: true, defaultMeetingLayout: SMART_LAYOUT}`

* **`bbb_config_html5`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/bbb-html5.yml`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.

* **`bbb_config_etherpad`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/etherpad.json`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.

* **`bbb_config_presentation`** (default: `{}`)\
  Custom overrides for `/etc/bigbluebutton/recording/presentation.yml`. This will be deep-merged into the role-managed configuration. List values will not be merged, but replaced.


### Other stuff not full migrated to BBB 3.0 yet.

> [!warning]
This is a junkyard of old BBB 2.7 configs that are not fully migrated yet. They may work, but some are also broken, have no effect, or will be removed soon. Do not rely on these!!!

* **`bbb_nginx_privacy`** (default: `false`)\
  Reduce nginx logging to just error logs.

* **`bbb_web_logouturl`** (default: `default`)\
  set logout URL  Instead of using `bigbluebutton.web.serverURL` as default logout page, set another URL or customize logout page e.g. ${bigbluebutton.web.serverURL}/logout.html. API create call with the `logoutURL` parameter overwrite this setting 

* **`bbb_allow_request_without_session`** (default: `false`)\
  Enable or disable allow request without session  Allow requests without JSESSIONID to be handled 

* **`bbb_api_demos_enable`** (default: `no`)\
  enable installation of the api demos   

* **`bbb_mute_on_start`** (default: `no`)\
  start with muted mic on join   

* **`bbb_app_log_level`** (default: `DEBUG`)\
  set bigbluebutton log level   

* **`bbb_freeswitch_log_level`** (default: `warning`)\
  set freeswitch log level   

* **`bbb_etherpad_log_level`** (default: `INFO`)\
  set etherpad log level   

* **`bbb_fsels_akka_log_level`** (default: `ERROR`)\
  set the loglevel between freeswitch and bbb-apps   

* **`bbb_apps_akka_log_level`** (default: `ERROR`)\
  set the loglevel for bbb-apps-akka   

* **`bbb_system_locale`** (default: `en_US.UTF-8`)\
  the system locale to use   

* **`bbb_guestpolicy`** (default: `ALWAYS_ACCEPT`)\
  How guest can access  acceptable options: ALWAYS_ACCEPT, ALWAYS_DENY, ASK_MODERATOR  |

* **`bbb_container_compat`** (default: `false`)\
  Compatibility with unprivileged containers. Enabling this option allows to deploy BBB into a unprivileged container.

* **`bbb_max_file_size_upload`** (default: 30000000)\
  Maximum file size for an uploaded presentation (default 30MB - number must be in byte)   

* **`bbb_http_session_timeout`** (default: `14400`)\
  Timeout (seconds) to invalidate inactive HTTP sessions.  4 Hours 

* **`bbb_default_max_users`** (default: `0`)\
  Default maximum number of users a meeting can have  Meeting doesn't have a user limit 

* **`bbb_default_meeting_duration`** (default: `0`)\
  Default duration of the meeting in minutes  Meeting doesn't end 

* **`bbb_max_num_pages`** (default: `200`)\
  Maximum number of pages allowed for an uploaded presentation   

* **`bbb_max_conversion_time`** (default: `5`)\
  Number of minutes the conversion should take  If it takes more than this time, cancel the conversion process 

* **`bbb_num_conversion_threads`** (default: `5`)\
  Number of threads in the pool to do the presentation conversion   

* **`bbb_num_file_processor_threads`** (default: `2`)\
  Number of threads to process file uploads   

* **`bbb_office_to_pdf_conversion_timeout`** (default: `60`)\
  Timeout(secs) to wait for conversion script execution   

* **`bbb_office_to_pdf_max_concurrent_conversions`** (default: `4`)\
  Max concurrent of conversion script execution   

* **`bbb_breakout_rooms_record`** (default: `false`)\
  Enable or disable recording in breakout rooms   

* **`bbb_breakout_rooms_privatechat_enable`** (default: `true`)\
  Enable or disable private chat in breakout rooms   

* **`bbb_user_inactivity_inspect_timer`** (default: `0`)\
  User inactivity audit timer interval in minutes  If `0` inactivity inspection is deactivated 

* **`bbb_user_inactivity_threshold`** (default: `30`)\
  Number of minutes to consider a user inactive  A warning message is send to client to check if really inactive 

* **`bbb_webcams_only_for_moderator`** (default: `false`)\
  Allow webcams streaming reception only to and from moderators   

* **`bbb_allow_mods_to_eject_cameras`** (default: `false`)\
  Allow moderators to eject webcams   

* **`bbb_user_activity_sign_response_delay`** (default: `5`)\
  Number of minutes for user to respond to inactivity warning before being logged out   

* **`bbb_meeting_camera_cap`** (default: `0`)\
  Per meeting camera share limit, if 0, there's no limit   

* **`bbb_user_camera_cap`** (default: `3`)\
  Per user camera share limit, if 0, there's no limit   

* **`bbb_pinned_cameras`** (default: `3`)\
  Maximum number of cameras pinned simultaneously   

* **`bbb_end_when_no_moderator`** (default: `false`)

* **`bbb_end_when_delay_in_minutes`** (default: `1`)

* **`bbb_notify_recording_is_on`** (default: `false`)

* **`bbb_allow_reveal_of_bbb_version`** (default: `false`)

* **`bbb_default_meeting_layout`** (no default)\
  Default Meeting Layout. Valid values are `CUSTOM_LAYOUT`, `SMART_LAYOUT`, `PRESENTATION_FOCUS`, `VIDEO_FOCUS`, `SMART_LAYOUT`

* **`bbb_disabled_features`** (default: `[]`)\
  List of features to disable. See https://docs.bigbluebutton.org/development/api#create for options 


## License

MIT (see `LICENSE` file)

[bbb_freeswitch_ipv6]: https://docs.bigbluebutton.org/support/troubleshooting.html#freeswitch-fails-to-bind-to-port-8021
