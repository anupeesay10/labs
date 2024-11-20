import time

# Define the original Fibonacci function
def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return recur_fibo(n - 1) + recur_fibo(n - 2)

# Define a decorator for caching
def memoize(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

# Apply the decorator to the Fibonacci function
@memoize
def recur_fibo_memoized(n):
    if n <= 1:
        return n
    else:
        return recur_fibo_memoized(n - 1) + recur_fibo_memoized(n - 2)

# Measure execution time for both versions
n = 35

# Without memoization
start_time_original = time.time()
original_result = recur_fibo(n)
end_time_original = time.time()
time_original = end_time_original - start_time_original

# With memoization
start_time_memoized = time.time()
memoized_result = recur_fibo_memoized(n)
end_time_memoized = time.time()
time_memoized = end_time_memoized - start_time_memoized

# Display results and execution times
print(f"original result: {original_result}, original time: {time_original}, memoized result: {memoized_result}, memoized time: {time_memoized}")
