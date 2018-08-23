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
import json
import logging
from os import walk
from os.path import isdir, isfile, join

from wtf_plugin_interface import WTFPluginInterface
from wtf_plugin import Plugin
from wtf_request import WTFRequest, WTFAction
import importlib

from typing import Dict

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class WTFPluginHandler(object):
    def __init__(self, config_path, plugins_folder):
        self._config_path = config_path
        self._plugins_folder = plugins_folder
        self._plugin_interfaces = dict()
        self._plugins = dict()  # type: Dict[str, Plugin]

        if not check_if_folder_exists(self.config_path):
            logging.fatal('Config path %s does not exist.', self.config_path)

        if not check_if_folder_exists(self.plugins_folder):
            logging.fatal('Plugins folder %s does not exist.', self.plugins_folder)

    def discover_plgins(self):
        plugin_paths = []
        for path, sub, files in walk(self.plugins_folder):
            if 'config.json' in files:
                logging.info('Plugin found at: %s', path)
                plugin_paths.append(path)
        return plugin_paths

    def build_plugin_interface(self, plugin_path):
        default_config_file = join(plugin_path, 'config.json')
        if not isfile(default_config_file):
            logging.fatal('plugin default config file not found.')
        with open(default_config_file) as f:
            default_config = json.load(f)
            plugin_interface = WTFPluginInterface(default_config)
            plugin_interface.read_user_config_file(self._config_path)
            return plugin_interface

    def build_all_plugin_interfaces(self):
        plugin_paths = self.discover_plgins()
        for path in plugin_paths:
            interface = self.build_plugin_interface(path)
            self._plugin_interfaces[interface.config.id] = interface

    def install_plugin(self, plugin_interface):
        """

        Args:
            plugin_interface (WTFPluginInterface):
        """
        logging.info('Installing plugin: %s', plugin_interface.config.id)
        module = importlib.import_module(plugin_interface.config.package)
        self._plugins[plugin_interface.config.id] = module.Setup(plugin_interface)

    def install_all_plugins(self):
        self.build_all_plugin_interfaces()
        for pid, plugin_interface in self._plugin_interfaces.iteritems():
            self.install_plugin(plugin_interface)

    def get_plugins_by_request(self, request, **kwargs):
        """ Will return list of plugins that support that request. If PID is supplied in the request only that plugin
        will be returned.

        Args:
            request (WTFRequest): Request to find plugins by
            **kwargs:

        Returns:

        """
        plugins = list()
        for plugin_name, plugin in self.plugins.iteritems():
            if request.pid and not plugin.id == request.pid:
                continue
            if plugin.has_request(request.request_name):
                plugins.append(plugin_name)
        return plugins

    def get_plugins_by_action(self, action, **kwargs):
        """ Will return list of plugins that support that action. If PID is supplied in the request only that plugin
        will be returned.

        Args:
            action (WTFAction): Action to find plugins by
            **kwargs:

        Returns:

        """

        plugins = list()
        for plugin_name, plugin in self.plugins.iteritems():
            if action.pid and not plugin.id == action.pid:
                continue
            if plugin.has_action(action.request_name):
                plugins.append(plugin_name)
        return plugins

    def send_request(self, request, **kwargs):
        """

        Args:
            request (WTFRequest): request to be sent
        """
        results = dict()
        p = self.get_plugins_by_request(request)
        for plugin_name in p:
            results[plugin_name] = self.send_single_request(request, plugin_name, **kwargs)
        return results

    def send_single_request(self, request, pid, **kwargs):
        return self.plugins[pid].call_request(request)

    def send_action(self, action, **kwargs):
        """

        Args:
            action (WTFAction): action to be sent
        """
        results = dict()
        p = self.get_plugins_by_action(action)
        for plugin_name in p:
            results[plugin_name] = self.send_single_action(action, plugin_name, **kwargs)
        return results

    def send_single_action(self, action, pid, **kwargs):
        return self.plugins[pid].call_action(action)

    @property
    def config_path(self):
        return self._config_path

    @property
    def plugins_folder(self):
        return self._plugins_folder

    @property
    def plugins(self):
        return self._plugins


def check_if_folder_exists(folder):
    return isdir(folder)


def check_if_file_exists(file):
    return isfile(file)
