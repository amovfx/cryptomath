from FieldElement.FieldElement import FieldElement as FE, S256Field
from FieldElement.Constants import SECP256K1
import pytest


class TestField:

    def test_pow(self):
        a = FE(2, 11)
        b = FE(8, 11)
        assert a**8 == pow(2, 8, 11)
        assert a**b == pow(2, 8, 11)


    def test_mul(self):
        a = FE(1234, 13)
        b = FE(7, 13)
        assert a * b.value == 1234 * 7 % 13
        assert a * 7 == 1234 * 7 % 13


    def test_truediv(self):
        a = FE(1234, 13)
        b = FE(7, 13)

        assert a / b.value == (1234 * pow(7, 13 - 2, 13)) % 13
        assert a // b.value == (1234 * pow(7, 13 - 2, 13)) % 13


    def test_add(self):
        a = FE(2, 11)
        b = FE(20, 11)
        assert a + b == (2 + 20) % 11


    def test_sub(self):
        a = FE(2, 5)
        b = FE(4, 5)
        assert a - b == (2 - 4) % 5


    def test_eq(self):
        a = FE(4, 5)
        b = FE(4, 5)
        assert a == b
        assert a == 4

    def test_neq(self):
        a = FE(3, 5)
        b = FE(4, 5)
        assert a != b
        assert a != 4

    def test_gt(self):
        a = FE(2, 11)
        b = FE(1, 11)
        assert a > b
        assert a > 1

    def test_ge(self):
        a = FE(9, 11)
        b = FE(9, 11)
        c = FE(8, 11)
        d = FE(10, 11)
        assert a >= b
        assert a >= 9
        assert a >= c
        assert d >= b

    def test_lt(self):
        a = FE(5, 11)
        b = FE(1, 11)
        assert b < a
        assert b < 5

    def test_le(self):
        a = FE(8, 9)
        b = FE(5, 9)
        c = FE(8, 9)
        assert a <= 8
        assert b <= a
        assert a <= c

    def test_and(self):
        a = FE(4, 13)
        b = FE(5, 13)
        assert a & 0 == 0
        assert b & 1 == 1

    def test_repr(self):
        a = FE(1, 13)
        assert repr(a) == '<FE[1|13]>'

class TestS256Field:

    def test_sqrt(self):
        a = S256Field(4)
        assert a.sqrt() == 2

    def test_neg(self):
        a = S256Field(4)
        assert -a == SECP256K1.P - 4

    def test_repr(self):
        a = S256Field(4)
        return repr(a) == '<S256Field[4]>'


