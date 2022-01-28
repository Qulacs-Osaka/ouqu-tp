staq -m --evaluate-all $1 > data/cpl.qasm

poetry run python ouqu_tp/noisesim_call.py $3 $4 $5 $6 $7 < data/cpl.qasm > $2