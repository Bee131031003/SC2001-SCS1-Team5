import random

def generate_random_array(size, max_val=None):
    # if no input value for max_val, max_val = size
    if max_val is None:
        max_val = size

    result_array = []

    for i in range(size):
        random_num = random.randint(1, max_val)
        result_array.append(random_num)

    return result_array
