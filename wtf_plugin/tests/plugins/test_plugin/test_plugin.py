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
from wtf_plugin.wtf_plugin import Plugin
from wtf_plugin.wtf_plugin_interface import WTFPluginInterface
from wtf_plugin.wtf_request import WTFRequest
from wtf_plugin.wtf_response import WTFResponse


def Setup(plugin_interface, **kwargs):
    """

    Args:
        plugin_interface (WTFPluginInterface): 
    """
    plugin = TestPlugin(plugin_interface, **kwargs)
    return plugin


class TestPlugin(Plugin):
    def __init__(self, plugin_interface, **kwargs):
        """

        Args:
            plugin_interface (WTFPluginInterface):
        """
        super(TestPlugin, self).__init__(plugin_interface, **kwargs)

        self.add_action('test_action', self.my_test_action)
        self.add_request('echo', self.my_echo_function)

    def my_test_action(self, request, **kwargs):
        """

        Args:
            request (WTFRequest):
        """
        print("Hello World! I am %s and %s years old" % (request.input_1, request.input_2))
        return self.build_action_response(True)

    def my_echo_function(self, request, **kwargs):
        print('Echoing: %s' % request.echo_input)
        return self.build_request_response(request.echo_input)
