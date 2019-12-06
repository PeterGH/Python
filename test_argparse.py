import argparse
import unittest

class TestArgParse(unittest.TestCase):

    def test_argument_type(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("strarg", help = "default type is string")
        parser.add_argument("intarg", help = "parse as int", type = int)
        parser.add_argument("--stropt", help = "default type is string")
        parser.add_argument("--intopt", help = "parse as int", type = int)
        args = parser.parse_args("123 456 --stropt 789 --intopt 10".split())
        self.assertEqual(type(args.strarg), str)
        self.assertEqual(type(args.intarg), int)
        self.assertEqual(type(args.stropt), str)
        self.assertEqual(type(args.intopt), int)

    def test_argument_bool(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--trueopt", help = "True if defined, False otherwise", action = "store_true")
        parser.add_argument("--falseopt", help = "False if defined, True otherwise", action = "store_false")
        args = parser.parse_args([])
        self.assertEqual(args.trueopt, False)
        self.assertEqual(args.falseopt, True)
        args = parser.parse_args("--trueopt --falseopt".split())
        self.assertEqual(args.trueopt, True)
        self.assertEqual(args.falseopt, False)

    def test_argument_value(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--defaultopt", help = "default value is None")
        parser.add_argument("--stropt", help = "string value")
        args = parser.parse_args("--stropt 123".split())
        self.assertEqual(args.defaultopt, None)
        self.assertEqual(args.stropt, "123")

    def test_argument_choices(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--enum1", help = "default value is None", type = int, choices = [0, 1, 2])
        parser.add_argument("--enum2", help = "default value is 1", type = int, choices = [0, 1, 2], default = 0)
        args = parser.parse_args([])
        self.assertEqual(args.enum1, None)
        self.assertEqual(args.enum2, 0)
        args = parser.parse_args("--enum1 1 --enum2 2".split())
        self.assertEqual(args.enum1, 1)
        self.assertEqual(args.enum2, 2)

    def test_argument_error(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--enum", help = "default value is 1", type = int, choices = [0, 1, 2], default = 0)
        # Seems argparse default behavior is to exit on ArgumentError,
        # so have to catch SystemExit exception.
        # with self.assertRaises(argparse.ArgumentError):
        with self.assertRaises(SystemExit):
            args = parser.parse_args("--enum 3".split())
        try:
            args = parser.parse_args("--enum 3".split())
        # except argparse.ArgumentError:
        except SystemExit:
            self.assertTrue(True)
        else:
            self.fail()

    def test_argument_mutually_exclusive(self):
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--opt1", help = "True if defined, False otherwise", action = "store_true")
        group.add_argument("--opt2", help = "True if defined, False otherwise", action = "store_true")
        group.add_argument("--opt3", help = "True if defined, False otherwise", action = "store_true")
        args = parser.parse_args(["--opt1"])
        self.assertTrue(args.opt1)
        args = parser.parse_args(["--opt2"])
        self.assertTrue(args.opt2)
        args = parser.parse_args(["--opt2"])
        self.assertTrue(args.opt2)
        with self.assertRaises(SystemExit):
            args = parser.parse_args("--opt1 --opt2".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("--opt2 --opt3".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("--opt1 --opt3".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("--opt1 --opt2 --opt3".split())

    def test_argument_zero_or_more(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("args", help = "zero or more arguments", nargs = "*")
        args = parser.parse_args([])
        self.assertEqual(len(args.args), 0)
        args = parser.parse_args(["v1"])
        self.assertEqual(len(args.args), 1)
        args = parser.parse_args("v1 v2".split())
        self.assertEqual(len(args.args), 2)
        args = parser.parse_args("v1 v2 v3".split())
        self.assertEqual(len(args.args), 3)

    def test_argument_one_or_more(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("args", help = "one or more arguments", nargs = "+")
        args = parser.parse_args(["v1"])
        self.assertEqual(len(args.args), 1)
        args = parser.parse_args("v1 v2".split())
        self.assertEqual(len(args.args), 2)
        args = parser.parse_args("v1 v2 v3".split())
        self.assertEqual(len(args.args), 3)
        with self.assertRaises(SystemExit):
            args = parser.parse_args([])

    def test_subparsers_command_by_bool(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        parser_cmd1 = subparsers.add_parser("cmd1", help = "Execute cmd1")
        parser_cmd1.add_argument("--cmd1", help = "A trick to inidicate whether cmd1 is called", action = "store_const", const = True, default = True)
        parser_cmd2 = subparsers.add_parser("cmd2", help = "Execute cmd2")
        parser_cmd2.add_argument("--cmd2", help = "A trick to inidicate whether cmd2 is called", action = "store_const", const = True, default = True)
        args = parser.parse_args(["cmd1"])
        self.assertTrue(hasattr(args, "cmd1"))
        self.assertFalse(hasattr(args, "cmd2"))
        self.assertTrue(args.cmd1)
        args = parser.parse_args("cmd1 --cmd1".split())
        self.assertTrue(hasattr(args, "cmd1"))
        self.assertFalse(hasattr(args, "cmd2"))
        self.assertTrue(args.cmd1)
        args = parser.parse_args(["cmd2"])
        self.assertTrue(hasattr(args, "cmd2"))
        self.assertFalse(hasattr(args, "cmd1"))
        self.assertTrue(args.cmd2)
        args = parser.parse_args("cmd2 --cmd2".split())
        self.assertTrue(hasattr(args, "cmd2"))
        self.assertFalse(hasattr(args, "cmd1"))
        self.assertTrue(args.cmd2)
        args = parser.parse_args([])
        self.assertFalse(hasattr(args, "cmd1"))
        self.assertFalse(hasattr(args, "cmd2"))
        with self.assertRaises(SystemExit):
            args = parser.parse_args("cmd1 cmd2".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("cmd1 --cmd2".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("cmd2 cmd1".split())
        with self.assertRaises(SystemExit):
            args = parser.parse_args("cmd2 --cmd1".split())

    def test_subparsers_command_by_enum(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--cmdid", help = "A trick to inidicate whether a cmd is called", action = "store_const", const = 0, default = 0)
        subparsers = parser.add_subparsers()
        parser_cmd1 = subparsers.add_parser("cmd1", help = "Execute cmd1")
        parser_cmd1.add_argument("--cmdid", help = "A trick to inidicate whether cmd1 is called", action = "store_const", const = 1, default = 1)
        parser_cmd2 = subparsers.add_parser("cmd2", help = "Execute cmd2")
        parser_cmd2.add_argument("--cmdid", help = "A trick to inidicate whether cmd2 is called", action = "store_const", const = 2, default = 2)
        parser_cmd3 = subparsers.add_parser("cmd3", help = "Execute cmd3")
        parser_cmd3.add_argument("--cmdid", help = "A trick to inidicate whether cmd3 is called", action = "store_const", const = 3, default = 3)
        args = parser.parse_args([])
        self.assertTrue(hasattr(args, "cmdid"))
        self.assertEqual(args.cmdid, 0)
        args = parser.parse_args(["cmd1"])
        self.assertTrue(hasattr(args, "cmdid"))
        self.assertEqual(args.cmdid, 1)
        args = parser.parse_args(["cmd2"])
        self.assertTrue(hasattr(args, "cmdid"))
        self.assertEqual(args.cmdid, 2)
        args = parser.parse_args(["cmd3"])
        self.assertTrue(hasattr(args, "cmdid"))
        self.assertEqual(args.cmdid, 3)

    def test_argument_command_by_enum(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command", help = "default value is cmd1", choices = ["cmd1", "cmd2", "cmd3"], default = "cmd1", nargs = "?")
        parser.add_argument("args", help = "command arguments, zero or more", nargs = "*")
        args = parser.parse_args([])
        self.assertEqual(args.command, "cmd1")
        self.assertEqual(len(args.args), 0)
        args = parser.parse_args(["cmd1"])
        self.assertEqual(args.command, "cmd1")
        self.assertEqual(len(args.args), 0)
        args = parser.parse_args(["cmd2"])
        self.assertEqual(args.command, "cmd2")
        self.assertEqual(len(args.args), 0)
        args = parser.parse_args("cmd3 arg1".split())
        self.assertEqual(args.command, "cmd3")
        self.assertEqual(len(args.args), 1)
        self.assertEqual(args.args[0], "arg1")
        args = parser.parse_args("cmd3 arg1 arg2".split())
        self.assertEqual(args.command, "cmd3")
        self.assertEqual(len(args.args), 2)
        self.assertEqual(args.args[0], "arg1")
        self.assertEqual(args.args[1], "arg2")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Demo how to use argparse",
            usage =
"""
    python %(prog)s [-h]
    python -m unittest %(prog)s [-v]
""")
    args = parser.parse_args()
    print(args)
