from chatbot_utils import constants as const


class FormattedResponse(object):
    """
    Helper class for parsing variable assignments out of a response phrase, and
    applying format tokens to the response text

    :ivar str response_text: The unformatted response text containing format tokens and/or\
        variable assignments
    :ivar list match_groups: The match groups from the input text that matched a regular expression
    :ivar dict variables: dict of variables that should be included when applying format tokens
    """
    def __init__(self, response_text, match_groups, variables={}):
        self.response_text = response_text
        self.match_groups = match_groups

        # Populated by 'parse' method
        self.formatted_response_text = None
        self.variables = {}

        self.parse(response_text, match_groups, variables)

    def parse(self, response_text, match_groups, variables={}):
        # Build format args for match groups
        if match_groups is None:
            fmtargs = {}
        else:
            fmtargs = {"p%d" % i: match_groups[i] for i in range(len(match_groups))}

        # Split out var. assignments, if any
        fields = response_text.split(const.VAR_ASSIGNMENT_SECTION_SEP)
        if len(fields) >= 2:
            response_text, assignment_str = const.VAR_ASSIGNMENT_SECTION_SEP.join(fields[:-1]), fields[-1]

            # Apply format tokens to variable assignments string
            try:
                assignment_str = assignment_str.format(**fmtargs)
            except KeyError:
                raise KeyError("Invalid format token in variable assignment")

            # Split up the string and populate 'new_vars' dict
            assignments = assignment_str.split(const.VAR_ASSIGNMENT_SEP)
            for a in assignments:
                names = a.split(const.VAR_ASSIGNMENT_OP)
                if len(names) != 2:
                    continue

                self.variables[names[0].strip()] = names[1].strip()

        try:
            self.formatted_response_text = response_text.format(**fmtargs, **variables)
        except (KeyError, IndexError):

            raise KeyError("Invalid format token in response '%s'" % response_text)
