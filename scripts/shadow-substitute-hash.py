#!/usr/bin/env python3

import argparse, shutil

SHADOW_PATH = '/etc/shadow'

def set_hash(old_shadow, user, hash) -> str:
    new_shadow_path = '/tmp/new_shadow'
    # TODO: perms
    with open(new_shadow_path, 'w') as new_shadow:
        for line in old_shadow:
            if line.startswith(f'{user}:'):
                components = line.split(':')
                components[1] = hash
                line = ':'.join(components)

            new_shadow.write(line)

    return new_shadow_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    parser.add_argument('new_hash')

    args = parser.parse_args()
    user = args.user
    new_hash = args.new_hash

    assert (':' not in user and ':' not in new_hash), 'what the hell'

    with open(SHADOW_PATH, 'r') as f:
        new_shadow = set_hash(f, user, new_hash)
        shutil.move(new_shadow, SHADOW_PATH)
