import os
import threading
from statsmodels.stats.weightstats import DescrStatsW
from random import seed
from datetime import datetime

FIVE_MINUTES = 5 * 60


def memory_usage():
    import psutil, time
    while True:
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / float(2 ** 20)
        print(f"{datetime.now().time()}: {mem} Mb")
        time.sleep(FIVE_MINUTES)


# Uses the current seed to time one invocation to f
def time_call(f):
    import time
    print(f"Starting at {datetime.now().time()}")
    start = time.process_time()
    f()
    delta = time.process_time() - start
    print(f"f={f}, delta={delta}")
    return delta


# Sets the seed once and times k invocations
def time_calls(f, k, seed_number, plot_memory=False):
    if plot_memory:
        thread = threading.Thread(target=memory_usage)
        thread.start()

    seed(seed_number)
    results = []
    print(f"Running {f} {k} times with seed={seed_number}")
    for i in range(k):
        result = time_call(f)
        results.append(result)
    print(f"Results: {results}")
    return results
