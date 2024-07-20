from time import perf_counter
import numpy as np
import pandas as pd
import numexpr


def time_it(f):
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        r = f(*args, **kwargs)
        t_diff = perf_counter() - t0
        n = 30 - len(f.__name__) - 2
        s = f"{'-' * (n//2)}[{f.__name__}]{'-' * (n//2)}"
        print(f"\n{s}\nTime taken: {t_diff:.5f} seconds\n{'-' * 30}")
        return r
    return wrapper


@time_it
def slow_numpy(num_items: int = 100_000_000):
    a = np.random.rand(num_items)
    b = np.random.rand(num_items)
    return a * b + np.sin(a)


@time_it
def fast_numpy(num_items: int = 100_000_000):
    a = np.random.rand(num_items)
    b = np.random.rand(num_items)
    return numexpr.evaluate("a * b + sin(a)", local_dict=locals())


def create_dataset(num_items: int = 100_000_000) -> pd.DataFrame:
    return pd.DataFrame({
        "A": np.random.rand(num_items),
        "B": np.random.rand(num_items),
        "C": np.random.rand(num_items),
        "D": np.random.rand(num_items),
    })


@time_it
def slow_pandas(df):
    df["E"] = df["A"] * df["B"] + np.sin(df["C"]) - np.log(df["D"])
    df["F"] = np.where(df["A"] > 0.5, df["B"] * df["C"], df["D"] / df["A"])
    df["G"] = (df["E"] ** 2 + df["F"] ** 2) ** 0.5
    return df


@time_it
def fast_pandas(df):
    A, B, C, D = df["A"].values, df["B"].values, df["C"].values, df["D"].values
    E = numexpr.evaluate("A * B + sin(C) - log(D)")
    F = numexpr.evaluate("where(A > 0.5, B * C, D / A)")
    G = numexpr.evaluate("(E ** 2 + F ** 2) ** 0.5")
    df["E"], df["F"], df["G"] = E, F, G
    return df


if __name__ == "__main__":
    slow_numpy()
    fast_numpy()
    dataframe = create_dataset()
    print(slow_pandas(dataframe).head())
    print(fast_pandas(dataframe).head())
