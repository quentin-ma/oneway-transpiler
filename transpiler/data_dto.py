from typing import List

from qiskit.circuit import ParameterExpression


class DataDto:
    def __init__(self, name: str, params: List[ParameterExpression], index: List[int]):
        self._name = name
        self._index = index
        self._params = params

    @property
    def name(self) -> str:
        return self._name

    @property
    def index(self) -> List[int]:
        return self._index

    @property
    def params(self) -> List[ParameterExpression]:
        return self._params
