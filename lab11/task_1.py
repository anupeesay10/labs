def zipmap(key_list, value_list, override=False):
    """
    Create a dictionary from two sequences.

    If override is True, duplicate keys will be overridden by the later value.
    If override is False, duplicates will be ignored.

    Args:
        key_list (list): The list of keys for the dictionary.
        value_list (list): The list of values for the dictionary.
        override (bool): Whether to allow overriding duplicate keys.

    Returns:
        dict: A dictionary mapping keys to values.
    """
    # Adjust the lengths of key_list and value_list using map
    min_len = min(len(key_list), len(value_list))
    max_len = max(len(key_list), len(value_list))

    # Use map to adjust the value_list to match the length of key_list
    value_list = list(map(lambda v, i: v if i < min_len else None, value_list, range(max_len)))

    # Create the dictionary with optional override functionality
    result = {}
    for key, value in zip(key_list, value_list):
        if override or key not in result:
            result[key] = value

    # Handle the case when key_list is longer than value_list by adding None for missing values
    if len(key_list) > len(value_list):
        for key in key_list[len(value_list):]:
            result[key] = None

    return result


# Example usages:
print(zipmap(['a', 'b', 'c', 'd', 'e', 'f'], [1, 2, 3, 4, 5, 6]))  # Expected: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], True))  # Expected: {1: 4, 2: 7, 3: 6}
print(zipmap([1, 2, 3], [4, 5, 6, 7, 8]))  # Expected: {1: 4, 2: 5, 3: 6}
print(zipmap([1, 3, 5, 7], [2, 4, 6]))  # Expected: {1: 2, 3: 4, 5: 6, 7: None}

