# Copyright 2017 Intel, Inc.
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

import json
import mock
import testtools

from sushy import exceptions

from rsd_lib.resources.v2_3.node import node


class NodeTestCase(testtools.TestCase):

    def setUp(self):
        super(NodeTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/node.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst = node.Node(
            self.conn, '/redfish/v1/Nodes/Node1',
            redfish_version='1.0.2')

    def test__get_attach_endpoint_action_element(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        value = self.node_inst._get_attach_endpoint_action_element()
        self.assertEqual('/redfish/v1/Nodes/Node1/Actions/'
                         'ComposedNode.AttachResource',
                         value.target_uri)
        self.assertEqual('/redfish/v1/Nodes/Node1/Actions/'
                         'AttachResourceActionInfo',
                         value.action_info_path)
        expected = [
            {
                "name": "Resource",
                "required": True,
                "data_type": "Object",
                "object_data_type": "#Resource.Resource",
                "allowable_values": (
                    "/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",
                )
            },
            {
                "name": "Protocol",
                "required": False,
                "data_type": "String",
                "object_data_type": None,
                "allowable_values": ["NVMeOverFabrics"]
            }
        ]
        self.assertEqual(expected, value.action_info.parameters)

    def test_get_allowed_attach_endpoints(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        expected = self.node_inst.get_allowed_attach_endpoints()
        result = ("/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",)
        self.assertEqual(expected, result)

    def test_attach_endpoint(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst.attach_endpoint(
            resource='/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1',
            protocol='NVMeOverFabrics')
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.AttachResource',
            data={'Resource': {'@odata.id': '/redfish/v1/StorageServices'
                                            '/1-sv-1/Volumes/1-sv-1-vl-1'},
                  'Protocol': 'NVMeOverFabrics'})

    def test_attach_endpoint_only_with_resource_uri(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst.attach_endpoint(
            resource='/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1')
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.AttachResource',
            data={'Resource': {'@odata.id': '/redfish/v1/StorageServices'
                                            '/1-sv-1/Volumes/1-sv-1-vl-1'}})

    def test_attach_endpoint_invalid_parameter(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        with self.assertRaisesRegex(
            exceptions.InvalidParameterValueError,
            '"resource" value.*{0}'.format(
                '/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1')):

            self.node_inst.attach_endpoint(resource='invalid-resource')

    def test__get_detach_endpoint_action_element(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        value = self.node_inst._get_detach_endpoint_action_element()
        self.assertEqual('/redfish/v1/Nodes/Node1/Actions/'
                         'ComposedNode.DetachResource',
                         value.target_uri)
        self.assertEqual('/redfish/v1/Nodes/Node1/Actions/'
                         'DetachResourceActionInfo',
                         value.action_info_path)
        expected = [
            {
                "name": "Resource",
                "required": True,
                "data_type": "Object",
                "object_data_type": "#Resource.Resource",
                "allowable_values": (
                    "/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",
                )
            },
            {
                "name": "Protocol",
                "required": False,
                "data_type": "String",
                "object_data_type": None,
                "allowable_values": ["NVMeOverFabrics"]
            }
        ]
        self.assertEqual(expected, value.action_info.parameters)

    def test_get_allowed_detach_endpoints(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        expected = self.node_inst.get_allowed_detach_endpoints()
        result = ("/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",)
        self.assertEqual(expected, result)

    def test_detach_endpoint(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst.detach_endpoint(
            resource='/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1')
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.DetachResource',
            data={'Resource': {'@odata.id': '/redfish/v1/StorageServices'
                                            '/1-sv-1/Volumes/1-sv-1-vl-1'}})

    def test_detach_endpoint_invalid_parameter(self):
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        with self.assertRaisesRegex(
            exceptions.InvalidParameterValueError,
            '"resource" value.*{0}'.format(
                '/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1')):

            self.node_inst.detach_endpoint(resource='invalid-resource')

    def test_refresh(self):
        self.assertIsNone(self.node_inst._actions.attach_endpoint.action_info)
        self.assertIsNone(self.node_inst._actions.detach_endpoint.action_info)

        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst._get_attach_endpoint_action_element()
        self.node_inst._get_detach_endpoint_action_element()

        self.assertIsNotNone(
            self.node_inst._actions.attach_endpoint.action_info)
        self.assertIsNotNone(
            self.node_inst._actions.detach_endpoint.action_info)

        with open('rsd_lib/tests/unit/json_samples/v2_3/node.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.node_inst.refresh()

        self.assertIsNone(self.node_inst._actions.attach_endpoint.action_info)
        self.assertIsNone(self.node_inst._actions.detach_endpoint.action_info)
