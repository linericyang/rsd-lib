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

from sushy.tests.unit import base

from rsd_lib.resources.v2_1.ethernet_switch import ethernet_switch


class TestEthernetSwtich(base.TestCase):

    def setUp(self):
        super(TestEthernetSwtich, self).setUp()
        self.conn = mock.Mock()

        with open('rsd_lib/tests/unit/json_samples/v2_1/ethernet_switch.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.ethernet_switch_inst = ethernet_switch.EthernetSwitch(
            self.conn,
            '/redfish/v1/EthernetSwitches/Switch1',
            redfish_version='1.0.2')

    def test_parse_attributes(self):
        self.ethernet_switch_inst._parse_attributes()
        self.assertEqual('1.0.2', self.ethernet_switch_inst.redfish_version)
        self.assertEqual('Switch1', self.ethernet_switch_inst.identity)
        self.assertEqual('Switch1', self.ethernet_switch_inst.name)
        self.assertEqual('description-as-string',
                         self.ethernet_switch_inst.description)
        self.assertEqual('Quanta', self.ethernet_switch_inst.manufacturer)
        self.assertEqual('ly8_rangley', self.ethernet_switch_inst.model)
        self.assertEqual('02/21/2015 00:00:00',
                         self.ethernet_switch_inst.manufacturing_data)
        self.assertEqual('2M220100SL', self.ethernet_switch_inst.seria_number)
        self.assertEqual('1LY8UZZ0007', self.ethernet_switch_inst.part_number)
        self.assertEqual('ONIE', self.ethernet_switch_inst.firmware_name)
        self.assertEqual('1.1', self.ethernet_switch_inst.firmware_version)
        self.assertEqual('TOR', self.ethernet_switch_inst.role)
        self.assertEqual('Enabled', self.ethernet_switch_inst.status.state)
        self.assertEqual('OK', self.ethernet_switch_inst.status.health)
        self.assertEqual('/redfish/v1/EthernetSwitches/Switch1/ACLs',
                         self.ethernet_switch_inst.acls)
        self.assertEqual('/redfish/v1/EthernetSwitches/Switch1/Ports',
                         self.ethernet_switch_inst.ports)
        self.assertEqual('/redfish/v1/Chassis/FabricModule1',
                         self.ethernet_switch_inst.links.chassis)
        self.assertEqual(('/redfish/v1/EthernetSwitches/Switch1/Ports',),
                         self.ethernet_switch_inst.links.managed_by)


class TestEthernetSwitchCollection(base.TestCase):

    def setUp(self):
        super(TestEthernetSwitchCollection, self).setUp()
        self.conn = mock.Mock()

        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'manager_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.ethernet_switch_col = ethernet_switch.EthernetSwitchCollection(
            self.conn,
            'redfish/v1/EthernetSwitches',
            redfish_version='1.0.2')

    def test_parse_attributes(self):
        self.ethernet_switch_col._parse_attributes()
        self.assertEqual('1.0.2', self.ethernet_switch_col.redfish_version)
        self.assertEqual('Ethernet Switches Collection',
                         self.ethernet_switch_col.name)
        self.assertIn(('/redfish/v1/EthernetSwitches/Switch1',),
                      self.ethernet_switch_col.members_identities)

    @mock.patch.object(ethernet_switch, 'EthernetSwitch', autospec=True)
    def test_get_member(self, mock_ethernet_switch):
        self.manager_col.get_member('/redfish/v1/EthernetSwitches/Switch1')

        mock_ethernet_switch.assert_called_once_with(
            self.ethernet_switch_col._conn,
            '/redfish/v1/EthernetSwitches/Switch1',
            redfish_version=self.ethernet_switch_col.redfish_version
        )

    @mock.patch.object(ethernet_switch, 'EthernetSwitch', autospec=True)
    def test_get_members(self, mock_ethernet_switch):
        members = self.ethernet_switch_col.get_members()
        self.assertEqual(mock_ethernet_switch.call_count, 1)
        self.assertInstance(members, list)
        self.assertEqual(1, len(members))