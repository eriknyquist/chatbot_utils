Format tokens
=============

Using format tokens to "remember" some earlier data that was provided
---------------------------------------------------------------------

Response text may include format tokens that reference matching text
within parenthesis groups in the pattern. These tokens should be of the form ``{{pN}}``,
where ``N`` is an integer representing the position of the parenthesis group within
the pattern, from left-to-right.

For example, given the pattern ``I like ([a-z]*) and ([a-z]*)``, and the response
text ``I like {{p0}} too, but not {{p1}}``, an input of ``I like cats and dogs`` would yield
a response of ``I like cats too, but not dogs``.

Creating new format tokens with special response syntax
-------------------------------------------------------

The provided response text may also contain commands to create custom format tokens
on the fly. Custom format tokens may be mapped to arbitrary literal strings, or to
other format tokens. This is achieved by appending ``;;`` to the end of the response
text, to mark the beginning of the custom format token assignments, followed by one or more
comma-separated assignment statements of the form ``name=value`` (both name and value
may be any string of characters, except for ``,`` and ``=``).

For example, given the pattern ``I like (.*) and (.*)``, and the response text
``OK, {{p0}} and {{p0}};;like1={{p0}},like2={{p1}}``, an input of ``I like green and red``
would yield a response of ``OK, green and red``, and would create two new format
tokens named "like1" and "like2" that can be used in future response phrases.
For example, the response text ``you like {{like1}} and {{like2}}`` would yield
"you like green and red" when triggered.

Example bot that remembers your favourite movie
-----------------------------------------------

Here is an example implementation of a simple bot that can remember your favourite movie and
report it to you when asked:

::

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

And here is some sample output from running the above example script:

.. code-block:: python

    $> python example_format_tokens_bot.py

    > howdy!

    "Please tell me what your favourite movie is"

    > hmm, OK, I guess my favourite film is Gone With The Wind

    "Cool, I will remember that your favourite film is Gone With The Wind!"

    > hey, can you tell me what my fave movie is?

    "Your favourite film is Gone With The Wind!"

    > alright, now my favorite movie is spiderman 2

    "Cool, I will remember that your favourite film is spiderman 2!"

    > what's my favourite film?

    "Your favourite film is spiderman 2!"

    >

