import pytest
from practice.fibonacci_logn.square_matrix import (
    SquareMatrix,
    square_matrix_multiplication,
    fibonacci
)


def test_insufficient_data():
    with pytest.raises(ValueError):
        SquareMatrix(1, 2, 3, size=2)


def test_creation_from_list(matrix3):
    matrix = SquareMatrix.from_list([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert matrix.size == 3
    assert matrix == matrix3


def test_get_from_index(matrix2):
    assert matrix2[0][0] == 1
    assert matrix2[0][1] == 2
    assert matrix2[1][0] == 3
    assert matrix2[1][1] == 4
    with pytest.raises(ValueError):
        _ = matrix2[-1]


def test_multiplication2(matrix2):
    with pytest.raises(ValueError):
        _ = matrix2 * 2
    assert square_matrix_multiplication(matrix2, matrix2) == matrix2 * matrix2


def test_multiplication3(matrix3):
    with pytest.raises(ValueError):
        _ = matrix3 * 2
    assert square_matrix_multiplication(matrix3, matrix3) == matrix3 * matrix3


def test_identity_exponentiation2(identity_matrix2):
    assert identity_matrix2 ** 2 == identity_matrix2
    assert identity_matrix2 ** 3 == identity_matrix2
    assert identity_matrix2 ** 4 == identity_matrix2


def test_identity_exponentiation3(identity_matrix3):
    assert (identity_matrix3 ** 2) == identity_matrix3
    assert (identity_matrix3 ** 3) == identity_matrix3
    assert (identity_matrix3 ** 4) == identity_matrix3


def test_identity2(identity_matrix2):
    assert SquareMatrix.identity(n=2) == identity_matrix2


def test_identity3(identity_matrix3):
    assert SquareMatrix.identity(n=3) == identity_matrix3


def test_matrix_exponentiation2(matrix2):
    expected = SquareMatrix(7, 10, 15, 22, size=2)
    assert matrix2 ** 2 == expected


def test_matrix_exponentiation3(matrix3):
    data = [30, 36, 42, 66, 81, 96, 102, 126, 150]
    expected = SquareMatrix(*data, size=3)
    assert matrix3 ** 2 == expected


def test_base_matrix_exponentiation():
    base = SquareMatrix(1, 1, 1, 0, size=2)
    assert base ** 2 == SquareMatrix(5, 3, 3, 2, size=2)
    assert base ** 3 == SquareMatrix(8, 5, 5, 3, size=2)
    assert base ** 4 == SquareMatrix(13, 8, 8, 5, size=2)


def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5
    assert fibonacci(6) == 8
    assert fibonacci(7) == 13
    assert fibonacci(8) == 21
    assert fibonacci(9) == 34
