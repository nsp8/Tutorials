from leetcode_practice import utils
from leetcode_practice.square_matrix import SquareMatrix


def test_mul2_different(matrix2):
    data = [7, 10, 15, 22]
    result = SquareMatrix(*data, size=2).vector
    assert result == utils.mul2(matrix2.vector, matrix2.vector)


def test_mul3_different(matrix3):
    data = [30, 36, 42, 66, 81, 96, 102, 126, 150]
    result = SquareMatrix(*data, size=3).vector
    assert result == utils.mul3(matrix3.vector, matrix3.vector)


def test_mul2_with_identity(identity_matrix2, matrix2):
    assert utils.mul2(identity_matrix2.vector, matrix2.vector) == matrix2.vector
    assert utils.mul2(
        identity_matrix2.vector, identity_matrix2.vector
    ) == identity_matrix2.vector


def test_mul3_with_identity(identity_matrix3, matrix3):
    assert utils.mul3(identity_matrix3.vector, matrix3.vector) == matrix3.vector
    assert utils.mul3(
        identity_matrix3.vector, identity_matrix3.vector
    ) == identity_matrix3.vector
