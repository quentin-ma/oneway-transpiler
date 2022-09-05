from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from tools.find_pattern import find_pattern
from transpiler.circuit_data import CircuitData


class Scheduler:
    def __init__(self, circuit_data: CircuitData):
        self.qubits = circuit_data.num_qubits
        self.data = circuit_data.data

    def schedule(self) -> QuantumCircuit:

        qubits = QuantumRegister(self.qubits + 1)
        clbits = ClassicalRegister(self.qubits + 1)
        circ = QuantumCircuit(qubits, clbits, name='circ_ext')

        d = {x: [] for x in range(len(self.data))}

        if self.data[0].name == 'reset':
            self.data.pop(0)

        pattern = find_pattern(self.data[0], extension=True)
        slots = [x for x in range(0, pattern.num_qubits)]
        outputs = [None for _ in range(self.qubits + 1)]

        current = self.data[0]

        last = slots[-1]

        if pattern.name == 'cx_ext':
            d[0].append(0)
            d[0].append(last - 1)
            d[0].append(last)

            outputs[current.index[0]] = d[0][0]
            outputs[current.index[1]] = d[0][-1]
        else:
            d[0].append(0)
            d[0].append(last)

            outputs[current.index[0]] = d[0][-1]

        slots = d[0]

        filtered_outputs = list(filter(None.__ne__, outputs))
        vacant = list(set(slots).symmetric_difference(filtered_outputs))

        circ.compose(pattern, qubits=slots, inplace=True)

        self.data.pop(0)

        for i, gate in enumerate(self.data):
            current = self.data[i]
            pattern = find_pattern(current, extension=True)
            k = i + 1
            circ.barrier()
            if gate.name == 'cx':
                aux = vacant.pop()
                if outputs[current.index[0]] is None and outputs[current.index[1]] is None:
                    d[k].append(last + 1)
                    d[k].append(aux)
                    d[k].append(last + 2)
                    last += 2

                if outputs[current.index[0]] is None and outputs[current.index[1]] is not None:
                    d[k].append(last + 1)
                    d[k].append(aux)
                    d[k].append(outputs[current.index[1]])
                    last += 1

                if outputs[current.index[0]] is not None and outputs[current.index[1]] is None:
                    d[k].append(outputs[current.index[0]])
                    d[k].append(aux)
                    d[k].append(last + 1)
                    last += 1

                if outputs[current.index[0]] is not None and outputs[current.index[1]] is not None:
                    d[k].append(outputs[current.index[0]])
                    d[k].append(aux)
                    d[k].append(outputs[current.index[1]])

                outputs[current.index[0]] = d[k][0]
                outputs[current.index[1]] = d[k][-1]

            else:
                if outputs[current.index[0]] is None:
                    if len(vacant) > 1:
                        if pattern.num_qubits > len(vacant):
                            t = list(vacant)
                            for _ in t:
                                qubit = vacant.pop()
                                circ.reset(qubits[qubit])
                                d[k].append(qubit)
                        else:
                            for _ in range(pattern.num_qubits):
                                qubit = vacant.pop()
                                circ.reset(qubits[qubit])
                                d[k].append(qubit)

                    elif len(vacant) == 1:
                        qubit = vacant.pop()
                        circ.reset(qubits[qubit])
                        d[k].append(qubit)
                        d[k].append(last + 1)
                        last += 1
                    else:
                        d[k].append(last + 1)
                        d[k].append(last + 2)
                        last += 2

                if outputs[current.index[0]] is not None:

                    d[k].append(outputs[current.index[0]])
                    if len(vacant) > 0:
                        qubit = vacant.pop()
                        circ.reset(qubits[qubit])
                        d[k].append(qubit)
                    else:
                        d[k].append(last + 1)
                        last += 1
                outputs[current.index[0]] = d[k][-1]

            slots = list(set().union(slots, d[k]))
            filtered_outputs = list(filter(None.__ne__, outputs))
            vacant = list(set(slots).symmetric_difference(filtered_outputs))

            circ.compose(pattern, qubits=d[k], inplace=True)

            print("last measured qubit:", circ.get_instructions('measure')[-1].qubits[0].index)

            print("d:", d)
        print(outputs)
        return circ
