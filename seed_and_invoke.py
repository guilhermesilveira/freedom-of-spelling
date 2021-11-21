import random
import sys
from datetime import datetime
from importlib import import_module


def main(argv):
    seed_number = int(argv[1])
    name = argv[2]

    print(f"Command line arguments were {argv}")
    print(f"Starting at {datetime.now().time()}")
    print(f"Using seed {seed_number} for {name}")
    random.seed(seed_number)
    print("Running at ", datetime.now().time())
    import_module(name)


if __name__ == "__main__":
    main(sys.argv)
