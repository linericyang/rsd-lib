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

from sushy import exceptions
from sushy.resources import base

from rsd_lib.resources.v2_1.ethernet_switch import port as v2_1_port
from rsd_lib.resources.v2_2.ethernet_switch import port_metrics

from rsd_lib import utils


class Port(v2_1_port.Port):

    _metrics = None  # ref to Port metrics instance

    def _get_metrics_path(self):
        """Helper function to find the Port metrics path"""
        metrics = self.json.get('Metrics')
        if not metrics:
            raise exceptions.MissingAttributeError(attribute='Metrics',
                                                   resource=self._path)
        return utils.get_resource_identity(metrics)

    @property
    def metrics(self):
        """Property to provide reference to `Metrics` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._metrics is None:
            self._metrics = port_metrics.PortMetrics(
                self._conn, self._get_metrics_path(),
                redfish_version=self.redfish_version)

        return self._metrics

    def refresh(self):
        super(Port, self).refresh()
        self._metrics = None


class PortCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Port

    def __init__(self, connector, path, redfish_version=None):
        """A class representing an Port

        :param connector: A Connector instance
        :param path: The canonical path to the Port collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PortCollection, self).__init__(connector, path, redfish_version)
