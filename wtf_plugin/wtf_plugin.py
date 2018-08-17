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

class Plugin(object):
  def __init__(self, pid, plugin_package, plugin_config, **kwargs):
    self._pid = pid
    self._plugin_package = plugin_package
    self._plugin_config = plugin_config

    self._request_map = dict()
    self._action_map = dict()
    self._self_checks_map = dict()

  def add_request(self, request_name, request_function):
    logging.debug('[PLUGIN] adding request: %s to plugin: %s', request_name, self.id)
    self.request_map[request_name] = request_function

  def add_action(self, action_name, action_function):
    logging.debug('[PLUGIN] adding action: %s to plugin: %s', action_name, self.id)
    self.action_map[action_name] = action_function

  #TODO(zpriddy): add function for adding self checks


  @property
  def id(self):
    return self._pid

  @property
  def request_map(self):
    return self._request_map

  @property
  def action_map(self):
    return self._action_map

  @property
  def self_checks_map(self):
    return self._self_checks_map