#!/usr/bin/env python3

from datetime import datetime
import yaml
import os, time, random

def process_shadow(line: str) -> dict:
    line = line.split(':')

    if len(line) < 2: return {}
    if not line[0]: return {}

    username = line[0]
    password = line[1]

    if not username or not password \
            or password == '!' \
            or password == '*' \
            or password == '!*': return {}

    return {
        username: {
            'disabled': False,
            'displayname': username,
            'password': password,
            'email': f'{username}@reed.edu',
        }
    }

def write_users_yaml(users: dict):
    def inner():
        with open('/var/lib/authelia/users.yml', 'x') as f:
            yaml.dump(users, f)

    try: inner()
    except FileExistsError as e: 
        ts = datetime.now().isoformat()
        print(f'Renaming existing conf to /var/lib/authelia/users.yml-{ts}')
        os.rename('/var/lib/authelia/users.yml', f'/var/lib/authelia/users-{ts}.yml')
        inner()


def jitter_retry(n, f, *args, **kwargs):
    if n == 0: return
    try:
        return f(*args, **kwargs)
    except Exception as e:
        delay = random.randint(3, 30)
        print(f'Retrying after {delay}s: {e}')
        time.sleep(delay)
        jitter_retry(n - 1, f, *args, **kwargs)


if __name__ == '__main__':
    users = dict()
    with open('/etc/shadow') as shadow:
        for line in shadow:
            users.update(process_shadow(line))

    jitter_retry(3, write_users_yaml, {'users': users})
