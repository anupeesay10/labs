from collections import defaultdict

def group_by(func, target_list):
    """
    Groups elements of a sequence based on the result of a given function.

    Args:
        func (function): A function to apply to each element.
        target_list (list): List of elements to group.

    Returns:
        dict: A dictionary where keys are results of func, and values are lists of elements.
    """
    grouped = defaultdict(list)  # Group elements by the function result
    for item in target_list:
        grouped[func(item)].append(item)

    return dict(grouped)  # Convert defaultdict to dict before returning


# Example usage:
print(group_by(len, ["hi", "dog", "me", "bad", "good"]))
# Expected output: {2: ['hi', 'me'], 3: ['dog', 'bad'], 4: ['good']}


