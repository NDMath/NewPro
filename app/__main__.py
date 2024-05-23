import pandas as pd
import numpy as np


def random() -> int:
    return np.random.randint(1, 100)


if __name__ == "__main__":
    print(f"{pd.__name__}: {pd.__version__}")
    print(f"{np.__name__}: {np.__version__}")
    print(f"Random number: {random()}")
