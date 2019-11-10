from openvqe.simulator.simulatorbase import SimulatorBase, SimulatorReturnType
from openvqe.simulator.simulator_symbolic import SimulatorSymbolic

"""
Check which simulators are installed
"""
has_pyquil = True
from shutil import which
has_qvm = which("qvm") is not None
try:
    from openvqe.simulator.simulator_pyquil import SimulatorPyquil

    has_pyquil = True
except ImportError:
    has_pyquil = False

if not has_qvm:
    has_pyquil = False


has_qiskit = True
try:
    from openvqe.simulator.simulator_qiskit import SimulatorQiskit

    has_qiskit = True
except ImportError:
    has_qiskit = False

has_cirq = True
try:
    from openvqe.simulator.simulator_cirq import SimulatorCirq

    has_cirq = True
except ImportError:
    has_cirq = False

has_qulacs = True
try:
    from openvqe.simulator.simulator_qulacs import SimulatorQulacs

    has_qulacs = True
except ImportError:
    has_qulacs = False

from openvqe.simulator.simulator_symbolic import SimulatorSymbolic



def pick_simulator(samples=None):

    if samples is None:
        # need full wavefunction simulator
        if has_qulacs:
            return SimulatorQulacs
        elif has_cirq:
            return SimulatorCirq
        elif has_pyquil:
            return SimulatorPyquil
        else:
            return SimulatorSymbolic

    else:
        # Measurement based simulations
        if has_qiskit:
            return SimulatorQiskit
        elif has_cirq:
            return SimulatorCirq
        else:
            raise Exception("You have no simulator installed which can simulate finite measurements")