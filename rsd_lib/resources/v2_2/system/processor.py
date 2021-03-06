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

from sushy.resources import base
from sushy.resources.system import processor
from sushy import utils

from rsd_lib.resources.v2_2.system import processor_metrics


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class Processor(processor.Processor):

    status = StatusField('Status')
    """The processor status"""

    def _get_metrics_path(self):
        """Helper function to find the System process metrics path"""
        return utils.get_sub_resource_path_by(
            self, ['Oem', 'Intel_RackScale', 'Metrics'])

    @property
    @utils.cache_it
    def metrics(self):
        """Property to provide reference to `Metrics` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        return processor_metrics.ProcessorMetrics(
            self._conn, self._get_metrics_path(),
            redfish_version=self.redfish_version)


class ProcessorCollection(processor.ProcessorCollection):

    @property
    def _resource_type(self):
        return Processor
