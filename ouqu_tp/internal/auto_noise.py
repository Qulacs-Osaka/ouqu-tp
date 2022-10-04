from typing import List, Tuple

from qulacs import GeneralQuantumOperator, Observable, QuantumCircuit
from qulacs.gate import (
    DepolarizingNoise,
    NoisyEvolution_fast,
    TwoQubitDepolarizingNoise,
)

from ouqu_tp.internal.tran import tran_to_pulse_tyukan


def auto_noise(
    inputcircuit_in: QuantumCircuit,
    p1: float,
    p2: float,
    pm: float,
    pp: float,
) -> QuantumCircuit:
    inputcircuit = inputcircuit_in.copy()
    n_qubit = inputcircuit.get_qubit_count()
    testcircuit = QuantumCircuit(n_qubit)
    for i in range(n_qubit):
        testcircuit.add_gate(DepolarizingNoise(i, pp))
    gate_num = inputcircuit.get_gate_count()
    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)
        testcircuit.add_gate(ingate)

        gate_index_list = (
            ingate.get_control_index_list() + ingate.get_target_index_list()
        )

        if len(gate_index_list) == 1:
            testcircuit.add_gate(DepolarizingNoise(gate_index_list[0], p1))
        if len(gate_index_list) == 2:
            testcircuit.add_gate(
                TwoQubitDepolarizingNoise(gate_index_list[0], gate_index_list[1], p2)
            )

        if len(gate_index_list) > 2:
            # 本来ありえません　3ビット以上のやつは
            raise RuntimeError("3ビット以上のやつを与えないでください もしくは何かバグがあるので、連絡して下さい")

    for i in range(n_qubit):
        testcircuit.add_gate(DepolarizingNoise(i, pm))
    return testcircuit


def auto_Res_list(inputcircuit: QuantumCircuit) -> List[Tuple[int, int]]:
    Res_list: List[Tuple[int, int]] = []

    gate_num = inputcircuit.get_gate_count()
    Res_set = set(Res_list)
    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)

        gate_index_list = (
            ingate.get_control_index_list() + ingate.get_target_index_list()
        )
        if len(gate_index_list) == 2:
            gen_Res_pair = (gate_index_list[0], gate_index_list[1])
            if gen_Res_pair not in Res_set:
                Res_set.add(gen_Res_pair)
                Res_list.append(gen_Res_pair)

    return Res_list


def auto_evo_noise(
    inputcircuit_in: QuantumCircuit,
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    decay_rate_ph: float,
    decay_rate_amp: float,
    evodt: float,
) -> QuantumCircuit:
    """
    :param pulce_comp:  各パルスは、(ゲート番号、スタート時刻、ゲート長さ)で、　tran_to_pulse_tyukanの帰り値を渡すことが多い
    :param dt: 1パルスの時間
    :param OZ: 1時間あたりの回転量(not 1パルス)
    :param OX: 1時間あたりの回転量
    :param ORes: 1時間あたりの回転量
    :param decay_rate_ph:1時間あたりの位相のデコヒーレンス量?
    :param decay_rate_amp:1時間あたりのampのデコヒーレンス量?
    :param n_qubit: キュービット数
    :param evodt: NoisyEvolutionでの1ステップの時間 これが小さいほど正確だけど計算負荷かかる
    """
    inputcircuit = inputcircuit_in.copy()
    Res_list = auto_Res_list(inputcircuit)
    (pulse_comp, unuse) = tran_to_pulse_tyukan(inputcircuit, Res_list, dt, OZ, OX, ORes)
    n_qubit = inputcircuit.get_qubit_count()
    anscircuit = QuantumCircuit(n_qubit)
    for ple in pulse_comp:
        (gate_ban, start, time) = ple
        # print(gate_ban, start, time)
        if gate_ban < n_qubit * 2 or n_qubit * 2 + len(Res_list) <= gate_ban:
            if gate_ban < n_qubit:  # Z gate
                target = gate_ban
                hamiltonian = Observable(n_qubit)
                hamiltonian.add_operator(OZ, "Z {0}".format(target))
            elif gate_ban < n_qubit * 2:  # X gate
                target = gate_ban - n_qubit
                hamiltonian = Observable(n_qubit)
                hamiltonian.add_operator(OX, "X {0}".format(target))
            elif gate_ban >= n_qubit * 2 + len(Res_list):  # I gate
                target = gate_ban - (n_qubit * 2 + len(Res_list))
                hamiltonian = Observable(n_qubit)
            jump_op_list = [GeneralQuantumOperator(n_qubit) for i in range(2)]
            jump_op_list[0].add_operator(decay_rate_ph, "Z {0}".format(target))
            jump_op_list[1].add_operator(
                decay_rate_amp / 2 * 1j, "Y {0}".format(target)
            )
            jump_op_list[1].add_operator(decay_rate_amp / 2, "X {0}".format(target))

        else:
            (control, target) = Res_list[gate_ban - n_qubit * 2]
            hamiltonian = Observable(n_qubit)
            hamiltonian.add_operator(ORes, "X {0} Z {1}".format(target, control))
            jump_op_list = [GeneralQuantumOperator(n_qubit) for i in range(4)]
            jump_op_list[0].add_operator(decay_rate_ph, "Z {0}".format(target))
            jump_op_list[1].add_operator(
                decay_rate_amp / 2 * 1j, "Y {0}".format(target)
            )
            jump_op_list[1].add_operator(decay_rate_amp / 2, "X {0}".format(target))
            jump_op_list[2].add_operator(decay_rate_ph, "Z {0}".format(control))
            jump_op_list[3].add_operator(
                decay_rate_amp / 2 * 1j, "Y {0}".format(control)
            )
            jump_op_list[3].add_operator(decay_rate_amp / 2, "X {0}".format(control))

        # print(gate_ban,n_qubit,len(Res_list))
        # print(hamiltonian, start, time, evodt)
        opr = NoisyEvolution_fast(hamiltonian, jump_op_list, time * dt)
        anscircuit.add_gate(opr)

    return anscircuit
