import glob
from scipy.stats import ranksums
import numpy as np
from statsmodels.stats.diagnostic import normal_ad
from statsmodels.stats.proportion import proportion_confint

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from statsmodels.stats.weightstats import DescrStatsW

from spaces import space_optimized, space_full
from tester import check


def summarize(name, test=False, space_creator=space_optimized):
    print("---------------------")
    print(f"{name}> summarizing")
    files = list(glob.glob(f"output/{name}/*_results.txt"))
    print(f"{name}> {len(files)} files found")

    failed = 0
    timed_out = 0
    memory_error = 0

    results = []
    for file in files:
        log_file = file.replace("_results.txt", "_log.txt")
        with open(log_file) as f:
            lines = "\n".join(f.readlines())
            if "out of memory" in lines:
                failed += 1
                memory_error += 1
                print(f"{name}> {log_file} out of memory")
                continue

        with open(file) as f:
            lines = f.readlines()
            time_taken = int(lines[3]) / 1000 / 60  # minutes
            if lines[5].startswith("False"):
                print(f"{name}> {file} timed out")
                failed += 1
                timed_out += 1
                continue
            results.append(time_taken)

        if test:
            check(log_file, stop_on_error=True, space_creator=space_creator)

    success_count = len(results)

    print(f"{name}> {success_count} successes")
    if success_count != 0:
        d = DescrStatsW(results)
        print(f"{name}> mean={d.mean}, std_mean={d.std_mean}")
        print(f"{name}> confidence interval", d.tconfint_mean())
    print(f"{name}> {failed} failed, {failed / (success_count + failed) * 100}%")
    print(f"{name}> {timed_out} timed out")
    print(f"{name}> {memory_error} memory error")
    print(f"{name}> binomial success ci={proportion_confint(success_count, success_count + failed, method='wilson')}")

    frame = frame_of(results, name)
    plt.figure()
    sns.boxplot(data=frame, y="time")
    plt.savefig(f"output/fig{name}.png")

    plt.figure()
    sns.displot(frame["time"])
    plt.ylim(0, 350)
    plt.savefig(f"output/fig{name}-dist.png")

    return results


def frame_of(results, name):
    f = pd.DataFrame({'time': results})
    f['source'] = name
    return f


# Compare results
def compare_results(name1, name2, r1, r2):
    print("---------------------")
    print(f"{name1},{name2}> Comparison statistics")
    print(normal_ad(np.array(r1)))
    print(normal_ad(np.array(r2)))

    d1 = DescrStatsW(r1)
    print(d1.get_compare(r2).summary(use_t=True, usevar='unequal'))
    print(f"{name1},{name2}>", ranksums(r1, r2))

    f1 = frame_of(r1, name1)
    f2 = frame_of(r2, name2)
    frame = pd.concat([f1, f2])

    plt.figure()
    sns.boxplot(data=frame, x="source", y="time")
    plt.savefig(f"output/fig{name1}x{name2}.png")


sns.set_theme(style="whitegrid")

# phase 1 is the baseline for generating rules
# phase1a = summarize("phase1a")
# phase1b = summarize("phase1b")

# remove test=True for quick reporting purposes
# phase2a = summarize("phase2a", test=True)
# phase2b = summarize("phase2b", test=True)
# phase3a = summarize("phase3a", test=True)

# remove test=True for quick reporting purposes
# phase4a = summarize("phase4a")
# phase4b = summarize("phase4b")
# phase4a = summarize("phase4a", test=True)
# phase4b = summarize("phase4b", test=True)
# compare_results("English_Optimized", "English_Optimized_Distinct", phase4a, phase4b)

# remove test=True for quick reporting purposes
# phase5a = summarize("phase5a", space_creator=space_full)
# phase5b = summarize("phase5b", space_creator=space_full)
# phase5c = summarize("phase5c", space_creator=space_full)
# phase5a = summarize("phase5a", space_creator=space_full, test=True)
# phase5b = summarize("phase5b", space_creator=space_full, test=True)
# phase5c = summarize("phase5c", space_creator=space_full, test=True)
