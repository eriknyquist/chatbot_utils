import re
from unittest import TestCase
from chatbot_utils.redict import ReDict

class TestReDict(TestCase):
    def test_all_items_accessible(self):
        num_iterations = 50
        d = ReDict()

        for i in range(num_iterations):
            expr = "(foo*|bar+) %d" % i
            d[expr] = i

        for i in range(num_iterations):
            test1 = "fo %d" % i
            test2 = "foo %d" % i
            test3 = "foooo %d" % i
            test4 = "bar %d" % i
            test5 = "barr %d" % i
            test6 = "barrrrr %d" % i

            for testval in [test1, test2, test3, test4, test5, test6]:
                self.assertEquals(i, d[testval])

    def test_groups_per_regex(self):
        d = ReDict()
        num_iterations = d.groups_per_regex * 3

        for i in range(num_iterations):
            expr = "((f)(o)(o)*|(b)(a)(r)+) %d" % i
            d[expr] = i

        for i in range(num_iterations):
            self.assertEqual(i, d["foo %d" % i])

    def test_value_can_be_arbitrary_object(self):
        d = ReDict()
        strval = "test string"
        boolval = False
        classval = self.__class__
        funcval = self.setUpClass

        d["str"] = strval
        d["bool"] = boolval
        d["class"] = classval
        d["func"] = funcval

        self.assertIs(d["str"], strval)
        self.assertIs(d["bool"], boolval)
        self.assertIs(d["class"], classval)
        self.assertIs(d["func"], funcval)

    def test_compile(self):
        # get type object for compiled regex
        retype = type(re.compile("a+"))

        d = ReDict()
        d["a"] = 1
        d["b"] = 2
        d["c"] = 3
        self.assertFalse(d.compiled)

        d.compile()
        self.assertTrue(len(d.compiled) > 0)

        for c in d.compiled:
            self.assertTrue(isinstance(c, retype))

    def test_groups(self):
        d = ReDict()
        num = 8
        val1 = "hello"
        val2 = "world"
        val3 = "!"
        expr = "(.*) (.*) (.*)"
        d[expr] = num

        testinput = "%s %s %s" % (val1, val2, val3)
        self.assertEqual(num, d[testinput])

        groups = d.groups()
        self.assertEqual(groups[0], val1)
        self.assertEqual(groups[1], val2)
        self.assertEqual(groups[2], val3)

    def test_dump_to_dict(self):
        testitems = {
            "a+": 1,
            "b*": 2,
            "c?": 3
        }

        d = ReDict()
        for key in testitems:
            d[key] = testitems[key]

        dumped = d.dump_to_dict()

        for key in dumped:
            self.assertTrue(key in testitems)
            self.assertEqual(dumped[key], testitems[key])

        self.assertEqual(len(testitems), len(dumped))

    def test_load_from_dict(self):
        testitems = {
            "x+": 1,
            "y?": 2,
            "z*": 3
        }

        d = ReDict()
        for key in testitems:
            d[key] = testitems[key]

        dumped = d.dump_to_dict()
        loaded_redict = ReDict().load_from_dict(dumped)

        self.assertEqual(testitems["x+"], loaded_redict["xxxx"])
        self.assertEqual(testitems["y?"], loaded_redict["y"])
        self.assertEqual(testitems["z*"], loaded_redict["zz"])