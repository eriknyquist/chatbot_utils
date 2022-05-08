# Shows how to use format tokens / variable assignments in response phrases,
# to make a bot that can remember what you say and report it back later
#
#
# Example usage:
#
#    $> python examples/format_tokens.py
#
#    > howdy!
#
#    "Please tell me what your favourite movie is"
#
#    > hmm, OK, I guess my favourite film is Gone With The Wind
#
#    "Cool, I will remember that your favourite film is Gone With The Wind!"
#
#    > hey, can you tell me what my fave movie is?
#
#    "Your favourite film is Gone With The Wind!"
#
#    > alright, now my favorite movie is spiderman 2
#
#    "Cool, I will remember that your favourite film is spiderman 2!"
#
#    > what's my favourite film?
#
#    "Your favourite film is spiderman 2!"
#
#    >


import random
import time

from chatbot_utils.responder import Responder
from chatbot_utils.utils import ContextCreator, get_input

responder = Responder()

responder.add_default_response("Please tell me what your favourite movie is")

responder.add_responses(
    # When the bot is told what my favourite film is, it will save whatever film I said (4th
    # parenthesis group, or p3) in a new variable named "faveMovie"
    (["(.* )?(favou?rite|fave) (movie|film) is (.*)$"],
     "Cool, I will remember that your favourite film is {p3}!;;faveMovie={p3}"),

    # When the bot is asked to recall what my favourite film is, it will report the value of 'faveMovie'
    (["(.*)?(what is|what'?s|(can you )?tell me )?(what('?s)? )?my (fave|favou?rite) (movie|film).*"],
     "Your favourite film is {faveMovie}!")
)

# Simple prompt to get input from command line and pass to responder
while True:
    text = get_input(" > ")
    resp, groups = responder.get_response(text)
    print("\n\"%s\"\n" % resp)
