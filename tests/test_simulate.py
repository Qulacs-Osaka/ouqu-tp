from ouqu_tp.internal.simulate import simulate_do


def test_simulate() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    input_strs = ["U(3.14159265358979,0,0) q[2];", "CX q[2],q[0];"]
    # getvalのテストを書く

    (vals, _) = simulate_do(input_strs, 25)
    print(vals)
    for aaaa in vals:
        assert aaaa == 5
