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

from typing import Any, Tuple

from wtf_action import WTFActions
from wtf_params import WTFParams, WTFParam

from os.path import join


class WTFPluginInterface(object):
    def __init__(self, plugin_config):
        self._plugin_config = WTFPluginConfigInterface(**plugin_config)

    @property
    def config(self):
        return self._plugin_config


class WTFPluginConfigInterface(object):
    def __init__(self, pid, context, package, config_file, enabled=False, config={}, actions={}, **kwargs):
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

        for config_name, config_param in self._config.params.iteritems():  # type: Tuple[str, WTFParam]
            setattr(self, '__' + config_name, WTFParamInterface(config_param))

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if type(self.__dict__['__' + item]) is WTFParamInterface:
            return self.__dict__['__' + item].value
        return self.__dict__['__' + item]

    def read_user_config_file(self, config_folder='config'):
        with open(join(config_folder,self._config_file)) as user_config:
            user_json = json.load(user_config)
            for param_name, param_vaue in user_json.iteritems():
                if param_name not in ['enabled']:
                    self.set_value(param_name, param_vaue)
                if param_name == 'enabled':
                    self._enabled = param_vaue

    def set_value(self, param_name, value):
        param = getattr(self, '__' + param_name)
        param.set_value(value)

    @property
    def enabled(self):
        return self._enabled


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
