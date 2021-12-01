staq -m --evaluate-all $1 > data/cpl.qasm

poetry run python ouqu_tp/simulate.py < data/cpl.qasm > $2
