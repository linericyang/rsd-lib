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
from sushy import utils

from rsd_lib.resources.v2_2.telemetry.metric_definitions \
    import metric_definitions


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')


class Telemetry(base.ResourceBase):

    status = StatusField('Status')
    """The telemetry service status"""

    def _get_metric_definitions_path(self):
        """Helper function to find the metric definitions path"""
        return utils.get_sub_resource_path_by(self, 'MetricDefinitions')

    @property
    @utils.cache_it
    def metric_definitions(self):
        """Property to provide reference to `MetricDefinitions` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        return metric_definitions.MetricDefinitionsCollection(
            self._conn, self._get_metric_definitions_path(),
            redfish_version=self.redfish_version)
