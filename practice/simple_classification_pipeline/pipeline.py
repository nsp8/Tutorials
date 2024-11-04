class Pipeline:
    def __init__(self, input_stream_generator):
        self.input_stream = input_stream_generator
        self.results = []

    @staticmethod
    def normalize(value, min_value, max_value):
        return (value - min_value) / (max_value - min_value)

    @staticmethod
    def classify(value):
        if 0 <= value < .25:
            return [1, 0, 0, 0]
        elif .25 <= value < 0.5:
            return [0, 1, 0, 0]
        elif .5 <= value < 0.75:
            return [0, 0, 1, 0]
        elif .75 <= value <= 1:
            return [0, 0, 0, 1]
        else:
            raise ValueError("Value needs to be within [0, 1].")

    def run(self):
        valid_values = []
        for input_value in self.input_stream():
            if isinstance(input_value, (int, float)):
                valid_values.append(input_value)
            elif isinstance(input_value, (tuple, float)):
                valid_values.extend([
                    x for x in input_value
                    if isinstance(x, (int, float))
                ])
        if valid_values:
            _last_100 = valid_values[-100:]
            _min, _max = min(_last_100), max(_last_100)
            for value in valid_values:
                normalized = Pipeline.normalize(value, _min, _max)
                classified = Pipeline.classify(normalized)
                self.results.append((normalized, classified))

    def display(self):
        for result in self.results:
            print(f"input: {result[0]}, class: {result[1]}")

    def save(self, run_id):
        import json
        data = {run_id: self.results}
        with open(f"{run_id}.json", "w") as f:
            json.dump(data, f, indent=2)


def input_stream():
    yield 10
    yield [20, 30.86, "test"]
    yield (15, 50, None, 25.5)


def main():
    pipeline = Pipeline(input_stream)
    pipeline.run()
    pipeline.display()
    pipeline.save("test_run")


if __name__ == "__main__":
    main()
