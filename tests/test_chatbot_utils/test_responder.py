import re
from unittest import TestCase
from chatbot_utils.responder import Responder, Context

class TestResponder(TestCase):
    def test_compile(self):
        r = Responder().add_response("f?", 0)
        c1 = Context().add_entry_phrase("a+", 1).add_response("b+", 2)
        c1.add_chained_phrases(
            ("x", 3),
            ("y", 4),
            ("z", 5)
        )

        c2 = Context().add_entry_phrase("q+", 6).add_response("t*", 7)
        c2.add_chained_phrases(
            ("x", 3),
            ("y", 4),
            ("z", 5)
        )

        r.add_contexts(c1, c2)

        # Verify nothing's been compiled yet
        self.assertFalse(r.responses.compiled)
        for context in r.contexts:
            self.assertFalse(context.responses.compiled)
            self.assertFalse(context.entry.compiled)

            for chain in context.chains:
                for responsedict in chain:
                    self.assertFalse(responsedict.compiled)

        # Get type of compiled regex
        retype = type(re.compile("abc+"))

        # Compile responder
        r.compile()

        # Verify everything's compiled now
        self.assertTrue(len(r.responses.compiled) > 0)
        for compiled in r.responses.compiled:
            self.assertEqual(type(compiled), retype)

        for context in r.contexts:
            self.assertTrue(len(context.responses.compiled) > 0)
            for compiled in context.responses.compiled:
                self.assertEqual(type(compiled), retype)

            self.assertTrue(len(context.entry.compiled) > 0)
            for compiled in context.entry.compiled:
                self.assertEqual(type(compiled), retype)

            for chain in context.chains:
                for responsedict in chain:
                    self.assertTrue(len(responsedict.compiled) > 0)
                    for compiled in responsedict.compiled:
                        self.assertEqual(type(compiled), retype)
