import typing


def input_strings() -> typing.List[str]:
    input_strs = []
    while True:
        try:
            line = input()
            if line == "END":  # END という3文字を受け取る
                break
            input_strs.append(line)
        except EOFError:
            break
    return input_strs
