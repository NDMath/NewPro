import pandas as pd
import numpy as np


def generate_random_number() -> int:
    """
    Generates a random integer between 1 and 100 (inclusive).

    Returns:
        int: The randomly generated integer.
    """
    return np.random.randint(low=1, high=101)


if __name__ == "__main__":
    print(f"Random number: {generate_random_number()}")
