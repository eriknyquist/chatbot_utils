from chatbot_utils.redict import ReDict

def _check_get_response(responsedict, text):
    try:
        response = responsedict[text]
    except KeyError:
        return None

    return response

def _check_pattern_response_pair(pair):
    if len(pair) != 2:
        raise ValueError("Pattern response pair must contain two items")

    patterns, response = pair
    if type(patterns) != list:
        raise ValueError("First item in pattern response pair must be "
            "a list")

    return patterns, response

class Context(object):
    def __init__(self, lists=None):
        self.entry = ReDict()
        self.responses = ReDict()
        self.chains = []
        self.chain = None
        self.chain_index = 0

        if lists:
            self._build_from_lists(lists)

    def add_chained_phrases(self, *pattern_response_pairs):
        chain = []
        for pair in pattern_response_pairs:
            patterns, response = _check_pattern_response_pair(pair)
            responsedict = ReDict()
            responsedict['|'.join(patterns)] = response
            chain.append(responsedict)

        self.chains.append(chain)

    def add_entry_phrases(self, *pattern_response_pairs):
        for pair in pattern_response_pairs:
            patterns, response = _check_pattern_response_pair(pair)
            self.entry['|'.join(patterns)] = response

    def add_responses(self, *pattern_response_pairs):
        for pair in pattern_response_pairs:
            patterns, response = _check_pattern_response_pair(pair)
            if type(patterns) != list:
                raise ValueError("First item in pattern response pair must be "
                    "a list")

            self.responses['|'.join(patterns)] = response

    def _search_chains(self, text):
        for chain in self.chains:
            if (len(chain) > 0):
                resp = _check_get_response(chain[0], text)
                if resp:
                    return chain, resp

        return None, None

    def _get_chained_response(self, text):
        if not self.chain:
            chain, response = self._search_chains(text)
            if chain:
                self.chain = chain
                self.chain_index = 1
                return response

            return None

        responsedict = self.chain[self.chain_index]
        resp = _check_get_response(responsedict, text)

        if resp:
            if self.chain_index < (len(self.chain) - 1):
                self.chain_index += 1
        elif self.chain_index > 0:
            responsedict = self.chain[self.chain_index - 1]
            resp = _check_get_response(responsedict, text)

        return resp

    def get_response(self, text):
        resp = self._get_chained_response(text)
        if resp:
            return resp

        resp = _check_get_response(self.responses, text)
        if resp:
            return resp

        return _check_get_response(self.entry, text)

class Responder(object):
    """
    """

    def __init__(self):
        """
        """

        self.responses = ReDict()
        self.default_response = None

        self.context = None
        self.contexts = []

    def add_default_response(self, response):
        """
        Set response to return when no other matching responses can be found

        :param response: object to return as default response
        """
        self.default_response = response

    def add_response(self, patterns, response):
        """
        Set response to reply with for a specific pattern (or patterns)

        :param list patterns: list of regular expressions. If the input passed \
            to ``get_response`` matches one of these patterns, then the object \
            passed here as ``response`` will be returned.
        :param object response: object to return from ``get_response`` if the \
            passed input matches one of the regular expressions passed here as
            ``response``.
        """
        self.responses['|'.join(patterns)] = response

    def add_context(self, context):
        if not isinstance(context, Context):
            raise ValueError("add_context argument must be a Context instance")

        self.contexts.append(context)

    def add_contexts(self, *contexts):
        for context in contexts:
            self.add_context(context)

    def add_responses(self, *pattern_response_pairs):
        """
        Set multiple pattern/response pairs at once

        :param responses: one or more response pairs, where each pair is a \
            tuple containing arguments for a single ``add_response`` call, \
            e.g. ``add_responses((['cat.*'], 'meow'), (['dog.*], 'woof'))``
        """
        for pair in pattern_response_pairs:
            patterns, response = _check_pattern_response_pair(pair)
            self.add_response(patterns, response)

    def _attempt_context_entry(self, text):
        for context in self.contexts:
            response = _check_get_response(context.entry, text)
            if response:
                self.context = context
                return response

        return None

    def get_response(self, text):
        response = None

        # If currently in a context, try to get a response from the context
        if self.context:
            response = self.context.get_response(text)

        # If no contextual response is available, try to get a response from
        # the dict of contextless responses
        if not response:
            response = _check_get_response(self.responses, text)
            if response:
                # If we are currently in a context but only able to get a
                # matching response from the contextless dict, set the current
                # context to None
                if self.context:
                    self.context = None
            else:
                # No contextless responses available, attempt context entry
                response = self._attempt_context_entry(text)
                if not response:
                    response = self.default_response

        if not response:
            return text

        return response
