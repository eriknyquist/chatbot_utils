Format tokens
=============

Response text may include format tokens that reference matching text
within parenthesis groups in the pattern. These tokens should be of the form "{{pN}}",
where "N" is an integer representing the position of the parenthesis group within
the pattern, from left-to-right.

For example, given the pattern "I like ([a-z]*) and ([a-z]*)", and the response
text "I like {{p0}} too, but not {{p1}}", an input of "I like cats and dogs" would yield
a response of "I like cats too, but not dogs".

Creating new format tokens with special response syntax
=======================================================

The provided response text may also contain commands to create custom format tokens
on the fly. Custom format tokens may be mapped to arbitrary literal strings, or to
other format tokens. This is achieved by appending ";;" to the end of the response
text, to mark the beginning of the custom format tokens, followed by one or more
comma-separated assignment statements of the form "name=value" (both name and value
may be any string of characters, except for "," and "=").

For example, given the pattern "I like (.*) and (.*)", and the response text
"OK, {{p0}} and {{p0}};;like1={{p0}},like2={{p1}}", an input of "I like green and red"
would yield a response of "OK, green and red", and would create two new format
tokens. You can now use "like1" and "like2" as format tokens in further responses.
For example, the response text "you like {{like1}} and {{like2}}" would yield
"you like green and red" when triggered.
