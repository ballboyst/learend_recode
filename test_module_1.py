from module_1 import add_numbers


def test_add_numbers_1():
    assert add_numbers(1, 2) == 3
    assert add_numbers(0, 0) == 0


def test_numbers_2():
    assert add_numbers(-1, -2) == -3
