from FieldElement.FieldElement import FieldElement as FE
from FieldElement.Point import Point, KeyPair, GeneratorPoint
from FieldElement.Constants import SECP256K1

import pytest


def test_curve():
    p = Point(-1,1,5,7)
    assert p.onCurve()

def test_typemistmatch():
    
    with pytest.raises(TypeError):
        p1 = Point(FE(12,106),1,2,3)


def test_eq():
    p1 = Point(FE(17,103), FE(64,103),FE(0,103),FE(7,103))
    p2 = Point(FE(17,103), FE(64,103),FE(0,103),FE(7,103))
    assert p1 == p2

def test_on_curve():
    # tests the following points whether they are on the curve or not
    # on curve y^2=x^3-7 over F_223:
    # (192,105) (17,56) (200,119) (1,193) (42,99)
    # the ones that aren't should raise a ValueError
    prime = 223
    a = FE(0, prime)
    b = FE(7, prime)

    valid_points = ((192, 105), (17, 56), (1, 193))
    invalid_points = ((200, 119), (42, 99))

    # iterate over valid points
    for x_raw, y_raw in valid_points:
        x = FE(x_raw, prime)
        y = FE(y_raw, prime)
        # Creating the point should not result in an error
        Point(x, y, a, b)

    # iterate over invalid points
    for x_raw, y_raw in invalid_points:
        x = FE(x_raw, prime)
        y = FE(y_raw, prime)
        with pytest.raises(ValueError):
            Point(x, y, a, b)

def test_ne():
    p1 = Point(FE(17,103), FE(64,103),FE(0,103),FE(7,103))
    p2 = Point(FE(16,103), FE(64,103),FE(0,103),FE(7,103))
    p3 = Point(FE(17,103), FE(65,103),FE(0,103),FE(7,103))
    print(vars(p1))
    assert p1 != p2
    assert p1 != p3

def test_add():
    # tests the following additions on curve y^2=x^3-7 over F_223:
    # (192,105) + (17,56)
    # (47,71) + (117,141)
    # (143,98) + (76,66)
    prime = 223
    a = 0
    b = 7

    additions = (
        # (x1, y1, x2, y2, x3, y3)
        (192, 105, 17, 56, 170, 142),
        (47, 71, 117, 141, 60, 139),
        (143, 98, 76, 66, 47, 71),
    )
    # iterate over the additions
    for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
        x1 = FE(x1_raw, prime)
        y1 = FE(y1_raw, prime)
        p1 = Point(x1, y1, a, b)
        x2 = FE(x2_raw, prime)
        y2 = FE(y2_raw, prime)
        p2 = Point(x2, y2, a, b)
        x3 = FE(x3_raw, prime)
        y3 = FE(y3_raw, prime)
        p3 = Point(x3, y3, a, b)
        # check that p1 + p2 == p3
        assert p1 + p2 == p3

def test_neg():
    a = FE(1,7)
    assert -a == FE(-1,7)


def test_KeyPair():
    a = SECP256K1.Gx
    priv_key1 = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000006")
    priv_key1_int = int.from_bytes(priv_key1,byteorder='big')
    G = GeneratorPoint()
    pubkey = priv_key1_int * G
    pubkey2 = pubkey.lift_x()
    assert pubkey == pubkey2

def test_verify_schnorr():
    kp = KeyPair()
    msg = "hello world"
    s = kp.sign(msg)
    result = kp.verify(msg, s,kp.pubkey)
    assert result == True


def test_verify_schnorr_tweak():
    kp = KeyPair()
    msg = "hello world"
    s, R = kp.sign(msg)
    result = kp.verify(msg, s, R)
    assert result == True
    msg2 = "hello world2"
    s2, R2 = kp.sign(msg2)
    result2 = kp.verify(msg2, s2, R2)
    assert result2 == True





