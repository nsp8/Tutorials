# NumExpr

---
NumExpr is a great library that accelerated Numpy and Pandas numerical expression processing, while abstracting most of the implementation in its powerful and simple API.

## Run this script to see the example
1. Activate a Python interpreter
2. Install the libraries using `requirements.txt` in the base directory
3. Run the script: 
```commandline
python -m neural_nine.fast_num_expr.main
```
> This example script uses 100,000,000 values to test the power of `numexpr`

Output:
```
---------[slow_numpy]---------
Time taken: 1.60606 seconds
------------------------------

---------[fast_numpy]---------
Time taken: 0.89279 seconds
------------------------------

--------[slow_pandas]--------
Time taken: 2.50102 seconds
------------------------------
          A         B         C         D         E           F           G
0  0.788390  0.113693  0.018131  0.610436  0.601347    0.002061    0.601351
1  0.441396  0.159651  0.777964  0.024773  4.470314    0.056123    4.470666
2  0.429309  0.366351  0.314570  0.829642  0.653446    1.932508    2.039994
3  0.858404  0.200442  0.139783  0.915330  0.399859    0.028018    0.400839
4  0.004134  0.780792  0.866913  0.829080  0.953001  200.537885  200.540149

--------[fast_pandas]--------
Time taken: 0.85235 seconds
------------------------------
          A         B         C         D         E           F           G
0  0.788390  0.113693  0.018131  0.610436  0.601347    0.002061    0.601351
1  0.441396  0.159651  0.777964  0.024773  4.470314    0.056123    4.470666
2  0.429309  0.366351  0.314570  0.829642  0.653446    1.932508    2.039994
3  0.858404  0.200442  0.139783  0.915330  0.399859    0.028018    0.400839
4  0.004134  0.780792  0.866913  0.829080  0.953001  200.537885  200.540149
```