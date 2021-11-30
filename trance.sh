python ouqu_tp/make_Cnet.py < $2 > data/created_Cnet.json

staq -S -O2 -m -d data/created_Cnet.json --evaluate-all $1 > data/cpl.qasm

python ouqu_tp/trancepile.py < data/cpl.qasm > $3

