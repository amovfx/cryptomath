from sys import byteorder
from typing import Union, Type
from FieldElement.Constants import SECP256K1


class FieldElement:
    pass


FieldInt = Union[int, Type[FieldElement]]


def convertrhs(func):
    def _convert_rhs(obj, rhs: FieldInt) -> Type[FieldElement]:
        if isinstance(rhs, int):
            FE = FieldElement(rhs, obj._prime)
            return FE
        if isinstance(rhs, FieldElement):
            if obj._prime != rhs._prime:
                raise TypeError("Fields dont match.")
        return rhs

    def wrapper(self, rhs):
        rhs = _convert_rhs(self, rhs)
        return func(self, rhs)

    return wrapper


class FieldElement:
    def __init__(self, num, prime):
        self._num = num
        self._prime = prime

    @convertrhs
    def __pow__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = pow(self._num, rhs._num, self._prime)
        return self.__class__(result, self._prime)

    @convertrhs
    def __mul__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num * rhs._num) % self._prime
        return self.__class__(result, self._prime)

    @convertrhs
    def __rmul__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num * rhs._num) % self._prime
        return self.__class__(result, self._prime)

    @convertrhs
    def __truediv__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = self._num * pow(rhs._num, self._prime - 2, self._prime) % self._prime
        return self.__class__(result, self._prime)

    def __floordiv__(self, rhs: FieldInt) -> Type[FieldElement]:
        return self / rhs

    @convertrhs
    def __add__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num + rhs._num) % self._prime
        return self.__class__(result, self._prime)

    @convertrhs
    def __sub__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num - rhs._num) % self._prime
        return self.__class__(result, self._prime)

    def __neg__(self):
        return self.__class__(num=-self._num, prime=self._prime)

    @convertrhs
    def __eq__(self, rhs) -> bool:
        return self._num == rhs._num

    @convertrhs
    def __neq__(self, rhs: Union[int, Type[FieldElement]]) -> bool:
        return not self.__eq__(rhs)

    @convertrhs
    def __gt__(self, rhs) -> bool:
        return self._num > rhs._num

    @convertrhs
    def __ge__(self, rhs) -> bool:
        return self._num >= rhs._num

    @convertrhs
    def __lt__(self, rhs) -> bool:
        return self._num < rhs._num

    @convertrhs
    def __le__(self, rhs) -> bool:
        return self._num <= rhs._num

    def __and__(self, rhs:int) -> bool:
        return self._num & rhs

    def as_bytes(self, size=32, byteorder="big") -> bytes:
        self._num.to_bytes(size, byteorder=byteorder)

    def __repr__(self) -> str:
        return f"<FE[{self._num}|{self._prime}]>"


class S256Field:
    pass


class S256Field(FieldElement):
    def __init__(self, num, prime=SECP256K1.P):
        super().__init__(num=num, prime=prime)

    def sqrt(self) -> Type[S256Field]:
        return self ** ((self._prime + 1) // 4)

    def __neg__(self) -> Type[S256Field]:
        result = (self._prime - self._num) % self._prime
        return self.__class__(num=result, prime=self._prime)
