from FieldElement.FieldElement import FieldElement as FE
import pytest

@pytest.fixture()
def resource():
    print("setup")
    FE = FieldElement(1,17)
    yield FE
    print("teardown")

def test_pow():
    a = FE(2,11)
    b = FE(8, 11)

    assert a ** b == pow(2,8,11)
    assert a ** 8 == pow(2,8,11)



def test_mul():
    a = FE(1234,13)
    b = FE(7,13)
    assert a*b == 1234*7%13
    assert a*7 == 1234*7%13

def test_truediv():
    a = FE(1234,13)
    b = FE(7,13)

    assert a / b == (1234*pow(7, 13-2, 13)) % 13
    assert a // b == (1234*pow(7, 13-2, 13)) % 13


def test_add():
    a = FE(2,11)
    b = FE(20,11)
    assert a + b == (2 + 20) % 11

def test_sub():
    a = FE(2, 5)
    b = FE(4, 5)
    assert a-b == (2-4)%5



def test_eqint(resource):
    assert resource == 1

def test_nqint(resource):
    assert resource != 2

def test_addint(resource):
    assert resource + 4 == 5

def test_addinvint(resource):
    new_f = resource - 1
    print(new_f)
    assert resource - 1 == 0

def test_multint(resource):
    assert resource * 45 == 45 %17

def test_divint():
    FE = FieldElement
