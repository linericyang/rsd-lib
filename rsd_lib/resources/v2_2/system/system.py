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

from sushy import utils

from rsd_lib.resources.v2_1.system import system
from rsd_lib.resources.v2_2.system import memory
from rsd_lib.resources.v2_2.system import metrics
from rsd_lib.resources.v2_2.system import processor


class System(system.System):

    def _get_metrics_path(self):
        """Helper function to find the System metrics path"""
        return utils.get_sub_resource_path_by(
            self, ['Oem', 'Intel_RackScale', 'Metrics'])

    @property
    @utils.cache_it
    def metrics(self):
        """Property to provide reference to `Metrics` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        return metrics.Metrics(
            self._conn, self._get_metrics_path(),
            redfish_version=self.redfish_version)

    @property
    @utils.cache_it
    def processors(self):
        """Property to provide reference to `ProcessorCollection` instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        return processor.ProcessorCollection(
            self._conn, self._get_processor_collection_path(),
            redfish_version=self.redfish_version)

        return self._processors

    @property
    @utils.cache_it
    def memory(self):
        """Property to provide reference to `Memory` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        return memory.MemoryCollection(
            self._conn, self._get_memory_collection_path(),
            redfish_version=self.redfish_version)


class SystemCollection(system.SystemCollection):

    @property
    def _resource_type(self):
        return System
