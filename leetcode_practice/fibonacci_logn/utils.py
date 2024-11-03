def mul2(a: list[list], b: list[list]):
    print(f"Calling predefined multiplication for order=2")
    return [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0], 
            a[0][0] * b[0][1] + a[0][1] * b[1][1]
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0], 
            a[1][0] * b[0][1] + a[1][1] * b[1][1]
        ]
    ]


def mul3(a: list[list], b: list[list]):
    print(f"Calling predefined multiplication for order=3")
    return [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
            a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2],
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
            a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2],
        ],
        [
            a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
            a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
            a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2],
        ],
    ]


PREDEFINED_FUNCTIONS = {
    2: mul2,
    3: mul3
}
