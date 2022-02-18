from ouqu_tp.internal.getval import getval_do


def test_getval() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    input_strs = [
        "U(1.5707963267949,1.5707963267949,1.5707963267949) q[2];",
        "U(1.5707963267949,0,3.14159265358979) q[3];",
        "CX q[3],q[4];",
    ]
    # getvalのテストを書く

    val = getval_do(input_strs, "tests/fer_test.txt")
    print(val)
    assert abs(val - 0.95) < 0.00001
