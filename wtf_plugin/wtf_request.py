#################################################################################
#                                                                               #
# Copyright 2018/08/16 Zachary Priddy (me@zpriddy.com) https://zpriddy.com      #
#                                                                               #
# Licensed under the Apache License, Version 2.0 (the "License");               #
# you may not use this file except in compliance with the License.              #
# You may obtain a copy of the License at                                       #
#                                                                               #
# http://www.apache.org/licenses/LICENSE-2.0                                    #
#                                                                               #
# Unless required by applicable law or agreed to in writing, software           #
# distributed under the License is distributed on an "AS IS" BASIS,             #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.      #
# See the License for the specific language governing permissions and           #
# limitations under the License.                                                #
#                                                                               #
#################################################################################


class WTFRequest(object):
    def __init__(self, request_name, pid=None, **kwargs):
        self._request_name = request_name
        self._pid = pid
        self._kwargs = kwargs

        self.set_kwargs()

    def set_kwargs(self):
        for name, value in self._kwargs.iteritems():
            setattr(self, name, value)

    @property
    def request_name(self):
        return self._request_name

    @property
    def pid(self):
        return self._pid

    @property
    def kwargs(self):
        return self._kwargs


class WTFAction(WTFRequest):
    def __init__(self, action_name, pid=None, **kwargs):
        super(WTFAction, self).__init__(action_name, pid, **kwargs)
