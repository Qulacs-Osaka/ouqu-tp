from qulacs import NoiseSimulator, Observable, QuantumCircuit, QuantumState


def get_measurement(circuit: QuantumCircuit, obs: Observable, shots: int) -> float:
    """
    Args:
        circuit (qulacs.Quantumcircuit):
        obs (qulacs.Observable)
        shots (int):  number of samples for each observable
    Return:
        :float: sampled expectation value of the observable
    """
    n_term = obs.get_term_count()
    n_qubit = obs.get_qubit_count()

    exp = 0 + 0.0j

    for i in range(n_term):
        pauli_term = obs.get_term(i)
        coef = pauli_term.get_coef()
        pauli_id = pauli_term.get_pauli_id_list()
        pauli_index = pauli_term.get_index_list()
        if len(pauli_id) == 0:  # means identity
            exp += coef
            continue
        buf_state = QuantumState(n_qubit)
        measurement_circuit = circuit.copy()

        for single_pauli, index in zip(pauli_id, pauli_index):
            if single_pauli == 1:
                measurement_circuit.add_H_gate(index)
            elif single_pauli == 2:
                measurement_circuit.add_Sdag_gate(index)
                measurement_circuit.add_H_gate(index)
        measurement_circuit.update_quantum_state(buf_state)
        samples = buf_state.sampling(shots)
        mask = "".join(
            ["1" if n_qubit - 1 - k in pauli_index else "0" for k in range(n_qubit)]
        )
        masked = int(mask, 2)
        exp += (
            coef
            * sum(
                list(map(lambda x: int((-1) ** (bin(x & masked).count("1"))), samples))
            )
            / shots
        )

    return exp.real


def get_noise_meseurment(circuit: QuantumCircuit, obs: Observable, shots: int) -> float:
    """
    Args:
        circuit (qulacs.Quantumcircuit) (have noise)
        obs (qulacs.Observable)
        shots (int):  number of samples for each observable
    Return:
        :float: sampled expectation value of the observable

    this func use noisesimulator
    """
    n_term = obs.get_term_count()
    n_qubit = circuit.get_qubit_count()

    exp = 0 + 0.0j

    for i in range(n_term):
        pauli_term = obs.get_term(i)
        coef = pauli_term.get_coef()
        pauli_id = pauli_term.get_pauli_id_list()
        pauli_index = pauli_term.get_index_list()
        if len(pauli_id) == 0:  # means identity
            exp += coef
            continue
        buf_state = QuantumState(n_qubit)
        measurement_circuit = circuit.copy()

        for single_pauli, index in zip(pauli_id, pauli_index):
            if single_pauli == 1:
                measurement_circuit.add_H_gate(index)
            elif single_pauli == 2:
                measurement_circuit.add_Sdag_gate(index)
                measurement_circuit.add_H_gate(index)

        nsim = NoiseSimulator(measurement_circuit, buf_state)
        samples = nsim.execute(shots)
        mask = "".join(
            ["1" if n_qubit - 1 - k in pauli_index else "0" for k in range(n_qubit)]
        )
        masked = int(mask, 2)
        exp += (
            coef
            * sum(
                list(map(lambda x: int((-1) ** (bin(x & masked).count("1"))), samples))
            )
            / shots
        )

    return exp.real


def get_noiseevo_meseurment(
    circuit: QuantumCircuit, obs: Observable, shots: int
) -> float:
    """
    Args:
        circuit (qulacs.Quantumcircuit) (have noise)
        obs (qulacs.Observable)
        shots (int):  number of samples for each observable
    Return:
        :float: sampled expectation value of the observable

    this func NOT use noisesimulator
    """
    n_term = obs.get_term_count()
    n_qubit = circuit.get_qubit_count()

    exp = 0 + 0.0j

    for i in range(n_term):
        pauli_term = obs.get_term(i)
        coef = pauli_term.get_coef()
        pauli_id = pauli_term.get_pauli_id_list()
        pauli_index = pauli_term.get_index_list()
        if len(pauli_id) == 0:  # means identity
            exp += coef
            continue

        buf_state = QuantumState(n_qubit)
        measurement_circuit = circuit.copy()

        for single_pauli, index in zip(pauli_id, pauli_index):
            if single_pauli == 1:
                measurement_circuit.add_H_gate(index)
            elif single_pauli == 2:
                measurement_circuit.add_Sdag_gate(index)
                measurement_circuit.add_H_gate(index)
        mask = "".join(
            ["1" if n_qubit - 1 - k in pauli_index else "0" for k in range(n_qubit)]
        )
        masked = int(mask, 2)
        for _ in range(shots):
            buf_state.set_zero_state()
            measurement_circuit.update_quantum_state(buf_state)
            sample = buf_state.sampling(1)[0]
            exp += coef * int((-1) ** (bin(sample & masked).count("1"))) / shots

    return exp.real
