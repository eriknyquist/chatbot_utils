import random
import time

from chatbot_utils.responder import Responder, Context

random.seed(time.time())

responder = Responder()

# Add a context for talking about cats
cat_context = Context()
cat_context.add_entry_phrases(
    (["(.* )?(talk about|tell( me)? about) cats?.*"], ["Sure, I love cats"])
)

cat_context.add_responses(
    (["(.* )?favou?rite thing about (them|cats?).*"], ["They are fuzzy"]),
    (["(.* )?(do )?you have (one|(a )?cat).*"], ["No, computer programs can't have cats."])
)

# Add a context for talking about cats
dog_context = Context()
dog_context.add_entry_phrases(
    (["(.* )?(talk about|tell( me)? about) dogs?.*"], ["Sure, I think dogs are great"])
)

dog_context.add_responses(
    (["(.* )?favou?rite thing about (them|dogs?).*"], ["They are loyal"]),
    (["(.* )?(do )?you have (one|(a )?dog).*"], ["No, computer programs can't have dogs."])
)

responder.add_default_response(["Oh, really?", "Mmhmm.", "Indeed.", "How fascinating."])
responder.add_responses(
    (["(.* )?hello.*"], ["How do you do?", "Hello!", "Oh, hi."]),
    (["(. *)?(good)?bye.*"], ["Alright then, goodbye.", "See ya.", "Bye."])
)

responder.add_contexts(cat_context, dog_context)

# Simple prompt to get input from command line and pass to responder
while True:
    text = raw_input(" > ")
    resp, groups = responder.get_response(text)
    print("\n\"%s\"\n" % (random.choice(resp)))
