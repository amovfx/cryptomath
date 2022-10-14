from FieldElement.FieldElement import FieldElement as FE
import pytest


@pytest.fixture()
def resource():
    print("setup")
    FE = FieldElement(1, 17)
    yield FE
    print("teardown")


def test_pow():
    a = FE(2, 11)
    b = FE(8, 11)

    assert a**b == pow(2, 8, 11)
    assert a**8 == pow(2, 8, 11)


def test_mul():
    a = FE(1234, 13)
    b = FE(7, 13)
    assert a * b == 1234 * 7 % 13
    assert a * 7 == 1234 * 7 % 13


def test_truediv():
    a = FE(1234, 13)
    b = FE(7, 13)

    assert a / b == (1234 * pow(7, 13 - 2, 13)) % 13
    assert a // b == (1234 * pow(7, 13 - 2, 13)) % 13


def test_add():
    a = FE(2, 11)
    b = FE(20, 11)
    assert a + b == (2 + 20) % 11


def test_sub():
    a = FE(2, 5)
    b = FE(4, 5)
    assert a - b == (2 - 4) % 5


def test_eq():
    a = FE(4, 5)
    b = FE(4, 5)
    assert a == b
    assert a == 4

def test_neq():
    a = FE(3, 5)
    b = FE(4, 5)
    assert a != b
    assert a != 4

def test_gt():
    a = FE(2, 11)
    b = FE(1, 11)
    assert a > b
    assert a > 1

def test_ge():
    a = FE(9, 11)
    b = FE(9, 11)
    c = FE(8, 11)
    d = FE(10, 11)
    assert a >= b
    assert a >= 9
    assert a >= c
    assert d >= b

def test_lt():
    a = FE(5, 11)
    b = FE(1, 11)
    assert b < a
    assert b < 5

def test_le():
    a = FE(8, 9)
    b = FE(5, 9)
    c = FE(8, 9)
    assert a <= 8
    assert b <= a
    assert a <= c

def test_repr():
    a = FE(1, 13)
    assert repr(a) == '<FieldElement[1|13]>'

