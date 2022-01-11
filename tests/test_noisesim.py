from ouqu_tp.noisesim import noisesim_do


def test_noisesim_A() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    # 1qubitのゲートミス率は0.3
    # 正しくやれば、000=160 001=40 100=640 101=160
    input_strs = [
        "U(3.14159265358979,0,3.14159265358979) q[2];",
        "U(0,0,3.14159265358979) q[0];",
    ]
    # getvalのテストを書く
    correct_count = [1600, 400, 0, 0, 6400, 1600, 0, 0]
    (vals, _) = noisesim_do(input_strs, 10000, 0.3, 0, 0, 0)
    gate_count = [0, 0, 0, 0, 0, 0, 0, 0]

    for aaaa in vals:
        gate_count[aaaa] += 1
    print(gate_count)
    for i in range(8):
        assert abs(correct_count[i] - gate_count[i]) < 200


def test_noisesim_B() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    # 1qubitのゲートミス率は0.3
    # 正しくやれば、000=160 001=40 100=640 101=160
    input_strs = ["U(1.5707963267949,0,3.14159265358979) q[0];", "CX q[0],q[2];"]
    # getvalのテストを書く
    correct_count = [4200, 800, 0, 0, 800, 4200, 0, 0]
    (vals, _) = noisesim_do(input_strs, 10000, 0.3, 0.3, 0, 0)
    gate_count = [0, 0, 0, 0, 0, 0, 0, 0]

    for aaaa in vals:
        gate_count[aaaa] += 1
    print(gate_count)
    for i in range(8):
        assert abs(correct_count[i] - gate_count[i]) < 200


def test_noisesim_C() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    # 1qubitのゲートミス率は0.3
    # 正しくやれば、000=160 001=40 100=640 101=160
    input_strs = ["U(0,0,3.14159265358979) q[1];"]
    # getvalのテストを書く
    correct_count = [72220, 10320, 15300, 2160]
    (vals, _) = noisesim_do(input_strs, 100000, 0.1, 0, 0.1, 0.1)
    gate_count = [0, 0, 0, 0]

    for aaaa in vals:
        gate_count[aaaa] += 1
    print(gate_count)
    for i in range(4):
        assert abs(correct_count[i] - gate_count[i]) < 800


# 0.825:0.175
