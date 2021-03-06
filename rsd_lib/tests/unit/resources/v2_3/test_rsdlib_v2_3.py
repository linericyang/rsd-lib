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

import json
import mock
import testtools

from rsd_lib.resources.v2_1.chassis import chassis as v2_1_chassis
from rsd_lib.resources.v2_1.manager import manager as v2_1_manager
from rsd_lib.resources.v2_2.ethernet_switch import ethernet_switch \
    as v2_2_ethernet_switch
from rsd_lib.resources.v2_2.system import system as v2_2_system
from rsd_lib.resources import v2_3
from rsd_lib.resources.v2_3.fabric import fabric as v2_3_fabric
from rsd_lib.resources.v2_3.node import node as v2_3_node
from rsd_lib.resources.v2_3.storage_service import storage_service \
    as v2_3_storage_service


class RSDLibV2_3TestCase(testtools.TestCase):

    def setUp(self):
        super(RSDLibV2_3TestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/root.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.rsd = v2_3.RSDLibV2_3(self.conn)

    def test__parse_attributes(self):
        self.rsd._parse_attributes()
        self.assertEqual("2.3.0", self.rsd._rsd_api_version)
        self.assertEqual("1.1.0", self.rsd._redfish_version)
        self.assertEqual("/redfish/v1/Systems", self.rsd._systems_path)
        self.assertEqual("/redfish/v1/Nodes", self.rsd._nodes_path)
        self.assertEqual("/redfish/v1/Chassis", self.rsd._chassis_path)
        self.assertEqual("/redfish/v1/Fabrics", self.rsd._fabrics_path)
        self.assertEqual("/redfish/v1/StorageServices",
                         self.rsd._storage_service_path)
        self.assertEqual(None, self.rsd._telemetry_service_path)

    @mock.patch.object(v2_2_system, 'SystemCollection', autospec=True)
    def test_get_system_collection(self, mock_system_collection):
        self.rsd.get_system_collection()
        mock_system_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Systems',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_2_system, 'System', autospec=True)
    def test_get_system(self, mock_system):
        self.rsd.get_system('fake-system-id')
        mock_system.assert_called_once_with(
            self.rsd._conn, 'fake-system-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_node, 'NodeCollection', autospec=True)
    def test_get_node_collection(self, mock_node_collection):
        self.rsd.get_node_collection()
        mock_node_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Nodes',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_node, 'Node', autospec=True)
    def test_get_node(self, mock_node):
        self.rsd.get_node('fake-node-id')
        mock_node.assert_called_once_with(
            self.rsd._conn, 'fake-node-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_fabric, 'FabricCollection', autospec=True)
    def test_get_fabric_collection(self, mock_fabric_collection):
        self.rsd.get_fabric_collection()
        mock_fabric_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Fabrics',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_fabric, 'Fabric', autospec=True)
    def test_get_fabric(self, mock_fabric):
        self.rsd.get_fabric('fake-fabric-id')
        mock_fabric.assert_called_once_with(
            self.rsd._conn, 'fake-fabric-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_1_chassis, 'ChassisCollection', autospec=True)
    def test_get_chassis_collection(self, mock_chassis_collection):
        self.rsd.get_chassis_collection()
        mock_chassis_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Chassis',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_1_chassis, 'Chassis', autospec=True)
    def test_get_chassis(self, mock_chassis):
        self.rsd.get_chassis('fake-chassis-id')
        mock_chassis.assert_called_once_with(
            self.rsd._conn, 'fake-chassis-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_storage_service, 'StorageServiceCollection',
                       autospec=True)
    def test_get_storage_service_collection(self,
                                            mock_storage_service_collection):
        self.rsd.get_storage_service_collection()
        mock_storage_service_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/StorageServices',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_3_storage_service, 'StorageService', autospec=True)
    def test_get_storage_service(self, mock_storage_service):
        self.rsd.get_storage_service('fake-storage-service-id')
        mock_storage_service.assert_called_once_with(
            self.rsd._conn, 'fake-storage-service-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_1_manager, 'ManagerCollection', autospec=True)
    def test_get_manager_collection(self, mock_manager_collection):
        self.rsd.get_manager_collection()
        mock_manager_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Managers',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_1_manager, 'Manager', autospec=True)
    def test_get_manager(self, mock_manager_service):
        self.rsd.get_manager('fake-manager-id')
        mock_manager_service.assert_called_once_with(
            self.rsd._conn, 'fake-manager-id',
            redfish_version=self.rsd.redfish_version
        )

    @mock.patch.object(v2_2_ethernet_switch,
                       'EthernetSwitchCollection',
                       autospec=True)
    def test_get_ethernet_switch_collection(self,
                                            mock_ethernet_switch_collection):
        self.rsd.get_ethernet_switch_collection()
        mock_ethernet_switch_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/EthernetSwitches',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(v2_2_ethernet_switch, 'EthernetSwitch', autospec=True)
    def test_get_ethernet_switch(self, mock_ethernet_switch_service):
        self.rsd.get_ethernet_switch('fake-ethernet-switch-id')
        mock_ethernet_switch_service.assert_called_once_with(
            self.rsd._conn, 'fake-ethernet-switch-id',
            redfish_version=self.rsd.redfish_version
        )

    # @mock.patch.object(v2_2_telemetry, 'Telemetry', autospec=True)
    # def test_get_telemetry_service(self, mock_telemetry_service):
    #     self.rsd.get_telemetry_service()
    #     mock_telemetry_service.assert_called_once_with(
    #         self.rsd._conn, '/redfish/v1/TelemetryService',
    #         redfish_version=self.rsd.redfish_version)
