#!/usr/bin/env python3

from dataclasses import dataclass
from itertools import chain

import sys, yaml

@dataclass
class User:
    username: str
    name: str
    hashed_password: str
    shell: str

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
                    'groups': 'users',
                    'name': f'{self.username}',
                    'password': f'{self.hashed_password}',
                    'shell': f'{self.shell}',
                    'state': 'present',
                    'system': False,
                    'update_password': 'on_create'
                }
            }
        ]

USERS: list[User] = [
        User('cgilligan', 'Connor Gilligan', '$6$gRtgcuWcABqI42ce$qQfgk1tf.Ui6X3VvH9OTVclaVHr6PMQX.oNvj2mWbTw.VTsnPvMbmC5bKlzGms1Ns/FUWRRXA/dDHpz..NAEQ/', '/usr/bin/fish'),
        User('doranp', 'Doran Penner', '$6$am88QaRysD4qMGpU$OQd/DnqyqdqepzZh/hGUc4OH2L/XzJ.qgVpj0oAK8gO17I0jAoTmiMvtwJar9U0SNm2UIhAR5t8DKrRt/Tt.a/', '/usr/bin/bash'),
        User('milesc', 'Miles Churchland', '$6$d12j/M9OSkHt.pEB$0d5cY/CbP/b98Xpi58qpofOtdy3vm5avUBiVBYlkWCrH4HS/YGZzW.ZTbiW3OVToge63W0IbSHlzAvOPytRB6/', '/usr/bin/bash'),
        User('mniederman', 'Max Niederman', '$6$YURLZMDLoc8fMaJZ$rCVagSrg.1HL6hibwMxxUQAc5FJf8/1nDj93HGu2nFbXI1f6r1z2OVumYFAAs6hLNTlCuvc6wcx6eTqjMvqBb.', '/usr/bin/bash'),
        User('tristanf', 'Tristan Figueroa-Reid', '$6$5ZETrZ8YpL7eXJZq$nlUUKuc.20TU/hwfuNf9lm2CHH9RZJnVolCDQEUpao7ta3Gi2Mk6T3fV9M2W1hMpK9FGNY6gmdgSw8N0ERT8J0', '/usr/bin/bash'),
        User('araney', 'Aoife Raney', '$6$J.RhfjcRPod4bxGa$hTbEVDzqrdL3ntEcFrMHrcGXpHxxRjE.hr6rR1ylmnNXhGfGUrqOSy3T4YvJtJBM0t2gYZIzxFZ8VULBBWzah/', '/usr/bin/bash'),
        User('yiyuanli', 'Yi Yuanli', '$6$yihWRkzhnthb4LiZ$nFS.c5uGj7SmDDMSQ0cG6asxwfvrTbQ2TvVtjeynYqCa/gEHULIJywMOx61LHI93ac3wj6QneazYuNgjmxmBn.', '/usr/bin/bash'),
        User('atali', 'Tali Auster', '$6$dhsmCbDovRsHoxk5$mvIfD/aq.bFy2e.OGTfyjyDeuNm8OZ4WmTja2ma7VWeoiLnZZaoZ1PeIspi9VojMGJ8guSytcnYRYRC0xX0z2/', '/usr/bin/bash'),
        User('dstewardson', 'Duncan Stewardson', '$6$mJrOZv3CIcA7j0Q5$50i6HXAnmfbf/fbPKBJaInBfnxMXe7kuccHxFIxZd0DqpoTx75PXdkg8NKqI3vsXAzqCUoGSR2WE9J/8vPqrA1', '/usr/bin/bash'),
        User('mbear', 'Michael Bear', '$6$gdvpDeTr9OMvfuk6$684boeZbYQ5NKcaM/IzSq5mJa1ft7Pu1M7zsW8OHiuOtFC3bDGwnVxUBEBNtw8mybDvPgf.vWCYWBIc1GzJ7B0', '/usr/bin/bash'),
        User('paramkapur', 'Param Kapur', '$6$YO8O.Fa1CSGMCdHZ$8/ijuA/aSZ7RMWCwiLWFxvO5kfMk4uZQwuDxXygg6i3B.dWyp7iEgtKvnUtLWzq6JuYltT5kJyI6E2zf39fs00', '/usr/bin/bash'),
        User('bsmith', 'B Smith', '$y$j9T$kH3DkHKI8t6kUHTgz3GpX1$8tMUxobm4xKf4VNnIbNLK/9zIDC.f2ES3iazRs0IQL6', '/usr/bin/bash'),
        User('yyou', 'Franklin You', '$y$jD5$wx3m2yO2DXf/AH1oR.b6f/$urFY/uK3kXOpdT.6.Kyw9gsNzYCZzqIG/oZaFsbX2UC', '/usr/bin/bash'),
        User('lrussell', 'Leland Russell', '$y$jD5$wx3m2yO2DXf/AH1oR.b6f/$urFY/uK3kXOpdT.6.Kyw9gsNzYCZzqIG/oZaFsbX2UC', '/usr/bin/bash')
]

def main():
    output = list(chain.from_iterable(map(User.to_conf, USERS)))
    yaml.dump(output, sys.stdout, default_flow_style=False, sort_keys=False)

if __name__ == '__main__':
    main()
