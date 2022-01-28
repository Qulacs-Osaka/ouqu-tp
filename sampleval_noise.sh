staq -m --evaluate-all $1 > data/cpl.qasm

poetry run python ouqu_tp/sampleval_noise_call.py $3 $4 $5 $6 $7 $8 < data/cpl.qasm > $2