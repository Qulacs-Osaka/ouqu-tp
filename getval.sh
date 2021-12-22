#!/bin/bash

workdir=$(mktemp -d)

staq -m --evaluate-all $1 > $workdir/cpl.qasm

poetry run python ouqu_tp/getval.py $3 < $workdir/cpl.qasm > $2
