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


def get_resource_identity(resource):
    if resource is None:
        return None
    else:
        return resource.get('@odata.id', None)


def int_or_none(x):
    """Given a value x it cast as int or None

    :param x: The value to transform and return
    :returns: Either None or x cast to an int

    """
    if x is None:
        return None
    return int(x)
