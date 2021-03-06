# Copyright 2018 Intel, Inc.
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

import copy
import json
import jsonschema
import mock
import testtools

from rsd_lib.resources.v2_3.fabric import endpoint
from rsd_lib.tests.unit.fakes import request_fakes


class EndpointTestCase(testtools.TestCase):

    def setUp(self):
        super(EndpointTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/endpoint_1.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.endpoint_inst = endpoint.Endpoint(
            self.conn, '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.endpoint_inst._parse_attributes()
        self.assertEqual('1.0.2', self.endpoint_inst.redfish_version)
        self.assertEqual('Fabric Endpoint',
                         self.endpoint_inst.description)
        self.assertEqual('1', self.endpoint_inst.identity)
        self.assertEqual('Fabric Endpoint', self.endpoint_inst.name)
        self.assertEqual('Target',
                         self.endpoint_inst.connected_entities[0].entity_role)
        self.assertEqual('/redfish/v1/StorageServices/1/Volumes/1',
                         self.endpoint_inst.connected_entities[0].entity_link)
        self.assertEqual('Enabled', self.endpoint_inst.status.state)
        self.assertEqual('OK', self.endpoint_inst.status.health)
        self.assertEqual('OK', self.endpoint_inst.status.health_rollup)
        self.assertEqual('NVMeOverFabrics', self.endpoint_inst.protocol)
        self.assertEqual('NQN',
                         self.endpoint_inst.identifiers[0].name_format)
        self.assertEqual('nqn.2014-08.org.nvmexpress:NVMf:uuid:'
                         '397f9b78-7e94-11e7-9ea4-001e67dfa170',
                         self.endpoint_inst.identifiers[0].name)
        self.assertEqual('UUID',
                         self.endpoint_inst.identifiers[1].name_format)
        self.assertEqual('397f9b78-7e94-11e7-9ea4-001e67dfa170',
                         self.endpoint_inst.identifiers[1].name)
        self.assertEqual((), self.endpoint_inst.links.ports)
        self.assertEqual((), self.endpoint_inst.links.endpoints)
        self.assertEqual(('/redfish/v1/Fabrics/NVMeoE/Zones/1',),
                         self.endpoint_inst.links.zones)
        self.assertEqual('/redfish/v1/Systems/Target/EthernetInterfaces/1',
                         self.endpoint_inst.links.interface)
        self.assertEqual(
            'RoCEv2',
            self.endpoint_inst.ip_transport_details[0].transport_protocol)
        self.assertEqual(
            '192.168.0.10',
            self.endpoint_inst.ip_transport_details[0].ipv4_address)
        self.assertEqual(
            None, self.endpoint_inst.ip_transport_details[0].ipv6_address)
        self.assertEqual(1023, self.endpoint_inst.ip_transport_details[0].port)
        self.assertEqual(None, self.endpoint_inst.oem.authentication)

        with open('rsd_lib/tests/unit/json_samples/v2_3/endpoint_2.json',
                  'r') as f:
            self.endpoint_inst._json = json.loads(f.read())

        self.endpoint_inst._parse_attributes()
        self.assertEqual('1.0.2', self.endpoint_inst.redfish_version)
        self.assertEqual('Fabric Initiator Endpoint',
                         self.endpoint_inst.description)
        self.assertEqual('1', self.endpoint_inst.identity)
        self.assertEqual('Fabric Endpoint', self.endpoint_inst.name)
        self.assertEqual('Initiator',
                         self.endpoint_inst.connected_entities[0].entity_role)
        self.assertEqual(None,
                         self.endpoint_inst.connected_entities[0].entity_link)
        self.assertEqual(None, self.endpoint_inst.status.state)
        self.assertEqual(None, self.endpoint_inst.status.health)
        self.assertEqual(None, self.endpoint_inst.status.health_rollup)
        self.assertEqual('NVMeOverFabrics', self.endpoint_inst.protocol)
        self.assertEqual('NQN',
                         self.endpoint_inst.identifiers[0].name_format)
        self.assertEqual('nqn.2014-08.org.nvmexpress:NVMf:uuid:'
                         '12345678-90ab-cdef-0000-000000000000',
                         self.endpoint_inst.identifiers[0].name)
        self.assertEqual('UUID',
                         self.endpoint_inst.identifiers[1].name_format)
        self.assertEqual('12345678-90ab-cdef-0000-000000000000',
                         self.endpoint_inst.identifiers[1].name)
        self.assertEqual((), self.endpoint_inst.links.ports)
        self.assertEqual((), self.endpoint_inst.links.endpoints)
        self.assertEqual(('/redfish/v1/Fabrics/NVMeoE/Zones/1',),
                         self.endpoint_inst.links.zones)
        self.assertEqual(None, self.endpoint_inst.links.interface)
        self.assertEqual(
            'RoCEv2',
            self.endpoint_inst.ip_transport_details[0].transport_protocol)
        self.assertEqual(
            '192.168.0.10',
            self.endpoint_inst.ip_transport_details[0].ipv4_address)
        self.assertEqual(
            None, self.endpoint_inst.ip_transport_details[0].ipv6_address)
        self.assertEqual(4791, self.endpoint_inst.ip_transport_details[0].port)
        self.assertEqual(None, self.endpoint_inst.oem.authentication)

    def test_update_authentication(self):
        self.endpoint_inst.update_authentication(username='fake-username')
        self.endpoint_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
            data={
                "Oem": {
                    "Intel_RackScale": {
                        "@odata.type": "#Intel.Oem.Endpoint",
                        "Authentication": {"Username": "fake-username"}
                    }
                }
            })

        self.endpoint_inst._conn.patch.reset_mock()
        self.endpoint_inst.update_authentication(password='fake-password')
        self.endpoint_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
            data={
                "Oem": {
                    "Intel_RackScale": {
                        "@odata.type": "#Intel.Oem.Endpoint",
                        "Authentication": {"Password": "fake-password"}
                    }
                }
            })

        self.endpoint_inst._conn.patch.reset_mock()
        self.endpoint_inst.update_authentication(username='fake-username',
                                                 password='fake-password')
        self.endpoint_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
            data={
                "Oem": {
                    "Intel_RackScale": {
                        "@odata.type": "#Intel.Oem.Endpoint",
                        "Authentication": {
                            "Username": "fake-username",
                            "Password": "fake-password"
                        }
                    }
                }
            })

    def test_update_authentication_with_invalid_parameter(self):
        with self.assertRaisesRegex(
            ValueError,
            'At least "username" or "password" parameter has to be specified'):
            self.endpoint_inst.update_authentication()


class EndpointCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(EndpointCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'endpoint_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.conn.post.return_value = request_fakes.fake_request_post(
            None, headers={"Location": "https://localhost:8443/redfish/v1/"
                                       "Fabrics/NVMeoE/Endpoints/3"})

        self.endpoint_col = endpoint.EndpointCollection(
            self.conn, '/redfish/v1/Fabrics/NVMeoE/Endpoints',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.endpoint_col._parse_attributes()
        self.assertEqual('1.0.2', self.endpoint_col.redfish_version)
        self.assertEqual('Endpoint Collection',
                         self.endpoint_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
                          '/redfish/v1/Fabrics/NVMeoE/Endpoints/2'),
                         self.endpoint_col.members_identities)

    @mock.patch.object(endpoint, 'Endpoint', autospec=True)
    def test_get_member(self, mock_endpoint):
        self.endpoint_col.get_member(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints/1')
        mock_endpoint.assert_called_once_with(
            self.endpoint_col._conn,
            '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
            redfish_version=self.endpoint_col.redfish_version)

    @mock.patch.object(endpoint, 'Endpoint', autospec=True)
    def test_get_members(self, mock_endpoint):
        members = self.endpoint_col.get_members()
        calls = [
            mock.call(self.endpoint_col._conn,
                      '/redfish/v1/Fabrics/NVMeoE/Endpoints/1',
                      redfish_version=self.endpoint_col.redfish_version),
            mock.call(self.endpoint_col._conn,
                      '/redfish/v1/Fabrics/NVMeoE/Endpoints/2',
                      redfish_version=self.endpoint_col.redfish_version)
        ]
        mock_endpoint.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))

    def test_create_endpoint(self):
        reqs = {
            "EndpointProtocol": "NVMeOverFabrics",
            "Identifiers": [
                {
                    "DurableNameFormat": "NQN",
                    "DurableName": "nqn.2014-08.org.nvmexpress:NVMf:"
                                   "uuid:397f9b78-7e94-11e7-9ea4-001e67dfa170"
                }
            ],
            "ConnectedEntities": [
                {
                    "EntityLink": {
                        "@odata.id": "/redfish/v1/StorageServices/1/Volumes/1"
                    },
                    "EntityRole": "Target"
                }
            ],
            "Links": {
                "Oem": {
                    "Intel_RackScale": {
                        "Interfaces": [
                            {
                                "@odata.id": "/redfish/v1/Systems/Target/"
                                             "EthernetInterfaces/1"
                            }
                        ]
                    }
                }
            }
        }
        result = self.endpoint_col.create_endpoint(
            identifiers=[
                {
                    "DurableNameFormat": "NQN",
                    "DurableName": "nqn.2014-08.org.nvmexpress:NVMf:"
                                   "uuid:397f9b78-7e94-11e7-9ea4-001e67dfa170"
                }
            ],
            connected_entities=[
                {
                    "EntityLink": {
                        "@odata.id": "/redfish/v1/StorageServices/1/Volumes/1"
                    },
                    "EntityRole": "Target"
                }
            ],
            protocol="NVMeOverFabrics",
            interface="/redfish/v1/Systems/Target/EthernetInterfaces/1")
        self.endpoint_col._conn.post.assert_called_once_with(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints', data=reqs)
        self.assertEqual(result,
                         '/redfish/v1/Fabrics/NVMeoE/Endpoints/3')

        self.endpoint_col._conn.post.reset_mock()
        reqs = {
            "EndpointProtocol": "iSCSI",
            "Identifiers": [
                {
                    "DurableNameFormat": "iQN",
                    "DurableName": "iqn.1986-03.com.intel:my_storage-uuid:"
                                   "397f9b78-7e94-11e7-9ea4-001e67dfa170"
                }
            ],
            "ConnectedEntities": [
                {
                    "EntityLink": {
                        "@odata.id": "/redfish/v1/StorageServices/1/Volumes/1"
                    },
                    "EntityRole": "Target",
                    "Identifiers": [
                        {
                            "DurableNameFormat": "LUN",
                            "DurableName": "1"
                        }
                    ]
                }
            ],
            "Oem": {
                "Intel_RackScale": {
                    "Authentication": {
                        "Username": "userA",
                        "Password": "passB"
                    }
                }
            }
        }
        result = self.endpoint_col.create_endpoint(
            identifiers=[
                {
                    "DurableNameFormat": "iQN",
                    "DurableName": "iqn.1986-03.com.intel:my_storage-uuid:"
                                   "397f9b78-7e94-11e7-9ea4-001e67dfa170"
                }
            ],
            connected_entities=[
                {
                    "EntityLink": {
                        "@odata.id": "/redfish/v1/StorageServices/1/Volumes/1"
                    },
                    "EntityRole": "Target",
                    "Identifiers": [
                        {
                            "DurableNameFormat": "LUN",
                            "DurableName": "1"
                        }
                    ]
                }
            ],
            protocol="iSCSI",
            authentication={
                "Username": "userA",
                "Password": "passB"
            })
        self.endpoint_col._conn.post.assert_called_once_with(
            '/redfish/v1/Fabrics/NVMeoE/Endpoints', data=reqs)
        self.assertEqual(result,
                         '/redfish/v1/Fabrics/NVMeoE/Endpoints/3')

    def test_create_endpoint_with_invalid_reqs(self):
        identifiers = [
            {
                "DurableNameFormat": "iQN",
                "DurableName": "iqn.1986-03.com.intel:my_storage-uuid:"
                               "397f9b78-7e94-11e7-9ea4-001e67dfa170"
            }
        ]
        connected_entities = [
            {
                "EntityLink": {
                    "@odata.id": "/redfish/v1/StorageServices/1/Volumes/1"
                },
                "EntityRole": "Target",
                "Identifiers": [
                    {
                        "DurableNameFormat": "LUN",
                        "DurableName": "1"
                    }
                ]
            }
        ]

        result = self.endpoint_col.create_endpoint(
            identifiers=identifiers, connected_entities=connected_entities)
        self.assertEqual(result,
                         '/redfish/v1/Fabrics/NVMeoE/Endpoints/3')

        # Test invalid identifiers argument
        invalid_identifiers = copy.deepcopy(identifiers)
        invalid_identifiers[0]['DurableNameFormat'] = 'fake-format'
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=invalid_identifiers,
                          connected_entities=connected_entities)

        invalid_identifiers = copy.deepcopy(identifiers)
        invalid_identifiers[0].pop('DurableNameFormat')
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=invalid_identifiers,
                          connected_entities=connected_entities)

        invalid_identifiers = copy.deepcopy(identifiers)
        invalid_identifiers[0].pop('DurableName')
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=invalid_identifiers,
                          connected_entities=connected_entities)

        invalid_identifiers = copy.deepcopy(identifiers)
        invalid_identifiers[0]['invalid_key'] = 'invalid_value'
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=invalid_identifiers,
                          connected_entities=connected_entities)

        # Test invalid connected_entities argument
        invalid_connected_entities = copy.deepcopy(connected_entities)
        invalid_connected_entities[0]['EntityRole'] = 'fake-format'
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=invalid_connected_entities)

        invalid_connected_entities = copy.deepcopy(connected_entities)
        invalid_connected_entities[0]['EntityLink'].pop('@odata.id')
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=invalid_connected_entities)

        invalid_connected_entities = copy.deepcopy(connected_entities)
        invalid_connected_entities[0].pop('EntityLink')
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=invalid_connected_entities)

        invalid_connected_entities = copy.deepcopy(connected_entities)
        invalid_connected_entities[0].pop('EntityRole')
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=invalid_connected_entities)

        invalid_connected_entities = copy.deepcopy(connected_entities)
        invalid_connected_entities[0]['invalid_key'] = 'invalid_value'
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=invalid_connected_entities)

        # Test invalid protocol argument
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=connected_entities,
                          protocol='invalid_potocol')

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=connected_entities,
                          protocol=1)

        # Test invalid interface argument
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=connected_entities,
                          interface=1)

        # Test invalid authentication argument
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          self.endpoint_col.create_endpoint,
                          identifiers=identifiers,
                          connected_entities=connected_entities,
                          authentication={'invalid_key': 'invalid_value'})
