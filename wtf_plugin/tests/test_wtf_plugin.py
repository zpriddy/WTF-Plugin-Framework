import unittest

from wtf_plugin.wtf import WTFPluginHandler
from wtf_plugin.wtf_request import WTFRequest, WTFAction
from wtf_plugin.wtf_response import WTFResponse

TEST_PLUGIN_PATH = 'plugins'
TEST_CONFIG_PATH = 'config'


class MyTestCase(unittest.TestCase):
    def test_handler_1(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        self.assertEqual(1, len(h.discover_plgins()), 'wrong number of plugins detected')

    def test_handler_2(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        plugin_paths = h.discover_plgins()
        for path in plugin_paths:
            interface = h.build_plugin_interface(path)
            self.assertEqual('password123', interface.config.password)

    def test_handler_3(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        h.install_all_plugins()
        self.assertEqual('password123', h.plugins['test_plugin'].config.password)

    # Disabled due to incorrect way of calling function
    # TODO: Disable this way of calling functions
    # def test_handler_4(self):
    #     h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
    #     h.install_all_plugins()
    #     self.assertTrue(h.plugins['test_plugin'].actions.test_action.enabled)
    #     h.plugins['test_plugin'].actions.test_action.call(WTFRequest('test_action'))
    #     h.plugins['test_plugin'].actions.test_action.call(WTFRequest('test_action', input_2='zpriddy'))

    def test_handler_4(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        h.install_all_plugins()
        self.assertTrue(h.plugins['test_plugin'].actions.test_action.enabled)
        action_result = h.send_action(WTFAction('test_action', 'test_plugin', input_1=5, input_2='zpriddy'))
        # h.plugins['test_plugin'].actions.test_action.call(WTFRequest('test_action'))
        # h.plugins['test_plugin'].actions.test_action.call(WTFRequest('test_action', input_2='zpriddy'))
        self.assertTrue(action_result['test_plugin'].success)

    # Disabled due to incorrect way of calling function
    # TODO: Disable this way of calling functions
    # def test_handler_5(self):
    #     h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
    #     h.install_all_plugins()
    #     self.assertTrue(h.plugins['test_plugin'].requests.echo.enabled)
    #     h.plugins['test_plugin'].requests.echo.call(WTFRequest('echo'))
    #     self.assertEqual(h.plugins['test_plugin'].requests.echo.call(WTFRequest('echo', echo_input='zpriddy')).value,
    #                      'zpriddy')

    def test_handler_plugins_by_request(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        h.install_all_plugins()
        p = h.get_plugins_by_request(WTFRequest('echo'))
        self.assertEqual(p, ['test_plugin'])

    def test_handler_send_request(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        h.install_all_plugins()
        p = h.send_request(WTFRequest('echo', echo_input='zpriddy'))
        self.assertEqual(WTFResponse('test_plugin', 'zpriddy', 5, function_name='echo', success=True).response,
                         p['test_plugin'].response)


if __name__ == '__main__':
    unittest.main()
