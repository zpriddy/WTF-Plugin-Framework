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
from os import walk
from os.path import isdir, isfile


class WTFPluginHandler(object):
    def __init__(self, config_path, plugins_folder):
        self._config_path = config_path
        self._plugins_folder = plugins_folder

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

    @property
    def config_path(self):
        return self._config_path

    @property
    def plugins_folder(self):
        return self._plugins_folder


def check_if_folder_exists(folder):
    return isdir(folder)


def check_if_file_exists(file):
    return isfile(file)
