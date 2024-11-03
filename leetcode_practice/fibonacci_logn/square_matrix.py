from copy import deepcopy
from dataclasses import dataclass
from leetcode_practice.fibonacci_logn import utils


@dataclass
class SquareMatrix:
    def __init__(self, *args, size: int):
        if len(args) < size ** 2:
            raise ValueError(f"Insufficient values for {size=}")
        self.vector = []
        self.size = size
        for row in range(size):
            i = (size - 1) * row
            for col in range(size):
                value = args[row + col + i]
                try:
                    self.vector[row].append(value)
                except IndexError:
                    self.vector.append([value])

    @staticmethod
    def from_list(array: list[list]):
        if isinstance(array, list):
            return SquareMatrix(*[x for v in array for x in v], size=len(array))
        raise ValueError("Input has to be a list!")

    def __len__(self):
        return self.size ** 2

    def __getitem__(self, item: int):
        if not isinstance(item, int) or item < 0:
            raise ValueError("index must be a positive integer")
        return self.vector[item]

    def __mul__(self, other):
        if isinstance(other, SquareMatrix):
            if self.size == other.size:
                if self.size in utils.PREDEFINED_FUNCTIONS:
                    f = utils.PREDEFINED_FUNCTIONS[self.size]
                    return SquareMatrix.from_list(f(self.vector, other.vector))
                else:
                    return square_matrix_multiplication(self, other)
            raise ValueError("Square matrices should have the same size")
        raise ValueError("Other argument has to be a SquareMatrix")

    @staticmethod
    def identity(n):
        matrix = [0] * (n ** 2)
        one_pos = [(n + 1) * i for i in range(n)]
        for pos in one_pos:
            matrix[pos] = 1
        return SquareMatrix(*matrix, size=n)

    def __pow__(self, power, modulo=None):
        result = SquareMatrix.identity(n=self.size)
        base = self
        while power > 0:
            if power % 2 == 1:
                result *= base
            base *= base
            power //= 2
        return result


def square_matrix_multiplication(a: SquareMatrix, b: SquareMatrix) -> SquareMatrix:
    c = deepcopy(a)
    for row in range(a.size):
        for col in range(b.size):
            v = [a.vector[row][k] * b.vector[k][col] for k in range(a.size)]
            c.vector[row][col] = sum(v)
    return c


def fibonacci(n):
    if n in (0, 1):
        return n
    matrix = SquareMatrix(1, 1, 1, 0, size=2) ** (n - 1)
    return matrix[0][0]
