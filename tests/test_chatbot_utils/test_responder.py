import re
from unittest import TestCase
from chatbot_utils.responder import Responder, Context

def iterate_redicts(responder):
    yield responder.responses
    for context in responder.contexts:
        yield context.responses
        yield context.entry

        for chain in context.chains:
            for responsedict in chain:
                yield responsedict

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
        for responsedict in iterate_redicts(r):
            self.assertFalse(responsedict.compiled)

        # Get type of compiled regex
        retype = type(re.compile("abc+"))

        # Compile responder
        r.compile()

        # Verify everything's compiled now
        for responsedict in iterate_redicts(r):
            self.assertTrue(len(responsedict.compiled) > 0)
            for compiled in responsedict.compiled:
                self.assertEqual(type(compiled), retype)
