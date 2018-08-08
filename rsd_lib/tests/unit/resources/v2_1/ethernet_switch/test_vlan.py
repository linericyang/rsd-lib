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

import json

import mock
import testtools

from rsd_lib.resources.v2_1.ethernet_switch import vlan


class VLANTestCase(testtools.TestCase):

    def setUp(self):
        super(VLANTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'ethernet_switch_port_vlan.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.vlan_inst = vlan.VLAN(
            self.conn,
            '/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs/VLAN1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.vlan_inst._parse_attributes()
        self.assertEqual('1.0.2', self.vlan_inst.redfish_version)
        self.assertEqual('VLAN1', self.vlan_inst.identity)
        self.assertEqual('VLAN Network Interface', self.vlan_inst.name)
        self.assertEqual('System NIC 1 VLAN', self.vlan_inst.description)
        self.assertEqual(True, self.vlan_inst.vlan_enable)
        self.assertEqual(101, self.vlan_inst.vlan_id)


class VLANCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(VLANCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'ethernet_switch_port_vlan_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
            self.vlan_col = vlan.VLANCollection(
                self.conn,
                '/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs',
                redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.vlan_col._parse_attributes()
        self.assertEqual('1.1.0', self.vlan_col.redfish_version)
        self.assertEqual(
            ('/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs/VLAN1',),
            self.vlan_col.members_identities)

    @mock.patch.object(vlan, 'VLAN', autospec=True)
    def test_get_member(self, mock_vlan):
        self.vlan_col.get_member(
            '/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs/VLAN1')
        mock_vlan.assert_called_once_with(
            self.vlan_col._conn,
            '/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/VLANs/VLAN1',
            redfish_version=self.vlan_col.redfish_version)

    @mock.patch.object(vlan, 'VLAN', autopspec=True)
    def test_get_members(self, mock_vlan):
        members = self.vlan_col.get_members()
        calls = [
            mock.call(self.vlan_col._conn,
                      '/redfish/v1/EthernetSwitches/Switch1/Ports/Port1/'
                      'VLANs/VLAN1',
                      redfish_version=self.vlan_col.redfish_version)
        ]
        mock_vlan.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
