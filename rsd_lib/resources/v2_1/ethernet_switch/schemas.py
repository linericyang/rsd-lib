# Copyright 2018 99cloud, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

vlan_network_interface_req_schema = {
    'type': 'object',
    'properties': {
        'VLANId': {'type': 'number'},
        'VLANEnable': {'type': 'boolean'},
        'Oem': {
            'type': 'object',
            'properties': {
                'Intel_RackScale': {
                    'type': 'object',
                    'properties': {
                        'Tagged': {'type': 'boolean'}
                    },
                    'required': ['Tagged']
                }
            },
            'required': ['Intel_RackScale']
        }
    },
    'required': [
        'VLANId',
        'VLANEnable',
        'Oem'
    ],
    'additionalProperties': False
}
