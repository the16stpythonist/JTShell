__author__ = 'Jonas'
import unittest
from JTShell.shell import Shell
from JTShell.util.token import FUNC
from JTShell.util.token import PARAM
from JTShell.util.error import SynError


class TestParser(unittest.TestCase):

    shell = Shell()

    def test_name(self):
        self.assertEqual(self.shell.parser.name, "Parser0")

    def test_parse(self):
        parsed_list = self.shell.parser.parse("test --name1:content1 --name2:content2")
        self.assertEqual(parsed_list[0].name, "test")
        self.assertEqual(parsed_list[0].get_dict(), {"name1": "content1", "name2": "content2"})
        parsed_list = self.shell.parser.parse("(& test --name:100) > test --name:content")
        self.assertEqual(parsed_list[0], "(")
        self.assertEqual(parsed_list[1], "&")
        self.assertEqual(parsed_list[2].name, "test")
        self.assertEqual(parsed_list[2].parameters[0].content, 100)
        self.assertEqual(parsed_list[3], ")")
        self.assertEqual(parsed_list[4], ">")
        self.assertEqual(parsed_list[5].parameters[0].content, "content")


class TestAnalyzer(unittest.TestCase):

    shell = Shell()

    def test_name(self):
        self.assertEqual(self.shell.analyzer.name, "Analyzer0")

    def test_check_brackets(self):
        self.shell.analyzer._check_brackets(["(", "(", "(", ")", ")", ")"], "((()))")
        try:
            self.shell.analyzer._check_brackets(["(", "(", ")", "(", ")"], "(()()")
        except Exception as e:
            if isinstance(e, SynError):
                self.assertEqual(True, True)
            else:
                self.assertEqual(True, False)
        try:
            self.shell.analyzer._check_brackets([")", "("], ")(")
        except Exception as e:
            if isinstance(e, SynError):
                self.assertEqual(True, True)
            else:
                self.assertEqual(True, False)

    def test_check_backgroundchaining(self):
        tokenlist = self.shell.parser.parse("& hallo --name:content ; & hallo --name:content")
        try:
            self.shell.analyzer._check_backgroundchaining(tokenlist)
        except SynError:
            self.assertEqual(True, False, msg="Raised Background chaining error with a correct command")
        try:
            tokenlist = self.shell.parser.parse("& hallo --name:content && hallo --name:content")
            self.shell.analyzer._check_backgroundchaining(tokenlist)
        except Exception as e:
            if isinstance(e, SynError):
                self.assertEqual(True, True)
            else:
                self.assertEqual(True, False, msg="Raised False Exception for true Error")


if __name__ == '__main__':
    unittest.main()