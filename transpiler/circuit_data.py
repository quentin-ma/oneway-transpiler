from typing import List

from qiskit.circuit import QuantumCircuit

from transpiler.data_dto import DataDto


class CircuitData:
    def __init__(self, circ: QuantumCircuit) -> None:
        self._circuit_data: List[DataDto] = list()
        self._num_qubits = circ.num_qubits

        for gate in circ.data:
            data_dto = DataDto(gate[0].name, gate[0].params, list(map(lambda x: x.index, gate[1][:])))
            self._circuit_data.append(data_dto)

    @property
    def data(self) -> List[DataDto]:
        return self._circuit_data

    @property
    def num_qubits(self) -> int:
        return self._num_qubits
