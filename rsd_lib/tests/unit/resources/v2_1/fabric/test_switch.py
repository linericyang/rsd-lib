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

from rsd_lib.resources.v2_1.fabric import switch


class SwitchTestCase(testtools.TestCase):

    def setUp(self):
        super(SwitchTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/switch.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.switch_inst = switch.Switch(
            self.conn, '/redfish/v1/Fabrics/PCIe/Switches/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.switch_inst._parse_attributes()
        self.assertEqual('1', self.switch_inst.identity)
        self.assertEqual('PCIe Switch', self.switch_inst.name)
        self.assertEqual('PCIe Switch', self.switch_inst.description)
        self.assertEqual('Enabled', self.switch_inst.status.state)
        self.assertEqual('OK', self.switch_inst.status.health)
        self.assertEqual('OK', self.switch_inst.status.health_rollup)
        self.assertEqual('Manufacturer Name', self.switch_inst.manufacturer)
        self.assertEqual('Model Name', self.switch_inst.model)
        self.assertEqual('SKU', self.switch_inst.sku)
        self.assertEqual('1234567890', self.switch_inst.serial_number)
        self.assertEqual('997', self.switch_inst.part_number)
        self.assertEqual('Customer Asset Tag', self.switch_inst.asset_tag)
        self.assertEqual(1, self.switch_inst.domain_id)
        self.assertEqual(True, self.switch_inst.is_managed)
        self.assertEqual(97, self.switch_inst.total_switch_width)
        self.assertEqual(None, self.switch_inst.indicator_led)
        self.assertEqual('On', self.switch_inst.power_state)
        self.assertEqual('/redfish/v1/Fabrics/PCIe/Switches/1/Ports',
                         self.switch_inst.ports.identity)


class SwitchCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(SwitchCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'switch_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.switch_col = switch.SwitchCollection(
            self.conn, '/redfish/v1/Fabrics/PCIe/Switches',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.switch_col._parse_attributes()
        self.assertEqual('Switch Collection',
                         self.switch_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/Switches/1',),
                         self.switch_col.members_identities)

    @mock.patch.object(switch, 'Switch', autospec=True)
    def test_get_member(self, mock_switch):
        self.switch_col.get_member(
            '/redfish/v1/Fabrics/PCIe/Switches/1')
        mock_switch.assert_called_once_with(
            self.switch_col._conn,
            '/redfish/v1/Fabrics/PCIe/Switches/1',
            redfish_version=self.switch_col.redfish_version)

    @mock.patch.object(switch, 'Switch', autospec=True)
    def test_get_members(self, mock_switch):
        members = self.switch_col.get_members()
        mock_switch.assert_called_with(
            self.switch_col._conn, '/redfish/v1/Fabrics/PCIe/Switches/1',
            redfish_version='1.0.2')
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
