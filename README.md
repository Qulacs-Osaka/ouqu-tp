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

実機制約について
CNOTゲートの制約は、staq側で処理します。
ibm_tokyo.json　というファイルに、　CNOTゲートの制約を書きます

√XとRZはouqu_tpで処理されます

注意点:このトランスパイラは、グローバル位相を完全に無視します。


ラッパーを書きました
trance.sh
CNOTの制約とQASMファイルから、実機で可能なQASMファイルを作ります

CNOTの制約はdata/CNOT_net.txtに書いてください
入力QASMファイルは、data/input.qasmに書いて下さい
出力QASMファイルは、data/output.qasmにあります
(data/cpl.qasm　は、中間表現です)
device mappingしてますが、どのようなマッピングかの情報が消えてます


simulate.sh
QASMファイルを受け取り、量子状態を得た後、shotの回数だけ実行します。
とりあえず回数=100
入力QASMファイルは、data/input.qasmに書いて下さい
得られた結果は、data/kekka.txtにあります。
kekkaの各行が量子状態に対応していて、　一番右が0番のbitです。


