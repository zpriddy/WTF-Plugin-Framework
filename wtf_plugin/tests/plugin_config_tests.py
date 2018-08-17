import json
import unittest

from wtf_plugin.wtf_action import WTFActionConfig, WTFActions
from wtf_plugin.wtf_params import WTFParams, WTFParam
from wtf_plugin.wtf_plugin_interface import WTFPluginInterface

TEST_PLUGIN_CONFIG = 'plugins/test_plugin/config.json'


class WTFConfigTests(unittest.TestCase):
    def test_reading_config_param(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            self.assertTrue('actions' in json_data, 'sample config for plugin is missing actions key')
            actions = json_data['actions']
            self.assertTrue('test_action' in actions, 'sample config for plugin is missing test_action')
            action = actions['test_action']
            self.assertTrue('params' in action, 'sample config for plugin test_action is missing params')
            params = action['params']

            p = WTFParams(params)
            self.assertTrue('input_1' in p.params, 'error parsing input_1')
            input_1 = p.params['input_1']  # type: WTFParam
            self.assertTrue(input_1.required, 'error reading required from input_1')
            self.assertTrue(input_1.default_init, 'error reading default_init from input_1')
            self.assertEqual(input_1.default, 'default value', 'error reading default from input_1')
            self.assertEqual(input_1.param_type, 'string', 'error reading param type from input_1')
            self.assertEqual(input_1.context, 'this is input 1', 'error reading param context from input_1')

            self.assertTrue('input_2' in p.params, 'error parsing input_2')
            input_2 = p.params['input_2']
            self.assertFalse(input_2.required, 'error reading required from input_2')
            self.assertTrue(input_2.default_init, 'error reading default_init from input_2')
            self.assertEqual(input_2.default, 777, 'error reading default from input_2')

    def test_export_param(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            self.assertTrue('actions' in json_data, 'sample config for plugin is missing actions key')
            actions = json_data['actions']
            self.assertTrue('test_action' in actions, 'sample config for plugin is missing test_action')
            action = actions['test_action']
            self.assertTrue('params' in action, 'sample config for plugin test_action is missing params')
            params = action['params']

            p = WTFParams(params)
            self.assertTrue('input_1' in p.params, 'error parsing input_1')
            input_1 = p.params['input_1']  # type: WTFParam

            exported = input_1.export()

            self.assertDictContainsSubset(exported, json_data['actions']['test_action']['params'],
                                          'error exporting param')

    def test_export_params(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            self.assertTrue('actions' in json_data, 'sample config for plugin is missing actions key')
            actions = json_data['actions']
            self.assertTrue('test_action' in actions, 'sample config for plugin is missing test_action')
            action = actions['test_action']
            self.assertTrue('params' in action, 'sample config for plugin test_action is missing params')
            params = action['params']

            p = WTFParams(params)

            exported = p.export()

            self.assertDictContainsSubset(exported, json_data['actions']['test_action']['params'],
                                          'error exporting params')

    def test_import_actions(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            self.assertTrue('actions' in json_data, 'sample config for plugin is missing actions key')
            actions = json_data['actions']
            self.assertTrue('test_action' in actions, 'sample config for plugin is missing test_action')
            action = actions['test_action']
            a = WTFActionConfig('test_action', **action)
            self.assertDictContainsSubset(a.export(), actions, 'error importing or exporting actions')

    def test_import_actions_multi(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            self.assertTrue('actions' in json_data, 'sample config for plugin is missing actions key')
            actions = json_data['actions']
            a = WTFActions(actions)
            self.assertDictEqual(a.export(), actions, 'error importing or exporting actions')

    def test_plugin_interface_1(self):
        with open(TEST_PLUGIN_CONFIG) as config_file:
            json_data = json.load(config_file)
            i = WTFPluginInterface(json_data)
            self.assertEqual('zpriddy', i.config.username, 'plugin interface did not get default username')
            i.config.read_user_config_file()
            self.assertEqual('not zpriddy', i.config.username, 'plugin interface did not get user config username')
            self.assertEqual('password123', i.config.password, 'plugin interface did not get user config password')



if __name__ == '__main__':
    unittest.main()
