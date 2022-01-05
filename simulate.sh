staq -m --evaluate-all $1 > data/cpl.qasm

poetry run python ouqu_tp/simulate_call.py $3 < data/cpl.qasm > $2