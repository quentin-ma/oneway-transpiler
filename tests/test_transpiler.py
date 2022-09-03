from qiskit import transpile
from qiskit.circuit.random import random_circuit

from transpiler.circuit_data import CircuitData
from transpiler.transpiler import Transpiler

basis_gates = ['h', 's', 'rz', 'u3', 'cx', 'id']


def _main():
    circ = random_circuit(2, 2)

    circ = transpile(circ, basis_gates=basis_gates, optimization_level=0)

    circuit_data = CircuitData(circ)
    circ = Transpiler(circuit_data, basis_gates)
    circ = circ.transpile()
    print(circ)


if __name__ == '__main__':
    _main()
