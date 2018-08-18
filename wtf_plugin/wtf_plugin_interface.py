################################################################################# 
#                                                                               #
# Copyright 2018/08/17 Zachary Priddy (me@zpriddy.com) https://zpriddy.com      #
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
import json
from os.path import join

from typing import Any, Tuple

from wtf_action import WTFActions, WTFActionConfig
from wtf_params import WTFParams, WTFParam

import logging


class WTFPluginInterface(object):
    def __init__(self, plugin_config):
        self._plugin_config = WTFPluginConfigInterface(**plugin_config)
        self._plugin_actions = WTFActionsInterface(self.config.actions)
        self._plugin_requests = WTFActionsInterface(self.config.requests)



    def read_user_config_file(self, config_folder='config'):
        self.config.read_user_config_file(config_folder)
        self._plugin_actions = WTFActionsInterface(self.config.actions)
        self._plugin_requests = WTFActionsInterface(self.config.requests)

    @property
    def config(self):
        return self._plugin_config

    @property
    def actions(self):
        return self._plugin_actions

    @property
    def requests(self):
        return self._plugin_requests


class WTFActionsInterface(object):
    def __init__(self, actions):
        """

        Args:
            actions (WTFActions):
        """
        self._actions = dict()
        for action_name, action in actions.actions.iteritems():
            self._actions[action_name] = WTFActionInterface(action)


    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if item in self._actions:
            return self._actions[item]
        raise AttributeError("module {__name__!r} has no attribute {item!r}")


    @property
    def actions(self):
        return self._actions

    @property
    def enabled_actions(self):
        enabled_actions = list()
        for action_name, action in self.actions.iteritems():
            if action.enabled:
                enabled_actions.append(action_name)
        return enabled_actions

    def set_action_function(self, action_name, function):
        self.__getattr__(action_name).set_function(function)


class WTFActionInterface(WTFActionConfig):
    def __init__(self, action, **kwargs):
        """

        Args:
            action (WTFActionConfig):
        """
        print(action.export())
        super(WTFActionInterface, self).__init__(**action.export_for_action_import())
        self._function = None

    def set_function(self, function):
        self._function = function

    #TODO(zpriddy): Get param default values, updated with values passed in, and check for required inputs


    def get_default_params(self):
        params = dict()
        for name, param in self.params.params.iteritems():
            params[name] = param.default
        return params

    def verify_params(self, **kwargs):
        default_params = self.get_default_params()
        for name in default_params:
            if self.params.params[name].required:
                if name not in kwargs:
                    logging.fatal('missing required action param: %s', name)
        default_params.update(**kwargs)
        return default_params

    def call(self, **kwargs):
        if not self.enabled:
            logging.fatal('action: %s is not enabled', self.name)
            return
        params = self.verify_params(**kwargs)
        return self.function(**params)

    @property
    def function(self):
        return self._function


class WTFPluginConfigInterface(object):
    def __init__(self, pid, context, package, config_file, enabled=False, config={}, actions={}, requests={}, **kwargs):
        """

        Args:
            pid:
            context:
            package:
            config_file:
            config: json string of config params
            **kwargs:
        """
        # type: (object, str, str, str, str, dict, dict) -> None
        self._pid = pid
        self._context = context
        self._package = package
        self._config_file = config_file
        self._config = WTFParams(config)
        self._enabled = enabled
        self._actions = WTFActions(actions)
        self._actions_json = actions
        self._requests = WTFActions(requests)
        self._requests_json = requests

        for config_name, config_param in self._config.params.iteritems():  # type: Tuple[str, WTFParam]
            setattr(self, '__' + config_name, WTFParamInterface(config_param))

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if '__'+item not in self.__dict__:
            raise AttributeError("module {__name__!r} has no attribute {item!r}")
        if type(self.__dict__['__' + item]) is WTFParamInterface:
            return self.__dict__['__' + item].value
        return self.__dict__['__' + item]

    def read_user_config_file(self, config_folder='config'):
        with open(join(config_folder, self._config_file)) as user_config:
            user_json = json.load(user_config)
            for param_name, param_vaue in user_json.iteritems():
                if param_name not in ['enabled', 'actions', 'requests']:
                    self.set_value(param_name, param_vaue)
                if param_name == 'enabled':
                    self._enabled = param_vaue
                if param_name == 'actions':
                    self._actions_json = param_vaue
                    self._actions = WTFActions(self._actions_json)
                if param_name == 'requests':
                    self._requests_json = param_vaue
                    self._requests = WTFActions(self._requests_json)

    def save_user_config_file(self, config_folder='config'):
        with open(join(config_folder, self._config_file), 'w') as user_config:
            config_output = dict()
            for key, value in self.__dict__.items():
                if key.startswith('__'):
                    config_output[key[2:]] = value.value
            config_output['actions'] = self.actions.export()
            config_output['requests'] = self.requests.export()
            config_output['enabled'] = self.enabled
            print(config_output)
            json.dump(config_output,user_config, indent=4,sort_keys=True)


    def set_value(self, param_name, value):
        param = getattr(self, '__' + param_name)
        param.set_value(value)

    @property
    def enabled(self):
        return self._enabled

    @property
    def package(self):
        return self._package

    @property
    def id(self):
        return self._pid

    @property
    def actions(self):
        return self._actions

    @property
    def requests(self):
        return self._requests


class WTFParamInterface(object):
    def __init__(self, param, value=None):
        # type: (WTFParam, Any) -> None
        self._param = param
        self._value = None

        self.set_value(value)

    def set_value(self, value):
        if not value and self.param.default_init:
            self.value = self.param.default
        else:
            self.value = value

    @property
    def param(self):
        return self._param

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
