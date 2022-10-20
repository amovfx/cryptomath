from multiprocessing.sharedctypes import Value
from FieldElement.FieldElement import FieldElement as FE
from FieldElement.FieldElement import S256Field
from FieldElement.Constants import SECP256K1
from typing import Type, Optional
from operator import __eq__
import secrets
import hashlib


class Point:
    pass


class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if all(type(self.x) == type(var) for var in vars(self)):
            raise TypeError(f"Please initialize {self} with all same types.")

        if self.x is None and self.y is None:
            return

    def as_tuple(self):
        return (self.x, self.y, self.a, self.b)

    def to_bytes(self):
        self.x.num.to_bytes(32, byteorder="big")

    def onCurve(self) -> bool:
        return self.y * self.y == self.x ** 3 + self.a * self.x + self.b

    def __eq__(self, rhs: Type[Point]) -> Type[Point]:
        return all(getattr(self, var) == getattr(rhs, var) for var in vars(self))

    def __ne__(self, rhs: Type[Point]) -> Type[Point]:
        return not self.__eq__(rhs)

    def __add__(self, rhs: Type[Point]) -> Type[Point]:
        # When x == infinity and y == 0
        if self.x is None:
            return rhs
        if rhs.x is None:
            return self

        if self.x == rhs.x and self.y != rhs.y:
            return self.__class__(None, None, self.a, self.b)

        # when x1 != x2
        if self.x != rhs.x:
            slope = (rhs.y - self.y) / (rhs.x - self.x)
            x3 = slope**2 - self.x - rhs.x
            y3 = slope * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        # when x1 == x2
        if self == rhs:
            slope = (3 * self.x**2 + self.a) / (2 * self.y)
            x3 = slope**2 - 2 * self.x
            y3 = slope * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        if self == rhs and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

    def __rmul__(self, coefficient):
        assert(coefficient != 0)
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result

    def __neg__(self):
        if self.x is None:
            return self
        return self.__class__(self.x, -self.y, self.a, self.b)

    def __repr__(self):
        return f"<ECCPoint[{self.x},{self.y},{self.a},{self.b}]>"


class S256Point(Point):
    def __init__(
        self,
        x: Type[S256Field],
        y: Type[S256Field],
        a: Type[S256Field] = S256Field(SECP256K1.A.value),
        b: Type[S256Field] = S256Field(SECP256K1.B.value),
    ):

        super().__init__(
            x,
            y,
            a,
            b,
        )

    @classmethod
    def make_from_x(cls,x):
        x = S256Field(num=x)
        y_squared = x**3 + S256Field(SECP256K1.A.value) * x + S256Field(SECP256K1.B.value)
        y = y_squared.sqrt()
        return (
            S256Point(x=x, y=y)
            if y & 0
            else S256Point(x=x, y=(-y))
        )

    def __rmul__(self, coefficient):
        coef = coefficient % SECP256K1.ORDER
        return super().__rmul__(coef)

    def lift_x(self):
        y_squared = self.x**3 + self.a * self.x + self.b
        y = self.y.sqrt()
        if y_squared != y**2:
            return self

        return (
            self.__class__(x=self.x, y=self.y)
            if y & 0
            else self._class(x=self.x, y=-self.y)
        )


    def to_bytes(self):
        return self.x._num.to_bytes(32, byteorder="big")


class GeneratorPoint(S256Point):
    def __init__(
        self,
        x=S256Field(SECP256K1.Gx),
        y=S256Field(SECP256K1.Gy),
        a=S256Field(SECP256K1.A.value),
        b=S256Field(SECP256K1.B.value),
    ):
        super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        return "<GeneratorPoint>"


class KeyPair:
    def __init__(self):
        self.privkey = int.from_bytes(secrets.token_bytes(32), byteorder="big") % SECP256K1.ORDER-1
        self.G = GeneratorPoint()
        self.aux_rand = bytes(32)
        self.pubkey = self.make_public_key(self.privkey)

    def make_public_key(self,r):
        pub = r * self.G
        pub = pub.lift_x()
        return pub

    def get_priv(self):
        return self.privkey

    def H(self,msg):
        return int.from_bytes(hashlib.sha256(msg.encode('utf-8')).digest(), byteorder='big') % SECP256K1.ORDER

    def sign(self, msg):
        def sha256(msg):
            round1 = hashlib.sha256(msg).digest()
            return int.from_bytes(hashlib.sha256(round1).digest())

        hashed_message = self.H(msg)
        #k is random value from 1 to SECP256K1.ORDER-1
        r = int.from_bytes(secrets.token_bytes(32), byteorder="big") % SECP256K1.ORDER-1
        #r is the x coordinate of the point k*G
        R = self.make_public_key(r)  # r * G
        s = (r + hashed_message * self.privkey) % SECP256K1.ORDER
        return R.to_bytes() + s.to_bytes(32, byteorder="big")

    def verify(self, msg, sig, public_key):

        s = int.from_bytes(sig[32:], byteorder="big")
        rhs = s * self.G
        rx = int.from_bytes(sig[:32], byteorder="big")
        R = S256Point.make_from_x(x=rx)
        K = public_key

        lhs = R + self.H(msg)*K
        
        val = lhs == rhs
        return val
