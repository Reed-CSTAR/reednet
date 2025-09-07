#!/usr/bin/env python3

import os, shutil, subprocess

import inotify.adapters, inotify.constants

MACHINES = [ # TODO: read from inventory.yaml
        'patty.reed.edu', 'peggy.reed.edu', 'polly.reed.edu',
        'banku.reed.edu', 'empanada.reed.edu', 'gyoza.reed.edu', 'pierogi.reed.edu'
]

def read_shadow(path) -> set:
    users = set()
    with open(path, 'r') as shadow:
        for line in shadow:
            if line.startswith('#'): continue

            components = line.split(':')
            if len(components) < 2: continue

            username = components[0]
            password = components[1]
            if not username or not password \
                    or password == '!' \
                    or password == '*' \
                    or password == '!*': continue

            users.add((username, password))

    return users

def send_shadow(shadow):
    for user, password in shadow:
        for machine in MACHINES:
            # Don't update ourself. This would cause an inotify event and a constant, infinite loop.
            if machine == 'polly.reed.edu': continue

            print(f'Updating {user}:{password} on {machine}.')
            try:
                assert '\'' not in user and '\'' not in password, 'i will drop kick you personally (if this is triggered, sanitize properly)'
                subprocess.run(
                    ['ssh', machine, 'poly-shadow-substitute-hash', f'\'{user}\'', f'\'{password}\''])
            except Exception as e:
                print(f'Failed: {e}')

if __name__ == '__main__':
    i = inotify.adapters.Inotify()
    i.add_watch('/etc', mask=inotify.constants.IN_MOVED_TO)

    shutil.copy('/etc/shadow', '/tmp/old-shadow')
    shadow = read_shadow('/tmp/old-shadow')
    os.remove('/tmp/old-shadow')

    send_shadow(shadow)

    for event in i.event_gen(yield_nones=False):
        if event[3] != 'shadow': pass
        shadow = read_shadow('/etc/shadow')
        send_shadow(shadow)

        print('Updating users.yml.')
        subprocess.run(['poly-authelia-users-from-shadow'])
