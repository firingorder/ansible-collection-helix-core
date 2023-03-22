#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: helix_core_password

short_description: This module will allow you to manage users on Perforce Helix Core

description:
    - "Update Helix server user passwords"

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

seealso:
    - name: Helix Core Password
      description: "Update Helix server user passwords"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_passwd.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


options:
    name:
        description:
            - The name of the user that needs to be managed
        required: true
        type: str
    oldpassword:
        description:
            - The old password to be set for the user that needs to be managed.
            - The old password is only valid if you are changing the logged-in users' password.
            required: false
            type: str
    newpassword:
        description:
            - The new password to be set for the user that needs to be managed.
            required: true
            type: str
    server:
        description:
            - The hostname/ip and port of the server (perforce:1666)
            - Can also use 'P4PORT' environment variable
        required: true
        type: str
        aliases:
            - p4port
    user:
        description:
            - A user with access to create users
            - Can also use 'P4USER' environment variable
        required: true
        type: str
        aliases:
            - p4user
    password:
        description:
            - The user password
            - Can also use 'P4PASSWD' environment variable
        required: true
        type: str
        aliases:
            - p4passwd
    charset:
        default: none
        description:
            - Character set used for translation of unicode files
            - Can also use 'P4CHARSET' environment variable
        required: false
        type: str
        aliases:
            - p4charset
    fingerprint:
        default: none
        description:
            - The SSL fingerprint that matches the one returned from the Perforce server.
        required: false
        type: str
        aliases:
            - p4fingerprint

authors:
    - Luke James (@luke-james)
'''

EXAMPLES = '''
# Modify another user password
- name: Modify a user password
  helix_core_password:
    name: perforce
    newpassword: newpassword123!
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Modify my user password
- name: Modify my user password
  helix_core_password:
    name: perforce
    oldpassword: oldpassword123!
    newpassword: newpassword123!
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect
from socket import gethostname


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True, fallback=(env_fallback, ['P4USER'])),
        oldpassword=dict(type='str', default='', required=False, fallback=(env_fallback, ['P4PASSWD']), no_log=True),
        newpassword=dict(type='str', required=True, no_log=True),
        server=dict(type='str', required=True, aliases=['p4port'], fallback=(env_fallback, ['P4PORT'])),
        user=dict(type='str', required=True, aliases=['p4user'], fallback=(env_fallback, ['P4USER'])),
        password=dict(type='str', required=True, aliases=['p4passwd'], fallback=(env_fallback, ['P4PASSWD']), no_log=True),
        charset=dict(type='str', default='none', aliases=['p4charset'], fallback=(env_fallback, ['P4CHARSET'])),
        fingerprint=dict(type=str, default='', aliases=['p4fingerprint'], fallback=(env_fallback, ["P4FINGERPRINT"]), no_log=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # modify password for a given user
        if module.params['oldpassword'] != '':
            p4.run_password("-O", module.params['oldpassword'], "-P", module.params['newpassword'], module.params['name'])
        else:    
            p4.run_password("-P", module.params['newpassword'], module.params['name'])
        result['changed'] = True

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
