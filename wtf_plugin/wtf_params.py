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
from const import PARAM_CONTEXT, PARAM_DEFAULT, PARAM_DEFAULT_INIT, PARAM_REQUIRED, PARAM_TYPE


class WTFParams(object):
    def __init__(self, params_json={}, **kwargs):
        self._params_json = params_json
        self._params = dict()

        for param_name, param in self._params_json.iteritems():
            self.add_param(param_name, **param)

    def __dict__(self):
        output=dict()
        for param in self.params.itervalues():
            output.update(param.export())
        return output

    def add_param(self, name, context, type, default=None, default_init=False, required=False):
        self._params[name] = WTFParam(name, context, type, default, default_init, required)

    def export(self):
        return self.__dict__()

    @property
    def params(self):
        return self._params


class WTFParam(object):
    def __init__(self, name, context, type, default=None, default_init=False, required=False):
        self._name = name
        self._context = context
        self._param_type = type
        self._default = default
        self._default_init = default_init
        self._required = required

    def __dict__(self):
        return {
            self.param_key: {
                PARAM_CONTEXT:      self.context,
                PARAM_TYPE:         self.param_type,
                PARAM_DEFAULT:      self.default,
                PARAM_DEFAULT_INIT: self.default_init,
                PARAM_REQUIRED:     self.required
            }
        }

    def export(self):
        return self.__dict__()

    @property
    def param_key(self):
        return self._name

    @property
    def context(self):
        return self._context

    @property
    def param_type(self):
        return self._param_type

    @property
    def default(self):
        return self._default

    @property
    def default_init(self):
        return self._default_init

    @property
    def required(self):
        return self._required
