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

from typing import Dict, Tuple

from const import ACTION_CONTEXT, ACTION_ENABLED, ACTION_PARAMS
from wtf_params import WTFParam, WTFParams


class WTFActions(object):
    def __init__(self, actions_json):
        self._actions_json = actions_json  # type: dict
        self._actions = dict()  # type: Dict[str, WTFActionConfig]

        self.import_actions()

    def __dict__(self):
        output = dict()
        for action_name, action in self._actions.iteritems():  # type: Tuple[str, WTFActionConfig]
            output.update(action.export())
        return output

    def export(self):
        return self.__dict__()

    def import_actions(self):
        for action_name, action in self._actions_json.iteritems():  # type: Tuple[str, WTFActionConfig]
            self._actions[action_name] = WTFActionConfig(action_name, **action)

    @property
    def actions(self):
        return self._actions


class WTFActionConfig(object):
    def __init__(self, action_name, context, enabled=True, params=None, **kwargs):
        """
        Args:
            action_name: (string) The name of the action
            context: (string) Description of the action
            enabled: (bool) Is this action enabled
            params: (dict) JSON representation of the input params in WTFParams format
            **kwargs:
        """
        self._action_name = action_name
        self._context = context
        self._enabled = enabled  # type: bool
        self._json_params = params  # type: dict
        self._params = None  # type: WTFParams

        self.import_params()

    def import_params(self):
        self._params = WTFParams(self._json_params)

    def add_param(self, param):
        """ Add a param to the action params.

        Args:
            param (WTFParam): param to add
        """
        self._params[param.param_key] = param

    def add_json_param(self, json_param):
        """ Add a param to the action params from JSON format.

        Args:
            json_param (dict): JSON representation of param to add
        """
        if len(json_param.keys()) != 1:
            logging.error('[WTFAction] JSON param has wrong number of keys')
            return

        param = WTFParam(json_param.keys()[0])
        self._params[param.param_key] = param

    def __dict__(self):
        return {
            self.name: {
                ACTION_CONTEXT: self.context,
                ACTION_ENABLED: self.enabled,
                ACTION_PARAMS:  self.params.export()
            }
        }

    def export(self):
        return self.__dict__()

    def export_for_action_import(self):
        return {
            'action_name': self.name,
            'context':     self.context,
            'enabled':     self.enabled,
            'params':      self.params.export()
        }

    @property
    def name(self):
        return self._action_name

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def context(self):
        return self._context

    @property
    def params(self):
        return self._params
