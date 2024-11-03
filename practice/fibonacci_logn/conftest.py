from pytest import fixture
from practice.fibonacci_logn.square_matrix import SquareMatrix


@fixture
def identity_matrix2():
    return SquareMatrix(1, 0, 0, 1, size=2)


@fixture
def identity_matrix3():
    return SquareMatrix(1, 0, 0, 0, 1, 0, 0, 0, 1, size=3)


@fixture
def matrix2():
    return SquareMatrix(1, 2, 3, 4, size=2)


@fixture
def matrix3():
    return SquareMatrix(*list(range(1, 10)), size=3)

