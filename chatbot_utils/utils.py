from chatbot_utils.responder import Context


class ContextCreator(object):
    """
    Context manager for populating a chatbot_utils.responder.Context object and adding it
    to either a Responder object or another Context object.

    Example usage:

        from chatbot_utils.responder import Responder
        from chatbot_utils.utils import ContextCreator

        responder = Responder()

        with ContextCreator(responder) as ctx:
            # Add entry phrase for context #1
            ctx.add_entry_phrase(...)

            # Add nested subcontext
            with ContextCreator(ctx) as subctx:
                # Add entry phrase for subcontext #1
                subctx.add_entry_phrase(...)

    :ivar context_parent: The object that the new context should be added to; should be \
        a chatbot_utils.responder.Responder instance or chatbot_utils.responder.Context instance
    :ivar entry_phrases: Optional list of entry phrase tuples for this context. If non-None,\
        then this will be passed to the 'add_entry_phrases' method of the chatbot_utils.responder.Context\
        object after instantiation.
    """
    def __init__(self, context_parent, entry_phrases=None):
        self.context = None
        self.parent = context_parent

        if entry_phrases is not None:
            self.parent.add_entry_phrases(entry_phrases)

    def __enter__(self):
        self.context = Context()
        return self.context

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.parent.add_context(self.context)


def get_input(prompt=None):
    """
    Helper function, maps to "raw_input" in py2 and "input" in py3
    """
    try:
        ret = raw_input(prompt)
    except NameError:
        ret = input(prompt)

    return ret
