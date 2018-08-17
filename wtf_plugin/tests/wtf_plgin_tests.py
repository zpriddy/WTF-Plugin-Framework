import unittest
from wtf_plugin.wtf import WTFPluginHandler

TEST_PLUGIN_PATH = 'plugins'
TEST_CONFIG_PATH = 'config'

class MyTestCase(unittest.TestCase):
    def test_handler_1(self):
        h = WTFPluginHandler(TEST_CONFIG_PATH, TEST_PLUGIN_PATH)
        self.assertEqual(1, len(h.discover_plgins()), 'wrong number of plugins detected')


if __name__ == '__main__':
    unittest.main()
