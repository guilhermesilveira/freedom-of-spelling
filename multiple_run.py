import subprocess
import sys
from multiprocessing import Pool
import random
import os

from time_information import *


def creator(k, seed_number, name, python_path: str = "python"):
    path = f"output/{name}/"
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/_{k}_log.txt", "w") as log_file:
        with open(f"{path}/_{k}_error.txt", "w") as error_file:
            start_time = current_milliseconds()
            args_to_invoke = [python_path, 'seed_and_invoke.py', str(seed_number), name]
            print(f"{k}> Ready to run", args_to_invoke)
            try:
                result = subprocess.run(args_to_invoke,
                                        stdout=log_file,
                                        stderr=error_file,
                                        timeout=FOUR_HOURS)
                success = result.returncode == 0
                success_message = ""
                return_code = result.returncode
            except subprocess.TimeoutExpired as err:
                success = False
                success_message = str(err)
                return_code = ""
            finish_time = current_milliseconds()
            print(f"{k}> Finished")

            # writes results
            with open(f"{path}/_{k}_results.txt", "w") as results_file:
                print(seed_number, file=results_file)
                print(start_time, file=results_file)
                print(finish_time, file=results_file)
                print(finish_time - start_time, file=results_file)
                print(return_code, file=results_file)
                print(success, file=results_file)
                print(success_message, file=results_file)


def start(function_name: str, repeat_count: int, python_path: str, workers: int = 1, starting_at=1):
    seed_number = 6798
    random.seed(seed_number)

    processes = []

    # generate all seeds
    seeds = []
    for i in range(repeat_count):
        # python int is unbounded
        seed_number = random.randint(-1000000000, 1000000000)
        seeds.append(seed_number)

    with Pool(processes=workers, maxtasksperchild=1) as pool:
        for i in range(starting_at, repeat_count + 1):
            processes.append(pool.apply_async(creator, args=(i, seeds[i - 1], function_name, python_path)))
        for process in processes:
            process.wait()
            if not process.successful:
                print("Error")
                process.get()
        print("Finishing waits")
        pool.close()
        pool.join()
        print("Finishing join")


def main():
    args = sys.argv[1:]
    python_path = args[0]
    function_name = args[1]
    repeat_count = int(args[2])
    workers = int(args[3])
    if len(args) >= 5:
        starting_at = int(args[4])
    else:
        starting_at = 1
    start(function_name, repeat_count, python_path, workers, starting_at)


if __name__ == "__main__":
    main()
