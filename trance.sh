python ouqu_tp/make_Cnet.py < data/CNOT_net.txt > data/created_Cnet.json

staq -S -O2 -m -d data/created_Cnet.json --evaluate-all data/input.qasm > data/cpl.qasm

python ouqu_tp/trancepile.py < data/cpl.qasm > data/output.txt

