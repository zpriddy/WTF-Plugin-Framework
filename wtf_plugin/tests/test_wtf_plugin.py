import unittest
from wtf_plugin.wtf import WTFPluginHandler

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

    def test_handler_4(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        h.install_all_plugins()
        self.assertTrue(h.plugins['test_plugin'].actions.test_action.enabled)
        h.plugins['test_plugin'].actions.test_action.call()
        h.plugins['test_plugin'].actions.test_action.call(input_2='zpriddy')

if __name__ == '__main__':
    unittest.main()
