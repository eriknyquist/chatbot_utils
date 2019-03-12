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

    def test_add_default_response(self):
        r = Responder()
        r.add_responses(("a", 1), ("b", 2)).add_default_response(3)

        self.assertEqual(r.get_response("a")[0], 1)
        self.assertEqual(r.get_response("b")[0], 2)

        self.assertEqual(r.get_response("c")[0], 3)
        self.assertEqual(r.get_response("gfnhvmnbvjm")[0], 3)

    def test_add_response(self):
        r = Responder()
        r.add_response("abc*", 8)
        r.add_response("def+", 9)

        self.assertEqual(r.get_response("ab")[0], 8)
        self.assertEqual(r.get_response("abc")[0], 8)
        self.assertEqual(r.get_response("abccccc")[0], 8)

        self.assertEqual(r.get_response("def")[0], 9)
        self.assertEqual(r.get_response("deff")[0], 9)
        self.assertEqual(r.get_response("deffff")[0], 9)

    def test_add_response_invalid(self):
        r = Responder()
        self.assertRaises(ValueError, r.add_response, 8, None)
        self.assertRaises(ValueError, r.add_response, True, None)

    def test_add_responses(self):
        r = Responder()
        r.add_responses(
            ("abc*", 8),
            ("def+", 9)
        )

        self.assertEqual(r.get_response("ab")[0], 8)
        self.assertEqual(r.get_response("abc")[0], 8)
        self.assertEqual(r.get_response("abccccc")[0], 8)

        self.assertEqual(r.get_response("def")[0], 9)
        self.assertEqual(r.get_response("deff")[0], 9)
        self.assertEqual(r.get_response("deffff")[0], 9)

    def test_add_responses_invalid(self):
        r = Responder()
        self.assertRaises(ValueError, r.add_responses, (8, 0))
        self.assertRaises(ValueError, r.add_responses, (True, 0))
        self.assertRaises(ValueError, r.add_responses, ("valid", 0), (False, 0))

    def test_add_context(self):
        num_tests = 100
        r = Responder()

        for i in range(num_tests):
            r.add_context(Context())
            self.assertEqual(len(r.contexts), i + 1)

    def test_add_context_invalid(self):
        r = Responder()
        self.assertRaises(ValueError, r.add_context, 5)
        self.assertRaises(ValueError, r.add_context, "test")
        self.assertRaises(ValueError, r.add_context, True)
        self.assertRaises(ValueError, r.add_context, Responder())

    def test_add_contexts(self):
        num_tests = 100
        r = Responder()
        contexts = [Context() for _ in range(num_tests)]
        r.add_contexts(*contexts)
        self.assertEqual(len(contexts), len(r.contexts))

    def test_add_contexts_invalid(self):
        r = Responder()
        self.assertRaises(ValueError, r.add_contexts, 5)
        self.assertRaises(ValueError, r.add_contexts, "test")
        self.assertRaises(ValueError, r.add_contexts, True)
        self.assertRaises(ValueError, r.add_contexts, Responder())
        self.assertRaises(ValueError, r.add_contexts, Context(), 5)
