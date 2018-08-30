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

from rsd_lib.resources.v2_1.ethernet_switch import acl_rule


class ACLRuleTestCase(testtools.TestCase):

    def setUp(self):
        super(ACLRuleTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/acl_rule.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.acl_rule_inst = acl_rule.ACLRule(
            self.conn,
            '/redfish/v1/EthernetSwitches/Switch1/ACLs/ACL1/Rules/Rule1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.acl_rule_inst._parse_attributes()
        self.assertEqual('1.0.2', self.acl_rule_inst.redfish_version)
        self.assertEqual('Rule1', self.acl_rule_inst.identity)
        self.assertEqual('Example Rule', self.acl_rule_inst.name)
        self.assertEqual('User defined rule for ACL',
                         self.acl_rule_inst.description)
        self.assertEqual(1, self.acl_rule_inst.rule_id)
        self.assertEqual('Mirror', self.acl_rule_inst.action)
        self.assertEqual('/redfish/v1/EthernetSwitches/Switch1/Ports/Port9',
                         self.acl_rule_inst.forward_mirror_interface)
        self.assertEqual(('/redfish/v1/EthernetSwitches/Switch1/Ports/Port1',
                          '/redfish/v1/EthernetSwitches/Switch1/Ports/Port2',),
                         self.acl_rule_inst.mirror_port_region)
        self.assertEqual('Bidirectional',
                         self.acl_rule_inst.mirror_type)
        self.assertEqual('192.168.1.0',
                         self.acl_rule_inst.condition.ip_source.ipv4_address)
        self.assertEqual('0.0.0.255',
                         self.acl_rule_inst.condition.ip_source.mask)
        self.assertEqual(None, self.acl_rule_inst.condition.ip_destination)
        self.assertEqual('00:11:22:33:44:55',
                         self.acl_rule_inst.condition.mac_source.address)
        self.assertEqual(None, self.acl_rule_inst.condition.mac_source.mask)
        self.assertEqual(1088, self.acl_rule_inst.condition.vlan_id.id)
        self.assertEqual(4095,
                         self.acl_rule_inst.condition.vlan_id.mask)
        self.assertEqual(22,
                         self.acl_rule_inst.condition.l4_source_port.port)
        self.assertEqual(255,
                         self.acl_rule_inst.condition.l4_source_port.mask)
        self.assertEqual(None,
                         self.acl_rule_inst.condition.l4_destination_port)


class ACLRuleCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(ACLRuleCollectionTestCase, self).setUp()
        self.conn = mock.Mock()

        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'acl_rule_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.acl_rule_col = acl_rule.ACLRuleCollection(
            self.conn,
            '/redfish/v1/EthernetSwitches/Switch1/ACLs/ACL1/Rules',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.acl_rule_col._parse_attributes()
        self.assertEqual('1.0.2', self.acl_rule_col.redfish_version)
        self.assertEqual('Ethernet Switch Access Control '
                         'List Rules Collection',
                         self.acl_rule_col.name)
        self.assertEqual(('/redfish/v1/EthernetSwitches/Switch1/ACLs/ACL1/'
                          'Rules/Rule1',),
                         self.acl_rule_col.members_identities)

    @mock.patch.object(acl_rule, 'ACLRule', autospec=True)
    def test_get_member(self, mock_acl_rule):
        self.acl_rule_col.get_member(
            '/redfish/v1/EthernetSwitches/Switch1/ACLs/ACL1/Rules/Rule1')

        mock_acl_rule.assert_called_once_with(
            self.acl_rule_col._conn,
            '/redfish/v1/EthernetSwitches/Switch1/ACLs/ACL1/Rules/Rule1',
            redfish_version=self.acl_rule_col.redfish_version
        )

    @mock.patch.object(acl_rule, 'ACLRule', autospec=True)
    def test_get_members(self, mock_acl_rule):
        members = self.acl_rule_col.get_members()
        self.assertEqual(mock_acl_rule.call_count, 1)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
