from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister


class Pattern:
    def __init__(self):
        pass

    def reset(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.reset(0)
        return qc

    def id(self) -> QuantumCircuit:
        qr = QuantumRegister(3)
        cr = ClassicalRegister(2)
        qc = QuantumCircuit(qr, cr, name='id')

        qc.h(qr[1:])
        qc.cz(qr[:-1], qr[1:])

        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.h(qr[1])
        qc.measure(qr[1], cr[1])

        qc.x(qr[2]).c_if(cr[0], 1)
        qc.z(qr[2]).c_if(cr[1], 1)
        return qc

    def h(self) -> QuantumCircuit:
        qr = QuantumRegister(2)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr, name='h')

        qc.h(qr[1:])
        qc.cz(qr[:-1], qr[1:])

        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.x(qr[1]).c_if(cr[0], 1)
        return qc

    def s(self) -> QuantumCircuit:
        qr = QuantumRegister(5)
        cr = ClassicalRegister(4)
        qc = QuantumCircuit(qr, cr, name='s')

        qc.h(qr[1:])
        qc.cz(qr[:-1], qr[1:])

        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.h(qr[1])
        qc.measure(qr[1], cr[1])

        qc.h(qr[2])
        qc.sdg(qr[2])
        qc.measure(qr[2], cr[2])

        qc.h(qr[3])
        qc.measure(qr[3], cr[3])

        qc.x(qr[4]).c_if(cr[1], 1)
        qc.x(qr[4]).c_if(cr[3], 1)
        qc.z(qr[4]).c_if(cr[0], 1)
        qc.z(qr[4]).c_if(cr[1], 1)
        qc.z(qr[4]).c_if(cr[2], 1)
        qc.z(qr[4])
        return qc

    def rz(self, phi) -> QuantumCircuit:
        qr = QuantumRegister(3)
        cr = ClassicalRegister(2)
        qc = QuantumCircuit(qr, cr, name='rz')

        qc.h(qr[1:])
        qc.cz(qr[:-1], qr[1:])

        qc.rz(phi, qr[0])
        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.h(qr[1])
        qc.measure(qr[1], cr[1])

        qc.x(qr[2]).c_if(cr[1], 1)
        qc.z(qr[2]).c_if(cr[0], 1)
        return qc

    # u3(ϴ,φ,λ) = p(φ+π) sx p(ϴ+π) sx p(λ)
    def u3(self, alpha, beta, lam) -> QuantumCircuit:
        qr = QuantumRegister(5)
        cr = ClassicalRegister(4)
        qc = QuantumCircuit(qr, cr, name='u3')

        qc.h(qr[1:])
        qc.cz(qr[:-1], qr[1:])

        qc.h(qr[0])
        qc.measure(qr[0], cr[0])

        qc.rx(alpha, qr[1])
        qc.h(qr[1])
        qc.measure(qr[1], cr[1])

        qc.rz(beta, qr[2])
        qc.h(qr[2])
        qc.measure(qr[2], cr[2])

        qc.rx(lam, qr[3])
        qc.h(qr[3])
        qc.measure(qr[3], cr[3])

        qc.x(qr[4]).c_if(cr[1], 1)
        qc.x(qr[4]).c_if(cr[3], 1)
        qc.z(qr[4]).c_if(cr[0], 1)
        qc.z(qr[4]).c_if(cr[2], 1)
        return qc

    def cx(self) -> QuantumCircuit:
        qr = QuantumRegister(4)
        cr = ClassicalRegister(2)
        qc = QuantumCircuit(qr, cr, name='cx')

        qc.h(qr[1:-1])

        qc.cz(qr[3], qr[2])
        qc.cz(qr[2], qr[1])
        qc.cz(qr[2], qr[0])

        qc.h(qr[2])
        qc.measure(qr[2], cr[0])

        qc.h(qr[3])
        qc.measure(qr[3], cr[1])

        qc.x(qr[1]).c_if(cr[0], 1)
        qc.z(qr[1]).c_if(cr[0], 1)
        qc.z(qr[0]).c_if(cr[1], 1)
        return qc
