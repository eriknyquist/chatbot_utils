# Shows how to use Context objects
#
# Example usage:
#
#    $> python examples/simple_context_bot.py
#
#     > hey, let's talk about cats
#     "Sure, I love cats"
#     > what's you favourite thing about them?
#     "They are fuzzy"
#     > do you have one?
#     "No, computer programs can't have cats."
#     > OK, let's talk about dogs now
#     "Sure, I think dogs are great"
#     > do you have one?
#     "No, computer programs can't have dogs."
#     > what's your favourite thing about them?
#     "They are loyal"

import random
import time

from chatbot_utils.responder import Responder
from chatbot_utils.utils import ContextCreator, get_input

random.seed(time.time())


responder = Responder()


# Add a context for talking about cats
with ContextCreator(responder) as ctx:
    # Phrase to trigger entry into cat context
    ctx.add_entry_phrases((["(.* )?(talk about|tell( me)? about) cats?.*"], ["Sure, I love cats"]))

    # These phrases will only be recognized after the entry phrase has been seen
    ctx.add_responses(
        (["(.* )?favou?rite thing about (them|cats?).*"], ["They are fuzzy"]),
        (["(.* )?(do )?you have (one|(a )?cat).*"], ["No, computer programs can't have cats."])
    )

    # Add a nested context inside the cat context (you can do this as deep as you like)
    with ContextCreator(ctx) as subctx:
        # Phrase to trigger entry into cat food context, will only be recognized when we're already in the cat context
        subctx.add_entry_phrases((["(.* )?(talk about|tell( me)? about) food?.*"], ["Sure, let's talk about cat food"]))

        # These phrases will only be recognized after BOTH entry phrases have been seen
        subctx.add_responses(
            (["(.* )?(favou?rite|best) type( of food)?.*"], ["Computer programs do not eat cat food."]),
        )

        # Add explicit exit phrase for cat food subcontext (if no exit phrase is added,
        # then he only way to exit the context is using a phrase that was added to the top-level
        # responder object with Responder.add_response())
        subctx.add_exit_phrases((["(.* )?(stop talking about ((dog )?food|this)|talk about something else).*"], ["OK, no more dog food talk."]))


# Add a context for talking about dogs
with ContextCreator(responder) as ctx:
    # Phrase to trigger entry into dog context
    ctx.add_entry_phrases((["(.* )?(talk about|tell( me)? about) dogs?.*"], ["Sure, I think dogs are great"]))

    # These phrases will only be recognized after the entry phrase has been seen
    ctx.add_responses(
        (["(.* )?favou?rite thing about (them|dogs?).*"], ["They are loyal"]),
        (["(.* )?(do )?you have (one|(a )?dog).*"], ["No, computer programs can't have dogs."])
    )

    # Add a nested context inside the dog context (you can do this as deep as you like)
    with ContextCreator(ctx) as subctx:
        # Phrase to trigger entry into dog food context, will only be recognized when we're already in the dog context
        subctx.add_entry_phrases((["(.* )?(talk about|tell( me)? about) food?.*"], ["Sure, let's talk about dog food"]))

        # These phrases will only be recognized after BOTH entry phrases have been seen
        subctx.add_responses(
            (["(.* )?(favou?rite|best) type( of food)?.*"], ["Computer programs do not eat dog food."]),
        )


# One of these responses will be randomly chosen whenever an unrecognized phrase is seen
responder.add_default_response(["Oh, really?", "Mmhmm.", "Indeed.", "How fascinating."])

# These phrases will only be recognized when no context is active
responder.add_responses(
    (["(.* )?hello.*"], ["How do you do?", "Hello!", "Oh, hi."]),
    (["(. *)?(good)?bye.*"], ["Alright then, goodbye.", "See ya.", "Bye."])
)

# Simple prompt to get input from command line and pass to responder
while True:
    text = get_input(" > ")
    resp, groups = responder.get_response(text)
    print("\n\"%s\"\n" % (random.choice(resp)))
