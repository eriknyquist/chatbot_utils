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
