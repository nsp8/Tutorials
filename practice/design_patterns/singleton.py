class SingletonMeta(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonClass(metaclass=SingletonMeta):
    pass


def test_singleton():
    instance1 = SingletonClass()
    instance2 = SingletonClass()
    assert instance1 is instance2
