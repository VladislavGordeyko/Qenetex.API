import random
import secrets
from typing import List


# Generate Hex string with n bytes
def generate_hex(n_bytes: int):
    return secrets.token_hex(n_bytes)


# Generate float number in min and max range
def generate_float(min_value: float = 0.01, max_value: float = 10000.0):
    return random.uniform(min_value, max_value)


# Get random elements from list
def pick_random_elements(ids: List[int], elements: int = 2):
    return random.sample(ids, elements)