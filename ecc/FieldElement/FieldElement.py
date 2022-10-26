from readline import read_history_file
from sys import byteorder
from typing import Union, Type
from FieldElement.Constants import SECP256K1


class FieldElement:
    pass


FieldInt = Union[int, Type[FieldElement]]


def convertrhs(func):
    def wrapper(self, rhs):
        if hasattr(rhs, '_num'):
            if hasattr(rhs,'_prime'):
                if rhs._prime != self._prime:
                    raise TypeError("Fields dont match.")
            return func(self, rhs._num)
        else:
            return func(self, rhs)

    return wrapper


class FieldElement:
    def __init__(self, num, prime):
        self._num = num
        self._prime = prime

    @property
    def value(self) -> int:
        return self._num

    def __repr__(self) -> str:
        return f"<FE[{self._num}|{self._prime}]>"

    def as_bytes(self, size=32, byteorder="big") -> bytes:
        self._num.to_bytes(size, byteorder=byteorder)

    @convertrhs
    def __pow__(self, rhs: int) -> Type[FieldElement]:
        result = pow(self._num, rhs, self._prime)
        return self.__class__(result, self._prime)
    @convertrhs
    def __mul__(self, rhs: int) -> Type[FieldElement]:
        result = (self._num * rhs) % self._prime
        return self.__class__(result, self._prime)
    @convertrhs
    def __rmul__(self, rhs: int) -> Type[FieldElement]:
        result = (self._num * rhs) % self._prime
        return self.__class__(result, self._prime)
    @convertrhs
    def __truediv__(self, rhs: int) -> Type[FieldElement]:
        result = self._num * pow(rhs, self._prime - 2, self._prime) % self._prime
        return self.__class__(result, self._prime)
    @convertrhs
    def __floordiv__(self, rhs: int) -> Type[FieldElement]:
        return self / rhs
    @convertrhs
    def __add__(self, rhs: int) -> Type[FieldElement]:
        result = (self._num + rhs) % self._prime
        return self.__class__(result, self._prime)
    @convertrhs
    def __sub__(self, rhs: int) -> Type[FieldElement]:
        result = (self._num - rhs) % self._prime
        return self.__class__(result, self._prime)

    def __neg__(self) -> Type[FieldElement]:
        return self.__class__(num=-self._num, prime=self._prime)

    def __eq__(self, rhs: Type[FieldElement]) -> bool:
        return self._num == rhs

    def __neq__(self, rhs: Type[FieldElement]) -> bool:
        return not self.__eq__(rhs)

    def __gt__(self, rhs: Type[FieldElement]) -> bool:
        return self._num > rhs

    def __ge__(self, rhs: Type[FieldElement]) -> bool:
        return self._num >= rhs

    def __lt__(self, rhs: Type[FieldElement]) -> bool:
        return self._num < rhs

    def __le__(self, rhs: Type[FieldElement]) -> bool:
        return self._num <= rhs

    @convertrhs
    def __and__(self, rhs: int) -> int:
        return self._num & rhs


class S256Field:
    pass


class S256Field(FieldElement):
    def __init__(self, num, prime=SECP256K1.P):
        super().__init__(num=num, prime=prime)

    def sqrt(self) -> Type[S256Field]:
        return self ** ((self._prime + 1) // 4)
    
    def to_bytes(self, size=32, byteorder="big") -> bytes:
        return self._num.to_bytes(size, byteorder=byteorder)

    def __neg__(self) -> Type[S256Field]:
        result = (self._prime - self._num) % self._prime
        return self.__class__(num=result, prime=self._prime)

    def __repr__(self) -> str:
        return f"<S256Field[{self._num}]>"
