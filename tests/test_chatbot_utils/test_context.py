import re
from unittest import TestCase
from chatbot_utils.responder import Responder, Context, NoResponse

def iterate_redicts(context):
    yield context.responses
    yield context.entry

    for chain in context.chains:
        for responsedict in chain:
            yield responsedict

class TestContext(TestCase):
    def test_compile(self):
        c = Context().add_entry_phrase("a+", 1).add_response("b+", 2)
        c.add_chained_phrases(
            ("x", 3),
            ("y", 4),
            ("z", 5)
        )

        # Verify nothing's been compiled yet
        for responsedict in iterate_redicts(c):
            self.assertFalse(responsedict.compiled)

        # Get type of compiled regex
        retype = type(re.compile("abc+"))

        # Compile responder
        c.compile()

        # Verify everything's compiled now
        for responsedict in iterate_redicts(c):
            self.assertTrue(len(responsedict.compiled) > 0)
            for compiled in responsedict.compiled:
                self.assertEqual(type(compiled), retype)

    def test_add_chained_phrases(self):
        c = Context().add_chained_phrases(
            ("0", 0),
            ("1", 1),
            ("2", 2),
            ("3", 3)
        )

        c.add_response("q", "q")

        # Walk through chain
        self.assertEqual(c.get_response("0")[0], 0)
        self.assertEqual(c.get_response("1")[0], 1)
        self.assertEqual(c.get_response("2")[0], 2)
        self.assertEqual(c.get_response("3")[0], 3)

        # Should be able to go back one step
        self.assertEqual(c.get_response("2")[0], 2)
        self.assertEqual(c.get_response("3")[0], 3)

        # Invalid input (no response) shouldn't exit the chain
        self.assertEqual(c.get_response("h")[0], NoResponse)
        self.assertEqual(c.get_response("3")[0], 3)

        # Exit chain with valid response from context.responses
        self.assertEqual(c.get_response("q")[0], "q")
        self.assertEqual(c.get_response("3")[0], NoResponse)

        # Make sure we can re-enter the chain
        self.assertEqual(c.get_response("0")[0], 0)
        self.assertEqual(c.get_response("1")[0], 1)
        self.assertEqual(c.get_response("2")[0], 2)
        self.assertEqual(c.get_response("3")[0], 3)

    def test_add_entry_phrase(self):
        c = Context().add_entry_phrase("e", 1).add_response("f", 2)
        r = Responder().add_response("a", 3).add_context(c)

        # Verify not in context
        self.assertEqual(r.get_response("a")[0], 3)
        self.assertEqual(r.get_response("f")[0], NoResponse)
        self.assertFalse(r.context)

        # Enter context
        self.assertEqual(r.get_response("e")[0], 1)
        self.assertEqual(r.get_response("f")[0], 2)
        self.assertIs(r.context, c)

        # Exit context, verify we have exited
        self.assertEqual(r.get_response("a")[0], 3)
        self.assertEqual(r.get_response("f")[0], NoResponse)
        self.assertFalse(r.context)

        # Verify we can re-enter
        self.assertEqual(r.get_response("e")[0], 1)
        self.assertEqual(r.get_response("f")[0], 2)
        self.assertIs(r.context, c)

    def test_add_entry_phrase_invalid(self):
        c = Context()
        self.assertRaises(ValueError, c.add_entry_phrase, 0, 0)
        self.assertRaises(ValueError, c.add_entry_phrase, Context(), 0)
        self.assertRaises(ValueError, c.add_entry_phrase, False, 0)
        self.assertRaises(ValueError, c.add_entry_phrase, None, 0)

    def test_add_entry_phrase_list_or_string(self):
        c1 = Context().add_entry_phrase("a|b|c", 1).add_response("d", 2)
        c2 = Context().add_entry_phrase(["a", "b", "c"], 3).add_response("e", 4)

        r1 = Responder().add_response("x", 5).add_context(c1)
        r2 = Responder().add_response("y", 6).add_context(c2)

        self.assertEqual(r1.get_response("x")[0], 5)
        self.assertEqual(r1.get_response("d")[0], NoResponse)

        self.assertEqual(r2.get_response("y")[0], 6)
        self.assertEqual(r1.get_response("e")[0], NoResponse)

        # Verify we can enter context c1 with all 3 version of entry phrase
        self.assertEqual(r1.get_response("a")[0], 1)
        self.assertEqual(r1.get_response("d")[0], 2)
        self.assertEqual(r1.get_response("x")[0], 5)

        self.assertEqual(r1.get_response("b")[0], 1)
        self.assertEqual(r1.get_response("d")[0], 2)
        self.assertEqual(r1.get_response("x")[0], 5)

        self.assertEqual(r1.get_response("c")[0], 1)
        self.assertEqual(r1.get_response("d")[0], 2)
        self.assertEqual(r1.get_response("x")[0], 5)

        # Verify we can enter context c2 with all 3 version of entry phrase
        self.assertEqual(r2.get_response("a")[0], 3)
        self.assertEqual(r2.get_response("e")[0], 4)
        self.assertEqual(r2.get_response("y")[0], 6)

        self.assertEqual(r2.get_response("b")[0], 3)
        self.assertEqual(r2.get_response("e")[0], 4)
        self.assertEqual(r2.get_response("y")[0], 6)

        self.assertEqual(r2.get_response("c")[0], 3)
        self.assertEqual(r2.get_response("e")[0], 4)
        self.assertEqual(r2.get_response("y")[0], 6)

    def test_add_entry_phrases(self):
        c = Context().add_entry_phrases(
            ("a", 1),
            ("b", 2)
        )

        c.add_response("c", 3)

        r = Responder().add_response("d", 4).add_context(c)

        # Verify not in context
        self.assertEqual(r.get_response("d")[0], 4)
        self.assertEqual(r.get_response("c")[0], NoResponse)
        self.assertFalse(r.context)

        # Enter context
        self.assertEqual(r.get_response("a")[0], 1)
        self.assertEqual(r.get_response("c")[0], 3)
        self.assertIs(r.context, c)

        # Exit context
        self.assertEqual(r.get_response("d")[0], 4)

        # Enter context
        self.assertEqual(r.get_response("b")[0], 2)
        self.assertEqual(r.get_response("c")[0], 3)
        self.assertIs(r.context, c)

    def test_add_entry_phrases_invalid(self):
        c = Context()
        self.assertRaises(ValueError, c.add_entry_phrases, (0, 0))
        self.assertRaises(ValueError, c.add_entry_phrases, (Context(), 0))
        self.assertRaises(ValueError, c.add_entry_phrases, (False, 0))
        self.assertRaises(ValueError, c.add_entry_phrases, (None, 0))
        self.assertRaises(ValueError, c.add_entry_phrases, ("valid", 0), (None, 0))
