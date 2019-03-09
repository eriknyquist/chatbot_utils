import time
import random
from chatbot_utils.redict import ReDict

import matplotlib.pyplot as plt

random.seed(time.time())

def plot(xdata, ydata, xlabel=None, ylabel=None, legend=None):
    for y in ydata:
        plt.plot(xdata, y)

    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if legend:
        plt.legend(legend)

    plt.show()

def test_redict_speed(num_items, start=0, dictobj=None):
    if dictobj is None:
        d = ReDict()
    else:
        d = dictobj

    num_regexs = 1

    for i in range(start, start + num_items):
        d["(f)(o)o? %d|b((a)(r)*) %d" % (i, i)] = i

    compile_start = time.time()
    d.compile()
    compile_time = time.time() - compile_start

    if num_items == 0:
        num_get_tests = 100
    else:
        num_get_tests = num_items / 10

    get_time = 0.0
    for _ in range(num_get_tests):
        index = random.randrange(0, len(d))
        text = "barrr %d" % index
        get_start = time.time()
        value = d[text]
        get_time += time.time() - get_start

    return compile_time, get_time / float(num_get_tests)

step = 1000
max_value = 25000

iterations = max_value / step
compile_times = []
get_times = []

d = ReDict()
for i in range(iterations):
    compile_time, get_time = test_redict_speed(step, step * i, d)
    compile_times.append(compile_time)
    get_times.append(get_time)

# worst caseno, chunking, 7.15 secs to compile with 25000 groups
# better, chunking 600, 4.5 secs with 25000 groups
# best (!), chunking 75, builtin 're' lib, 1.65 secs with 25000 groups
test_values = range(0, max_value, step)
plot(test_values, [compile_times, get_times],
    xlabel="Number of items in ReDict instance",
    ylabel="Time in seconds",
    legend=[
        'Time to compile ReDict instance',
        'Time to fetch item from compiled ReDict'
    ]
)
