from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit


class PatternExtension:
    def __init__(self):
        pass

    def h(self):
        qr = QuantumRegister(2)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr)

        qc.h(qr[1])
        qc.cz(qr[0], qr[1])

        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.x(qr[1]).c_if(cr[0], 1)

        return qc

    def rz(self, phi):
        qr = QuantumRegister(2)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr)

        qc.h(qr[1])
        qc.cz(qr[0], qr[1])

        qc.rz(phi, qr[0])
        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.x(qr[1]).c_if(cr[0], 1)

        qc.reset(qr[0])
        qc.h(qr[0])

        qc.cz(qr[1], qr[0])

        qc.h(qr[1])
        qc.measure(qr[1], cr[0])

        qc.x(qr[0]).c_if(cr[0], 1)

        return qc

    def cx(self):
        qr = QuantumRegister(3)
        cr = ClassicalRegister(2)
        qc = QuantumCircuit(qr, cr)

        qc.h(qr[1])
        qc.cz(qr[0], qr[1])
        qc.cz(qr[1], qr[2])

        qc.h(qr[2])
        qc.measure(qr[2], cr[0])

        qc.reset(qr[2])
        qc.h(qr[2])

        qc.cz(qr[1], qr[2])

        qc.h(qr[1])
        qc.measure(qr[1], cr[1])

        qc.x(qr[2]).c_if(cr[1], 1)
        qc.z(qr[2]).c_if(cr[0], 1)
        qc.z(qr[0]).c_if(cr[0], 1)
        return qc

