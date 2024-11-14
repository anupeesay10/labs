def product_of_digits(x):
    # Take the absolute value to ignore the negative sign
    x = abs(x)

    # Base case: if x is a single digit (0-9), return x
    if x < 10:
        return x

    # Recursive case: multiply the last digit (x % 10) by the product of the remaining digits (x // 10)
    return (x % 10) * product_of_digits(x // 10)

def array_to_string(a, index=0):
    # Base case: if we've reached the last element in the list, return that element as a string
    if index == len(a) - 1:
        return str(a[index])

    # Recursive case: convert the current element to a string and add a comma,
    # then concatenate with the result of the next recursive call
    return str(a[index]) + ',' + array_to_string(a, index + 1)

def log(base, value):
    # Check for invalid input and raise an error if needed
    if value <= 0 or base <= 1:
        raise ValueError("Value must be greater than 0 and base must be greater than 1.")

    # Base case: if value is less than the base, we can't divide further, so the result is 0
    if value < base:
        return 0

    # Recursive case: divide value by base, adding 1 for each recursive call
    return 1 + log(base, value // base)

def main():
    print(product_of_digits(27))
    print(array_to_string([1, 2, 3, 4], 0))
    print(log(2, 64))

if __name__ == "__main__":
    main()


