from functools import lru_cache
from time import perf_counter


@lru_cache(maxsize=100)
def fibonacci(n):
    if n in {0, 1}:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def print_cached_fibonacci(iters=10):
    t0 = perf_counter()
    for i in range(iters):
        print(f"[{i=}]: F={fibonacci(i)}")
    print(f"{perf_counter() - t0:.2f} sec.")


if __name__ == "__main__":
    print_cached_fibonacci(iters=100)
