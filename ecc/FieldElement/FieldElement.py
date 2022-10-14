from typing import Union, Type


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
        return FieldElement(result, self._prime)

    @convertrhs
    def __mul__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num * rhs._num) % self._prime
        return FieldElement(result, self._prime)

    @convertrhs
    def __truediv__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = self._num * pow(rhs._num, self._prime - 2, self._prime) % self._prime
        return FieldElement(result, self._prime)

    def __floordiv__(self, rhs: FieldInt) -> Type[FieldElement]:
        return self / rhs

    @convertrhs
    def __add__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num + rhs._num) % self._prime
        return FieldElement(result, self._prime)

    @convertrhs
    def __sub__(self, rhs: FieldInt) -> Type[FieldElement]:
        result = (self._num - rhs._num) % self._prime
        return FieldElement(result, self._prime)

    @convertrhs
    def __ge__(self, rhs) -> bool:
        return self._num >= rhs._num

    @convertrhs
    def __le__(self, rhs) -> bool:
        return self._num <= rhs._num

    @convertrhs
    def __eq__(self, rhs) -> bool:
        return self._num == rhs._num

    @convertrhs
    def __neq__(self, rhs: Union[int, Type[FieldElement]]) -> bool:
        return not self.__eq__(rhs)

    def __repr__(self) -> str:
        return f"<FieldElement<{self._prime}>({self._num})>"
