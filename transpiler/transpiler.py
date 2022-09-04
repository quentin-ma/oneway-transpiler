from typing import List

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister

from tools.find_pattern import find_pattern
from transpiler.circuit_data import CircuitData
from transpiler.pattern import Pattern


class Transpiler:
    def __init__(self, circuit_data: CircuitData, basis):
        self.circuit_data = circuit_data
        self.basis = basis
        self._outputs = []
        self.pattern = Pattern()

    def scan(self) -> int:
        auxiliaries = 0
        counts = [0] * self.circuit_data.num_qubits

        for i, gate in enumerate(self.circuit_data.data):
            num_qubits = find_pattern(self.circuit_data.data[i]).num_qubits
            if len(gate.index) > 1:
                if counts[gate.index[0]] > 0 and counts[gate.index[1]] > 0:
                    auxiliaries += 2

                if counts[gate.index[0]] == 0 and counts[gate.index[1]] > 0:
                    counts[gate.index[0]] += 1
                    auxiliaries += 2

                if counts[gate.index[0]] > 0 and counts[gate.index[1]] == 0:
                    counts[gate.index[1]] += 1
                    auxiliaries += 2

                if counts[gate.index[0]] == 0 and counts[gate.index[1]] == 0:
                    counts[gate.index[0]] += 1
                    counts[gate.index[1]] += 1
                    auxiliaries += 2
            else:
                if counts[gate.index[0]] > 0:
                    counts[gate.index[0]] += num_qubits - 1

                if counts[gate.index[0]] == 0:
                    counts[gate.index[0]] += num_qubits
        return sum(counts) + auxiliaries

    def transpile(self) -> QuantumCircuit:
        num_qubits = self.scan()
        num_gates = len(self.circuit_data.data)

        indexes = [gate.index for gate in self.circuit_data.data]
        outputs = [None for _ in range(self.circuit_data.num_qubits)]
        d = {x: (([], []), []) for x in range(num_gates)}

        qubits = QuantumRegister(num_qubits)
        cbits = ClassicalRegister(num_qubits)
        circ = QuantumCircuit(qubits, cbits, name='oway')

        pattern = find_pattern(self.circuit_data.data[0])
        slots = [x for x in range(pattern.num_qubits)]

        last = slots[-1]

        if pattern.name == "cx":
            if indexes[0][0] > indexes[0][1]:
                d[0][0][0].append(last)
                d[0][0][0].append(1)
                d[0][0][0].append(2)
                d[0][0][0].append(0)
            else:
                list(map(lambda x: d[0][0][0].append(x), slots))

            outputs[indexes[0][0]] = d[0][0][0][0]
            outputs[indexes[0][1]] = d[0][0][0][1]
            d[0][0][1].append(d[0][0][0][0])
            d[0][0][1].append(d[0][0][0][1])
        else:
            list(map(lambda x: d[0][0][0].append(x), slots))
            outputs[indexes[0][0]] = d[0][0][0][-1]
            d[0][0][1].append(last)
        d[0][1].append(last)

        circ.compose(pattern, qubits=slots, inplace=True)

        for i in range(1, num_gates):
            pattern = find_pattern(self.circuit_data.data[i])
            current = self.circuit_data.data[i]

            last = d[i - 1][1][0]

            if pattern.name == 'cx':
                if indexes[i][0] > indexes[i][1]:

                    if outputs[current.index[0]] is None and outputs[current.index[1]] is None:
                        begin = last + 1
                        end = begin + pattern.num_qubits - 1

                        d[i][0][0].append(end)
                        d[i][0][0].append(begin + 1)
                        d[i][0][0].append(begin + 2)
                        d[i][0][0].append(begin)

                        d[i][1].append(last + pattern.num_qubits)

                    if outputs[current.index[0]] is None and outputs[current.index[1]] is not None:
                        control = last + pattern.num_qubits - 1
                        target = outputs[current.index[1]]

                        d[i][0][0].append(control)
                        d[i][0][0].append(target + 1)
                        d[i][0][0].append(target + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + pattern.num_qubits - 1)

                    if outputs[current.index[0]] is not None and outputs[current.index[1]] is None:
                        control = outputs[current.index[0]]
                        target = last

                        d[i][0][0].append(control)
                        d[i][0][0].append(target + 1)
                        d[i][0][0].append(target + 2)
                        d[i][0][0].append(target + 3)

                        d[i][1].append(last + pattern.num_qubits - 1)

                    if outputs[current.index[0]] is not None and outputs[current.index[1]] is not None:
                        control = outputs[current.index[0]]
                        target = outputs[current.index[1]]

                        d[i][0][0].append(control)
                        d[i][0][0].append(last + 1)
                        d[i][0][0].append(last + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + 2)

                if indexes[i][0] < indexes[i][1]:
                    if outputs[current.index[0]] is None and outputs[current.index[1]] is None:
                        control = last + 1
                        target = control + pattern.num_qubits - 1

                        d[i][0][0].append(control)
                        d[i][0][0].append(control + 1)
                        d[i][0][0].append(control + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + pattern.num_qubits)

                    if outputs[current.index[0]] is None and outputs[current.index[1]] is not None:
                        control = last + 1
                        target = outputs[current.index[1]]

                        d[i][0][0].append(control)
                        d[i][0][0].append(control + 1)
                        d[i][0][0].append(control + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + pattern.num_qubits - 1)

                    if outputs[current.index[0]] is not None and outputs[current.index[1]] == None:
                        control = outputs[current.index[0]]
                        target = last + pattern.num_qubits - 1

                        d[i][0][0].append(control)
                        d[i][0][0].append(last + 1)
                        d[i][0][0].append(last + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + pattern.num_qubits - 1)

                    if outputs[current.index[0]] is not None and outputs[current.index[1]] is not None:
                        control = outputs[current.index[0]]
                        target = outputs[current.index[1]]

                        d[i][0][0].append(control)
                        d[i][0][0].append(last + 1)
                        d[i][0][0].append(last + 2)
                        d[i][0][0].append(target)

                        d[i][1].append(last + 2)

                d[i][0][1].append(d[i][0][0][0])
                d[i][0][1].append(d[i][0][0][1])

                outputs[current.index[0]] = d[i][0][1][0]
                outputs[current.index[1]] = d[i][0][1][1]

            if pattern.name != "cx":
                if outputs[current.index[0]] is None:
                    slots = [x for x in range(last + 1, last + pattern.num_qubits + 1)]
                    list(map(lambda x: d[i][0][0].append(x), slots))

                if outputs[current.index[0]] is not None:
                    d[i][0][0].append(outputs[current.index[0]])
                    slots = [x for x in range(last + 1, last + pattern.num_qubits)]
                    list(map(lambda x: d[i][0][0].append(x), slots))

                d[i][0][1].append(d[i][0][0][-1])
                d[i][1].append(d[i][0][1][0])

                outputs[current.index[0]] = d[i][0][1][0]

            circ.compose(pattern, qubits=d[i][0][0], inplace=True)

        print(d)
        print(outputs)

        self._outputs = outputs

        return circ

    def get_outputs(self, circ: QuantumCircuit) -> List[int]:
        indexes = [x for x in range(circ.num_qubits)]
        print(f"outputs: {self._outputs}")
        return list(set(indexes) - set(self._outputs))
