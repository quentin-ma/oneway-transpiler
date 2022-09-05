from qiskit.circuit.random import random_circuit
from qiskit.compiler import transpile

from transpiler.circuit_data import CircuitData
from transpiler.scheduler import Scheduler

basis_gates = ['h', 'rz', 'cx', 'id']


def _main():
    circ = random_circuit(3, 3)
    print(circ)

    circ = transpile(circ, basis_gates=basis_gates, optimization_level=0)

    circuit_data = CircuitData(circ)
    scheduler = Scheduler(circuit_data)
    circ = scheduler.schedule()
    print(circ)


if __name__ == '__main__':
    _main()
