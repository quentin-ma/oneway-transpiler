from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from tools.find_pattern import find_pattern
from transpiler.circuit_data import CircuitData


class Scheduler:
    def __init__(self, circuit_data: CircuitData):
        self.qubits = circuit_data.num_qubits
        self.data = circuit_data.data
        self.outputs = [None] * self.qubits

    def schedule(self) -> QuantumCircuit:
        qubits = QuantumRegister(self.qubits + 1)
        clbits = ClassicalRegister(self.qubits)
        circ = QuantumCircuit(qubits, clbits)

        last = 0
        slots = []

        vacant = set()

        for index, gate in enumerate(self.data):

            pattern = find_pattern(self.data[index], extension=True)
            print("current output: ", self.outputs[gate.index[0]])

            curr_outputs = self.outputs[gate.index[0]]

            if len(gate.index) > 1:
                pass

            if len(gate.index) == 1:
                slots[0] = curr_outputs
                left = pattern.num_qubits - 1

                if curr_outputs is None:

                    if len(vacant) > 0:
                        if left > len(vacant):
                            remains = left - len(vacant)
                            for x in range(len(vacant)):
                                slots.append(vacant.pop())

                            list(map(lambda x: slots.append(x), [k for k in range(last + 1, )]))

                    slots = [x for x in range(0, pattern.num_qubits)]
                    print("slots: ", slots)
                    last = slots[-1]

                if curr_outputs is not None:

                    if len(vacant) > 0:
                        if left > len(vacant):
                            remains = left - len(vacant)
                            for x in range(len(vacant)):
                                slots.append(vacant.pop())
                                left -= 1
                            list(map(lambda x: slots.append(x), [k for k in range(last, remains)]))

                        if len(vacant) >= left:
                            for x in range(left):
                                slots.append(vacant.pop())
                                left -= 1

            circ.compose(pattern, qubits=slots, inplace=True)

            print(circ.get_instructions('measure'))
            vacant_qubit = circ.get_instructions('measure')[-1][1][0].index
            circ.barrier()
            circ.reset(vacant_qubit)
            circ.barrier()

            vacant.add(vacant_qubit)

            self.outputs[gate.index[0]] = slots[-1]
            slots = [None]
            print("vacant: ", vacant)

        return circ
