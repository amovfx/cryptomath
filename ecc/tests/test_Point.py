from typing import Type
from FieldElement.FieldElement import FieldElement as FE
from FieldElement.FieldElement import S256Field
from FieldElement.Point import Point, KeyPair, GeneratorPoint, S256Point
from FieldElement.Constants import SECP256K1

import pytest
import secrets


class TestECCPoint():

    def test_type_consisitency(self):
        with pytest.raises(TypeError):
            Point(1, FE(2, 11), FE(3, 11), FE(4, 11))
    
    def test_type_consisitency_int(self):  
        with pytest.raises(TypeError):
            Point(1.0,1,5,7)

    def test_on_curve(self):
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


def test_eq():
    p1 = Point(FE(17,103), FE(64,103),FE(0,103),FE(7,103))
    p2 = Point(FE(17,103), FE(64,103),FE(0,103),FE(7,103))
    assert p1 == p2



def test_ne():
    prime = 223
    x,y =(192, 105)
    x2,y2 =(17, 56)
    p1 = Point(FE(x,prime), FE(y,prime),FE(0,prime),FE(7,prime))
    p2 = Point(FE(x2,prime), FE(y2,prime),FE(0,prime),FE(7,prime))
    assert p1 != p2

def test_add():
    # tests the following additions on curve y^2=x^3-7 over F_223:
    # (192,105) + (17,56)
    # (47,71) + (117,141)
    # (143,98) + (76,66)
    prime = 223
    a = FE(0,prime)
    b = FE(7,prime)

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


def test_lift_x():
    a = SECP256K1.Gx
    priv_key1 = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000006")
    priv_key1_int = int.from_bytes(priv_key1,byteorder='big')
    G = GeneratorPoint()
    pubkey = priv_key1_int * G
    pubkey2 = pubkey.lift_x()
    assert pubkey == pubkey2

def test_point_regeneration():

    for i in range(20):
        kp = KeyPair()
        r = int.from_bytes(secrets.token_bytes(32), byteorder="big") % SECP256K1.ORDER-1
        R = kp.make_public_key(r)
        R= R.lift_x()

        P = S256Point(x=S256Field(R.x.value))
        P = P.lift_x()
        assert P == R

def test_256Point():
    x=13844178783120810765292313722011411873808158300720866139256509270287664762357
    y1 = 100089987570602369677569329480474179133361846904042450748411367069892173212242
    y2 = 15702101666713825746001655528213728719908137761598113291046216938016661459421
    a = S256Point(x=S256Field(x),y=S256Field(y1))
    b = S256Point(x=S256Field(x),y=S256Field(y2))
    c = -b
    assert a.x._num == x
    assert a.y._num == y1
    assert a == c
    assert a != b
    assert a == b.lift_x()



def test_verify_schnorr():
    kp = KeyPair()
    msg = "hello world"
    s = kp.sign(msg)

    assert s

def test_verify():
    kp = KeyPair()

    assert kp.sign_tweaked()


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





