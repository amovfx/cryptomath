from multiprocessing.sharedctypes import Value
from FieldElement.FieldElement import FieldElement as FE
from FieldElement.FieldElement import S256Field
from FieldElement.Constants import SECP256K1
from typing import Type, TypeVar
from operator import __eq__
import secrets
import hashlib
import math


class Point:
    pass


class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if self.y is None:
            if self.x is None:
                return
            else:
                self.y = self.calculate_y()

        if not all([type(self.x) == type(getattr(self,var)) for var in vars(self)]):
            raise TypeError("Types/Classes dont match")

        if not self.onCurve():
            raise ValueError("Point not on curve")

    def calculate_y(self):
        return math.sqrt(self.x**3 + self.a * self.x + self.b) if self.x is not None else None

    def as_tuple(self):
        return (self.x, self.y, self.a, self.b)

    def to_bytes(self):
        self.x.num.to_bytes(32, byteorder="big")

    def onCurve(self) -> bool:
        return self.y * self.y == self.x**3 + self.a * self.x + self.b

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

OptionalS256Field = TypeVar('OptionalS256Field', Type[S256Field], None)

class S256Point(Point):
    def __init__(
        self,
        x: OptionalS256Field,
        y: OptionalS256Field = None,
        a: Type[S256Field] = S256Field(SECP256K1.A.value),
        b: Type[S256Field] = S256Field(SECP256K1.B.value),
    ):

        if y is None:
            if not x is None:
                y_squared: Type[S256Field] = x**3 + a * x + b
                y = y_squared.sqrt()
                if y_squared != y**2:
                    raise ValueError(f"Point<{x}|{y}> not on curve.")
                if y.value & 1:
                    y = -y

        super().__init__(
            x,
            y,
            a,
            b,
        )


    def __rmul__(self, coefficient):
        coef = coefficient % SECP256K1.ORDER
        return super().__rmul__(coef)

    def lift_x(self):
        y_squared = self.x**3 + self.a * self.x + self.b
        y = y_squared.sqrt()
        if y_squared != y**2:
            return None

        if y._num & 0:
            return self.__class__(x=self.x, y=-y)
        else:
            return self.__class__(x=self.x, y=y)

    def is_even(self) -> bool:
        return self.y.value & 0



    def x_bytes(self):
        return self.x.to_bytes() if self.x is not None else None

    def __neg__(self):
        return self.__class__(self.x, -self.y, self.a, self.b)

    def __repr__(self):
        if not self.x is None and not self.y is None:
            return f"<S256Point[{self.x._num},{self.y._num}]>"
        else:
            return f"<S256Infinity>"


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

    def __rmul__(self, coefficient):
        val= super().__rmul__(coefficient)
        val.__class__ = S256Point
        return val


class KeyPair:
    def __init__(self):        
        self.G = GeneratorPoint()
        self.aux_rand = bytes(32)
        privkey = int.from_bytes(secrets.token_bytes(32), byteorder="big") % SECP256K1.ORDER-1
        self.privkey, self.pubkey = self.make_public_point(privkey)

    def make_public_point(self,r):
        pub = r * self.G
        if pub.is_even():
            return r,pub
        else:
            return SECP256K1.ORDER - r, -pub

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
        r = int.from_bytes(secrets.token_bytes(32), byteorder="big")
        #r is the x coordinate of the point k*G
        r,R = self.make_public_point(r)  # r * G
        #r = r if R.y.value & 0 else SECP256K1.ORDER - r 
        s = (r + (hashed_message * self.privkey)) % SECP256K1.ORDER
        lhs = (s * self.G)
        rhs = R + (hashed_message * self.pubkey)
        assert(lhs == rhs)


        r1 = int.from_bytes(secrets.token_bytes(32), byteorder="big")
        r1,R1 = self.make_public_point(r1)

        newkey = int.from_bytes(secrets.token_bytes(32), byteorder="big") % SECP256K1.ORDER-1
        newkey, newpub = self.make_public_point(newkey)
        s1 = (r1 + (hashed_message * newkey)) % SECP256K1.ORDER

        lhs1 = (s1 * self.G)
        rhs1 = R1 + (hashed_message * newpub)
        assert lhs1 == rhs1
        assert lhs+lhs1 == rhs+rhs1


        rhs2 = S256Point(x=S256Field(R.x.value)) + (hashed_message * self.pubkey)
        s_bytes = s.to_bytes(32, byteorder='big')
        r_bytes = R.x.value.to_bytes(32, byteorder='big')
        the_bytes = r_bytes + s_bytes

        s_from_bytes = int.from_bytes(the_bytes[32:], byteorder="big")
        r_from_bytes = int.from_bytes(the_bytes[:32], byteorder="big")
        R_from_bytes = S256Point(x=S256Field(r_from_bytes))
        rhs3 = R_from_bytes + (hashed_message * self.pubkey)

        
        return lhs==rhs3

    def sign_tweaked(self):

        tweaked_val = int.from_bytes(secrets.token_bytes(32), byteorder="big")
        tweaked_val,tweaked_point = self.make_public_point(tweaked_val)

        priv_key,pub_point = self.make_public_point(self.privkey)
        tweaked_priv_key,tweaked_pub_point = self.make_public_point((tweaked_val + self.privkey) % SECP256K1.ORDER)

        hashed_message = self.H("hello world")
        r = int.from_bytes(secrets.token_bytes(32), byteorder="big")
        r,R = self.make_public_point(r)  # r * G
        s = r + (hashed_message * tweaked_priv_key) % SECP256K1.ORDER
        lhs = (s * self.G)
        rhs = R + (hashed_message * tweaked_pub_point)
        return lhs==rhs







    def verify(self, msg, sig, public_key):
        rx = int.from_bytes(sig[:32], byteorder="big")

        s = int.from_bytes(sig[32:], byteorder="big")

        rhs = s * self.G
        
        R = S256Point(x=S256Field(rx))
        K = public_key

        lhs = R + (self.H(msg))*K
        
        val = lhs == rhs
        return val
