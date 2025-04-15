# Minimal Ansible Playbook Example

Minimal example on how to use the `ebbba.bigbluebutton` role. This is not an
ansible tutorial though, we assume that you [installed ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html) and [know how
to use](https://docs.ansible.com/ansible/latest/getting_started/index.html) it.

* Install dependencies with `ansible-galaxy install -r requirements.yml`. Roles and collections will be installed into `.ansible` instead of your home folder thanks to `ansible.cfg`. This avoids conflicts with other environments and keeps everything local to this directory. You can add more dependencies or change the version (branch, tag or hast) of this role in `requirements.yml` and than re-run the `ansible-galaxy install` command.
* Edit `hosts.yml` and configure your own hosts, groups and vars. Check out the [role documentation](https://github.com/ebbba-org/ansible-role-bigbluebutton) for a list of all possible `bbb_*` vars.
* Make sure your current user can log into all your BBB nodes and has sudo permissions. Run `ansible-play -K install-bigbluebutton.yml` to start your deployment. Good luck!