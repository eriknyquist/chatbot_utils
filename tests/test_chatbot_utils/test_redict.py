import re
from unittest import TestCase
from chatbot_utils.redict import ReDict

class TestReDict(TestCase):
    def fill_redict(self, dictobj=None, numitems=1000):
        if not dictobj:
            dictobj = ReDict()

        testitems = {"((foo+|bar*) )?%d" % i : i for i in range(numitems)}

        for key, val in testitems.items():
            dictobj[key] = val

        return testitems, dictobj

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
        testitems, d = self.fill_redict()
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

    def test_pop(self):
        d = ReDict()
        d["a+"] = 1
        d["b+"] = 2

        self.assertEqual(2, len(d))
        self.assertEqual(d["aaa"], 1)
        self.assertEqual(d["bbb"], 2)

        self.assertEqual(d.pop("b"), 2)
        self.assertEqual(1, len(d))

        self.assertEqual(d["aaa"], 1)
        self.assertRaises(KeyError, d.__getitem__, "bbb")

    def test_items(self):
        testitems, d = self.fill_redict()
        redict_items = d.items()
        self.assertEqual(len(redict_items), len(testitems))

        for key, value in redict_items:
            self.assertTrue(key in testitems)
            self.assertEqual(value, testitems[key])

    def test_values(self):
        testitems, d = self.fill_redict()
        redict_values = d.values()
        self.assertEqual(len(redict_values), len(testitems))

        for value in redict_values:
            self.assertTrue(value in testitems.values())

    def test_keys(self):
        testitems, d = self.fill_redict()
        redict_keys = d.keys()
        self.assertEqual(len(redict_keys), len(testitems))

        for key in redict_keys:
            self.assertTrue(key in testitems)

    def test_iteritems(self):
        item_count = 0
        testitems, d = self.fill_redict()
        for key, value in d.iteritems():
            self.assertTrue(key in testitems)
            self.assertEqual(value, testitems[key])
            item_count += 1

        self.assertEqual(item_count, len(testitems))

    def test_clear(self):
        d = ReDict()
        testitems = {
            "q+": 4,
            "r*": 5,
            "s?": 6
        }

        for key, val in testitems.items():
            d[key] = val

        self.assertEqual(d["qqq"], 4)
        self.assertEqual(len(testitems), len(d))

        d.clear()
        self.assertEqual(0, len(d))
        self.assertRaises(KeyError, d.__getitem__, "qqq")

    def test_copy(self):
        d = ReDict()
        testitems = {
            "xyz+": 4,
            "ab*c": 5,
            "def?": 6
        }

        for key, val in testitems.items():
            d[key] = val

        d2 = d.copy()

        self.assertEqual(len(d), len(d2))
        for key, val in d.iteritems():
            self.assertTrue(key in d2.keys())
            self.assertTrue(val in d2.values())

        self.assertEqual(d2["xyz"], d["xyz"])
        self.assertEqual(d2["abbbc"], d["abbbc"])
        self.assertEqual(d2["def"], d["def"])

    def test_update(self):
        d1 = ReDict()
        d2 = ReDict()
        testitems = {
            "xyz+": 4,
            "ab*c": 5,
            "def?": 6
        }

        updateitems = {
            "q+": 1,
            "r*": 2,
            "s?": 3
        }

        for key, val in testitems.items():
            d1[key] = val

        for key, val in updateitems.items():
            d2[key] = val

        d1.update(d2)
        self.assertEqual(len(d1), len(testitems) + len(updateitems))

        for key, val in testitems.items():
            self.assertTrue(key in d1.keys())
            self.assertTrue(val in d1.values())

        for key, val in updateitems.items():
            self.assertTrue(key in d1.keys())
            self.assertTrue(val in d1.values())
