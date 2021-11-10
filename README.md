# ouqu-tp

英語対応してなくてごめん
いろいろ暫定です

# 使い方

input_test.qasm を入力する場合、

python main.py < input_test.qasm
すると、　結果が出力されます。

ただし、input_test.qasmは受け付ける関数の種類が非常に少ないです。
事前にstaqを用いて、コンパイル?しておく必要があります。
https://github.com/softwareQinc/staq

input_origin.qasmを本来のqasmファイルとしたとき、

staq -S -O2 -m -d ibm_tokyo.json --evaluate-all　input_origin.qasm

を用いて、　コンパイルされたqasmファイルをouqu-tpに入力します。


注意点:このトランスパイラは、グローバル位相を完全に無視します。
