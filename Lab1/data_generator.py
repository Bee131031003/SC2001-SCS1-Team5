import random

def generate_random_array(size):
    max_val = 10000000
    result_array = []
    for step in range(size):
        random_num = random.randint(1, max_val)
        result_array.append(random_num)
    return result_array
