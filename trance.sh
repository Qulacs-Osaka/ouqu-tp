#!/bin/bash

workdir=$(mktemp -d)

poetry run python ouqu_tp/make_Cnet.py < $2 > $workdir/created_Cnet.json

staq -S -O2 -m -d $workdir/created_Cnet.json --evaluate-all $1 > $workdir/cpl.qasm

poetry run python ouqu_tp/trancepile.py < $workdir/cpl.qasm > $3
