from qiskit import QuantumCircuit

from transpiler.data_dto import DataDto
from transpiler.pattern import Pattern
from transpiler.pattern_extension import PatternExtension


def find_pattern(data_dto: DataDto, extension=False) -> QuantumCircuit:
    patterns = [pattern for pattern in dir(
        PatternExtension if extension else Pattern)
                if pattern.startswith('__') is False]
    find = lambda f, patterns: next((x for x in patterns if f(x)), None)
    pattern = find(lambda x: x == data_dto.name, patterns)

    #  only rz and u3 have parameters
    if pattern == 'rz' or pattern == 'u3':
        params = data_dto.params
        params = list(map(lambda x: float(x), params))
    else:
        params = ''

    target = PatternExtension() if extension else Pattern()

    return eval('target.' + str(pattern) + str(tuple(params)))
