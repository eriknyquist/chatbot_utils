# Shows how to use the 'groups' value returned by get_response() to obtain
# input from the person speaking with a bot
#
# Example usage:
#
#    $> python examples/bedtime_bot.py
#
#    > hey, what time is it?
#    "The time is 18:31"
#    > is that past my bedtime?
#    "You haven't told me what your bedtime is yet."
#    > ok, remember that my bedtime is 23:00
#    "OK, I'll remember that your bedtime is 23:00"
#    > is it past my bedtime yet?
#    "No, your bedtime is at 23:00"
#    > OK, now my bedtime is 18:31
#    "OK, I'll remember that your bedtime is 18:31"
#    > what time is it now?
#    "The time is 18:32"
#    > is that past my bedtime?
#    "Yes, your bedtime was at 18:31"

import time
from datetime import timedelta

from chatbot_utils.responder import Responder, Context

bedtime = [None, None]

def current_time():
    t = time.localtime()
    return t.tm_hour, t.tm_min

def current_time_handler(groups):
    hour, minute = current_time()
    return "The time is %02d:%02d" % (hour, minute)

def ask_bedtime_handler(groups):
    hour, minute = bedtime
    if not hour:
        return "You haven't told me what your bedtime is yet."

    return "Your bedtime is %02d:%02d" % (hour, minute)

def set_bedtime_handler(groups):
    # We are expecting the time to be in the 2nd paren. group of the regex
    # associated with this handler
    bedtime_string = groups[1]

    bedtime_string = bedtime_string.replace(':', '.')
    fields = bedtime_string.split('.')
    if len(fields) != 2:
        return "Can't understand time format, please use HH:MM format with 24 hours"

    try:
        hour = int(fields[0])
        minute = int(fields[1])
    except:
        return "Can't understand time format, please use HH:MM format with 24 hours"

    bedtime[0] = hour
    bedtime[1] = minute
    return "OK, I'll remember that your bedtime is %02d:%02d" % (hour, minute)

def bedtime_handler(groups):
    hour, minute = current_time()
    bedtime_hour, bedtime_minute = bedtime
    if not bedtime_hour:
        return "You haven't told me what your bedtime is yet."

    bedtimestr = "%02d:%02d" % (bedtime_hour, bedtime_minute)
    bedtime_td = timedelta(hours=bedtime_hour, minutes=bedtime_minute)
    now_td = timedelta(hours=hour, minutes=minute)

    # Assuming your bedtime is at night...
    if (now_td < bedtime_td) and (hour <= 5):
        return "Yes, your bedtime was at %s" % bedtimestr

    if (now_td > bedtime_td) and (bedtime_hour <= 5):
        return "No, your bedtime is at %s" % bedtimestr

    if now_td < bedtime_td:
        return "No, your bedtime is at %s" % bedtimestr

    if now_td > bedtime_td:
        return "Yes, your bedtime was at %s" % bedtimestr

    return "Your bedtime is now!"

def default_handler(groups):
    return "I don't understand that"

responder = Responder()

responder.add_responses(
    (["(.* )?bedtime is (.*).*"], set_bedtime_handler),
    (["(.* )?(what|when).*bedtime.*"], ask_bedtime_handler),
    (["(.* )?what( time is it|( i|'?)s the time).*"], current_time_handler),
    (["(.* )?(is )?(that|it) past (my )?bedtime.*"], bedtime_handler)
)

responder.add_default_response(default_handler)

# Simple prompt to get input from command line and pass to responder
while True:
    text = raw_input(" > ")
    handler, groups = responder.get_response(text)
    response = handler(groups)
    print("\n\"%s\"\n" % response)
