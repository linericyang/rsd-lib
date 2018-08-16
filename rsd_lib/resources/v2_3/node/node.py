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

from rsd_lib.resources.v2_1.node import node as v2_1_node
from rsd_lib.resources.v2_3.node import attach_action_info
from rsd_lib import utils as rsd_lib_utils


class AttachEndpointActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)
    action_info_path = base.Field('@Redfish.ActionInfo',
                                  adapter=rsd_lib_utils.get_resource_identity)
    action_info = None


class DetachEndpointActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)
    action_info_path = base.Field('@Redfish.ActionInfo',
                                  adapter=rsd_lib_utils.get_resource_identity)
    action_info = None


class NodeActionsField(v2_1_node.NodeActionsField):
    attach_endpoint = AttachEndpointActionField('#ComposedNode.AttachResource')
    detach_endpoint = DetachEndpointActionField('#ComposedNode.DetachResource')


class Node(v2_1_node.Node):

    _actions = NodeActionsField('Actions', required=True)

    def _get_attach_endpoint_action_element(self):
        attach_endpoint_action = self._actions.attach_endpoint
        if not attach_endpoint_action:
            raise exceptions.MissingActionError(
                action='#ComposedNode.AttachResource',
                resource=self._path)

        if attach_endpoint_action.action_info is None:
            attach_endpoint_action.action_info = \
                attach_action_info.AttachResourceActionInfo(
                    self._conn, attach_endpoint_action.action_info_path,
                    redfish_version=self.redfish_version)
        return attach_endpoint_action

    def get_allowed_attach_endpoints(self):
        """Get the allowed endpoints for attach action.

        :returns: A set with the allowed attach endpoints.
        """
        attach_action = self._get_attach_endpoint_action_element()
        for i in attach_action.action_info.parameters:
            if i['name'] == 'Resource':
                return i['allowable_values']
        return ()

    def attach_endpoint(self, resource, protocol=None):
        """Attach endpoint from available pool to composed node

        :param resource: Link to endpoint to attach.
        :param protocol: Protocol of the remote drive.
        :raises: InvalidParameterValueError
        """
        attach_action = self._get_attach_endpoint_action_element()
        valid_endpoints = self.get_allowed_attach_endpoints()
        target_uri = attach_action.target_uri

        if resource and resource not in valid_endpoints:
            raise exceptions.InvalidParameterValueError(
                parameter='resource', value=resource,
                valid_values=valid_endpoints)

        data = {}
        if resource is not None:
            data['Resource'] = {'@odata.id': resource}
        if protocol is not None:
            data['Protocol'] = protocol

        self._conn.post(target_uri, data=data)

    def _get_detach_endpoint_action_element(self):
        detach_endpoint_action = self._actions.detach_endpoint
        if not detach_endpoint_action:
            raise exceptions.MissingActionError(
                action='#ComposedNode.DetachResource',
                resource=self._path)

        if detach_endpoint_action.action_info is None:
            detach_endpoint_action.action_info = \
                attach_action_info.AttachResourceActionInfo(
                    self._conn, detach_endpoint_action.action_info_path,
                    redfish_version=self.redfish_version)
        return detach_endpoint_action

    def get_allowed_detach_endpoints(self):
        """Get the allowed endpoints for detach action.

        :returns: A set with the allowed detach endpoints.
        """
        detach_action = self._get_detach_endpoint_action_element()
        for i in detach_action.action_info.parameters:
            if i['name'] == 'Resource':
                return i['allowable_values']
        return ()

    def detach_endpoint(self, resource):
        """Detach endpoint from available pool to composed node

        :param resource: Link to endpoint to detach.
        :raises: InvalidParameterValueError
        """
        detach_action = self._get_detach_endpoint_action_element()
        valid_endpoints = self.get_allowed_detach_endpoints()
        target_uri = detach_action.target_uri

        if resource not in valid_endpoints:
            raise exceptions.InvalidParameterValueError(
                parameter='resource', value=resource,
                valid_values=valid_endpoints)

        data = {}
        if resource is not None:
            data['Resource'] = {'@odata.id': resource}

        self._conn.post(target_uri, data=data)

    def refresh(self):
        super(Node, self).refresh()
        if self._actions.attach_endpoint:
            self._actions.attach_endpoint.action_info = None
        if self._actions.detach_endpoint:
            self._actions.detach_endpoint.action_info = None


class NodeCollection(v2_1_node.NodeCollection):

    @property
    def _resource_type(self):
        return Node

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a NodeCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Node collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(NodeCollection, self).__init__(connector, path, redfish_version)
