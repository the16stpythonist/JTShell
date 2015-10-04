__author__ = 'Jonas'
import unittest
from JTShell.util.token import PARAM
from JTShell.util.token import FUNC


class ParamTest(unittest.TestCase):

    param = PARAM("--name=content")

    def test_convert_parametertype_boolean(self):
        self.assertEqual(self.param._convert_parametertype("true"), True)
        self.assertEqual(self.param._convert_parametertype("True"), True)
        self.assertEqual(self.param._convert_parametertype("false"), False)
        self.assertEqual(self.param._convert_parametertype("False"), False)

    def test_convert_parametertype_float(self):
        self.assertEqual(self.param._convert_parametertype("120"), 120.0)
        self.assertEqual(self.param._convert_parametertype("56.23"), 56.23)

    def test_convert_parametetype_string(self):
        self.assertEqual(self.param._convert_parametertype("hallo"), "hallo")
        self.assertEqual(self.param._convert_parametertype('''"hallo"'''), "hallo")

    def test_string_parameter(self):
        param = PARAM('''--name:"all i do is testing"''')
        self.assertEqual(param.name, "name")
        self.assertEqual(param.content, "all i do is testing")

    def test_float_parameter(self):
        param = PARAM("--name:123.12")
        self.assertEqual(param.name, "name")
        self.assertEqual(param.content, 123.12)

    def test_list_parameter(self):
        param = PARAM('''--name:[1, 2, 3,"hallo"]''')
        self.assertEqual(param.name, "name")
        self.assertEqual(param.content, [1, 2, 3, "hallo"])


class FuncTest(unittest.TestCase):

    def test_name(self):
        func = FUNC("testname")
        self.assertEqual(func.name, "testname")

    def test_parameters(self):
        func = FUNC("test")
        param = PARAM("--name:content")
        func.add_parameter(param)
        self.assertEqual(func.get_dict(), {"name": "content"})

if __name__ == '__main__':
    unittest.main()
