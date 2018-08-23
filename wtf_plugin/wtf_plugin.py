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
import logging

from wtf_plugin_interface import WTFPluginConfigInterface, WTFPluginInterface
from wtf_request import WTFRequest, WTFAction
from wtf_response import WTFResponse

from time import sleep


class Plugin(object):
    def __init__(self, plugin_interface, **kwargs):
        self._plugin_interface = plugin_interface  # type: WTFPluginInterface
        self._request_map = dict()
        self._action_map = dict()
        self._self_checks_map = dict()
        self._current_request = None
        self._request_lock = False
        self._current_action = None
        self._action_lock = False

        self.config.save_user_config_file()

    def add_request(self, request_name, request_function):
        logging.debug('[PLUGIN] adding request: %s to plugin: %s', request_name, self.id)
        self.requests.set_action_function(request_name, request_function)
        self.request_map[request_name] = request_function

    def add_action(self, action_name, action_function):
        logging.debug('[PLUGIN] adding action: %s to plugin: %s', action_name, self.id)
        self.actions.set_action_function(action_name, action_function)
        self.action_map[action_name] = action_function

    def has_request(self, request_name):
        return request_name in self.request_map.keys()

    def has_action(self, action_name):
        return action_name in self.action_map.keys()

    def call_request(self, request, **kwargs):
        """

        Args:
            request (WTFRequest):
        """
        while self._request_lock:
            sleep(1)
        self._request_lock = True
        self._current_request = request.request_name

        if request.request_name in self.requests.actions.keys():
            response = self.request_map[request.request_name](request)
        else:
            response = WTFResponse(self.id, None, 0, ['request name not found'])

        self._current_request = None
        self._request_lock = False

        return response

    def build_request_response(self, result, success=True, errors=[], notes=[]):
        return WTFResponse(self.id, result, self.config.requests.actions[self._current_request].confidence, errors,
                           notes, self._current_request, success)

    def call_action(self, action, **kwargs):
        """

        Args:
            action (WTFAction):
        """
        while self._action_lock:
            sleep(1)
        self._action_lock = True
        self._current_action = action.request_name

        if action.request_name in self.actions.actions.keys():
            response = self.action_map[action.request_name](action)
        else:
            response = WTFResponse(self.id, None, 0, ['action name not found'])

        self._current_action = None
        self._action_lock = False

        return response

    def build_action_response(self, success, result=None, errors=[], notes=[]):
        return WTFResponse(self.id, result, self.config.actions.actions[self._current_action].confidence, errors,
                           notes, self._current_action, success)

    # TODO(zpriddy): add function for adding self checks

    @property
    def config(self):
        """

        Returns:
            WTFPluginConfigInterface: config interface
        """
        return self._plugin_interface.config

    @property
    def actions(self):
        return self._plugin_interface.actions

    @property
    def requests(self):
        return self._plugin_interface.requests

    @property
    def id(self):
        return self.config.id

    @property
    def request_map(self):
        return self._request_map

    @property
    def action_map(self):
        return self._action_map

    @property
    def self_checks_map(self):
        return self._self_checks_map
