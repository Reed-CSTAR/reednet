from dataclasses import dataclass
from itertools import chain

import sys, yaml

@dataclass
class User:
    username: str
    name: str

    # Hash of "changeme", a default for new users. Note that since
    # update_password is set to on_create, hashes here will not be accurate to
    # what's actually in the shadow files.
    hashed_password: str = '$y$jD5$wx3m2yO2DXf/AH1oR.b6f/$urFY/uK3kXOpdT.6.Kyw9gsNzYCZzqIG/oZaFsbX2UC'
    shell: str = '/usr/bin/bash'

    def to_conf(self) -> list[map]:
        return [
            {
                'name': f'Synchronize group \'{self.username}\'',
                'become': True,
                'ansible.builtin.group': {
                    'name': self.username,
                    'state': 'present',
                    'system': False
                }
            },
            {
                'name': f'Synchronize user \'{self.username}\'',
                'become': True,
                'ansible.builtin.user': {
                    'append': False,
                    'comment': f'{self.name},,,',
                    'generate_ssh_key': False,
                    'group': f'{self.username}',
                    'groups': ['users'],
                    'name': f'{self.username}',
                    'password': f'{self.hashed_password}',
                    'shell': f'{self.shell}',
                    'state': 'present',
                    'system': False,
                    'update_password': 'on_create'
                }
            }
        ]

def run(users):
    output = list(chain.from_iterable(map(User.to_conf, users)))
    yaml.dump(output, sys.stdout, default_flow_style=False, sort_keys=False)
