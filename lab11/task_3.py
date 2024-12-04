from functools import reduce

def filter_using_reduce(func, target_list):
    """
    Implements filter() using reduce() to accumulate elements that satisfy func.

    Args:
        func (function): A function that returns True or False, used to filter the list.
        target_list (list): The list of elements to filter.

    Returns:
        list: A list of elements that satisfy func.
    """
    return reduce(lambda acc, item: acc + [item] if func(item) else acc, target_list, [])

# Example usage:
print(filter_using_reduce(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))  # Expected: [2, 4, 6]
