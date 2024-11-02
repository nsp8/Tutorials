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
