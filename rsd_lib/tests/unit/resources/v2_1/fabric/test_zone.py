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

from rsd_lib.resources.v2_1.fabric import zone


class ZoneTestCase(testtools.TestCase):

    def setUp(self):
        super(ZoneTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/zone.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.zone_inst = zone.Zone(
            self.conn, '/redfish/v1/Fabrics/PCIe/Zones/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.zone_inst._parse_attributes()
        self.assertEqual('1.0.2', self.zone_inst.redfish_version)
        self.assertEqual('PCIe Zone 1',
                         self.zone_inst.description)
        self.assertEqual('1', self.zone_inst.identity)
        self.assertEqual('PCIe Zone 1', self.zone_inst.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/'
                          'Endpoints/HostRootComplex1',
                          '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF2'),
                         self.zone_inst.links.endpoint_identities)
        self.assertEqual('Enabled', self.zone_inst.status.state)
        self.assertEqual('OK', self.zone_inst.status.health)

    def test_endpoints(self):
        # check for the underneath variable value
        self.assertIsNone(self.zone_inst._endpoints)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'endpoint.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_endpoints = self.zone_inst.endpoints
        # | THEN |
        self.assertEqual('NVMeDrivePF1', actual_endpoints[0].identity)
        self.assertEqual(2, len(actual_endpoints))
        self.conn.get.return_value.json.assert_called_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_endpoints,
                      self.zone_inst.endpoints)
        self.conn.get.return_value.json.assert_not_called()

    def test_endpoints_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'endpoint.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertEqual('NVMeDrivePF1', self.zone_inst.endpoints[0].identity)
        self.assertEqual(2, len(self.zone_inst.endpoints))

        # On refreshing the fabric instance...
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'zone.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.zone_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.zone_inst._endpoints)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'endpoint.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertEqual('NVMeDrivePF1', self.zone_inst.endpoints[0].identity)
        self.assertEqual(2, len(self.zone_inst.endpoints))

    def test_update(self):
        self.zone_inst.update(
            ['/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF1'])
        self.zone_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Fabrics/PCIe/Zones/1',
            data={"Endpoints": [{"@odata.id": "/redfish/v1/Fabrics/PCIe/"
                                              "Endpoints/NVMeDrivePF1"}]})

        self.zone_inst._conn.patch.reset_mock()
        self.zone_inst.update(
            ['/redfish/v1/Fabrics/PCIe/Endpoints/HostRootComplex1',
             '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF2'])
        self.zone_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Fabrics/PCIe/Zones/1',
            data={"Endpoints":
                  [{"@odata.id": "/redfish/v1/Fabrics/PCIe/Endpoints/"
                                 "HostRootComplex1"},
                   {"@odata.id": "/redfish/v1/Fabrics/PCIe/Endpoints/"
                                 "NVMeDrivePF2"}]})


class ZoneCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(ZoneCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'zone_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.zone_col = zone.ZoneCollection(
            self.conn, '/redfish/v1/Fabrics/PCIe/Zones',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.zone_col._parse_attributes()
        self.assertEqual('1.0.2', self.zone_col.redfish_version)
        self.assertEqual('PCIe Zone Collection',
                         self.zone_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/Zones/1',
                          '/redfish/v1/Fabrics/PCIe/Zones/2'),
                         self.zone_col.members_identities)

    @mock.patch.object(zone, 'Zone', autospec=True)
    def test_get_member(self, mock_zone):
        self.zone_col.get_member('/redfish/v1/Fabrics/PCIe/Zones/1')
        mock_zone.assert_called_once_with(
            self.zone_col._conn, '/redfish/v1/Fabrics/PCIe/Zones/1',
            redfish_version=self.zone_col.redfish_version)

    @mock.patch.object(zone, 'Zone', autospec=True)
    def test_get_members(self, mock_zone):
        members = self.zone_col.get_members()
        mock_zone.assert_called_with(
            self.zone_col._conn, '/redfish/v1/Fabrics/PCIe/Zones/2',
            redfish_version=self.zone_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
