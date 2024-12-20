# How To Use

ouqu-tpには次の機能があります。

- CNOT の制約と OpenQASM ファイルから、実機で可能な OpenQASM ファイルを作る機能
- OpenQASM ファイルを受け取り、量子状態を得た後、shot の回数だけ実行する機能
- OpenQASM ファイルを受け取り、量子状態を得た後、オブザーバブルを openfermion の形式で受けとり、期待値を厳密に求める機能
- OpenQASM ファイルを受け取り、量子状態を得た後、オブザーバブルを openfermion の形式で受けとり、shot の回数サンプリングしてオブザーバブルの値を求める機能

将来的には次の機能が予定されています。

- CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作り、それをパルスシークエンスとして出力する機能
- QASMもどきとqulacsの相互変換

入出力例として、サンプルの各ファイルが、すでに sample フォルダに入っています。参考にしてください。

注意点:このトランスパイラは、グローバル位相を完全に無視します。

## 機能紹介

### trance

```
# poetryの場合
poetry run ouqu-tp trance trance --input-qasm-file=入力.qasm --input-cnot-json-file=CNOT制約.json

# pipの場合
ouqu-tp trance trance --input-qasm-file=入力.qasm --input-cnot-json-file=CNOT制約.json
```

CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作ります

サンプルの CNOT の制約は sample/CNOT_net.txt にあります

サンプルの入力 QASM ファイルは sample/input.qasm にあります

サンプルの出力 QASM ファイルは sample/output.qasm にあります

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
# poetryの場合
poetry run ouqu-tp trance trance --input-qasm-file=sample/input.qasm --input-cnot-json-file=sample/created_Cnet.json

# pipの場合
ouqu-tp trance trance --input-qasm-file=sample/input.qasm --input-cnot-json-file=sample/created_Cnet.json

```

### trance_res
上のやつで、　RZ,sqrtX,CNOT の代わりに、RZ,sqrtX,CRes を命令セットとしたものです。

ただし、CResは、[[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]] / √2 の量子ゲートです。

CResはOpenQASMにないことに注意してください

```
poetry run ouqu-tp trance trance_res --input-qasm-file=sample/input.qasm --input-cnot-json-file=sample/created_Cnet.json
```

### trance_pulse

```
poetry run ouqu-tp trance trance_pulse --input-qasm-file=入力.qasm --input-cnot-json-file=CNOT制約.json
--cnot-net-file=CNOT制約.txt --dt=1パルスの時間 --oz=RZゲートの1単位時間での回転量 --ox=RXゲートの1単位時間での回転量 --ores=CResゲートの1単位時間での回転量
```

numpy の　array を出力します。
出力形式はsavetxtを使っているので、　loadtxt関数を使うと読み込むことができます。

1行目は時間の配列です。
[0,dt,dt*2,dt*3 ...] が入ります。
2行目以降が、そのパルスでゲートを作用させるかさせないかです。

numpy arrayは[ゲート番号][時間]　で定義されます。
ゲート番号は、ZZZZZXXXXXRRRRR... のような定義をされるます。
ただし、Rは　CRes のことで、　CNOT_net.txt でのゲートの順番です。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

dt は 1パルスあたりの時間です。
ozはZゲートの、oxはXゲートの、oresはレゾナンスゲートの1単位時間(1パルスではない)あたりの回転角です

input json file と、それのもとになる cnot net file 両方を入力して下さい

出力は2次元の　numpy arrayで、[ゲート番号][時間]　で表されます。
値が0ではないとき、回転を行うということです

ゲート番号は、前から、 各qubitのZゲート、各qubitのXゲート、　各Resゲート(make_Cnetの順) の順で定義されます。ZZZXXXRRRR...

```
poetry run ouqu-tp trance trance_pulse --input-qasm-file=sample/input.qasm --input-cnot-json-file=sample/created_Cnet.json --cnot-net-file=sample/CNOT_net.txt --dt=0.005 --oz=10 --ox=10 --ores=1
```

パルスの入る数は、
RZゲートなら、 int(回転角 / (dt*oz * 2) + 0.5)
sqrtXゲートなら、int(pi / 2 / (dt*ox * 2) + 0.5)
CResゲートなら、int(pi / (dt * ores * 4) + 0.5)
です。
定義の違い? とかで半減されていた気がします


### make_Cnet
```
# poetryの場合
poetry run ouqu-tp trance makeCnet --cnot-net-file=CNOT制約.txt

# pipの場合
ouqu-tp trance makeCnet --cnot-net-file=CNOT制約.txt
```
上のtranceが利用するCnot制約はjsonで書かれています。

書きやすいように、以下の形式のtxtファイルからjsonに変換するプログラムです。

```
# poetryの場合
poetry run ouqu-tp trance makeCnet --cnot-net-file=sample/CNOT_net.txt

# pipの場合
ouqu-tp trance makeCnet --cnot-net-file=sample/CNOT_net.txt
```

####　サンプルにある sample/CNOT_net.txt を例にした,CNOT 制約ファイルの説明

```
1行目：名前 なんでもいい
2行目:qubit数
3行目:connected数
以降、connected数行:  control,tergetの順

例:

test
9
12
0,1
1,2
3,4
4,5
6,7
7,8
0,3
3,6
1,4
4,7
2,5
5,8


これは、
0-1-2
| | |
3-4-5
| | |
6-7-8
のグリッドでのCnotに対応します。
```

細かい仕様

3 行目:connected 数 は実は使っていなくて、 EOF まで読んでる
control,terget のところに END というアルファベット 3 文字の入力が来ると、終了になる

## ノイズがないバージョン

### simulate

```
# poetryの場合
poetry run ouqu-tp ideal simulate --input-qasm-file=入力.qasm --shots=shot回数

# pipの場合
ouqu-tp ideal simulate --input-qasm-file=入力.qasm --shots=shot回数
```

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、結果を受け取る

それを、shot の回数だけ実行します。

shot 回数は整数である必要があります。

出力の各行が量子状態に対応していて、行の中で、一番「右」が 0 番の bit です。

入力 QASM ファイルのサンプルは、sample/input.qasm にあります。

得られた結果のサンプルは、sample/kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
# poetryの場合
poetry run ouqu-tp ideal simulate --input-qasm-file=sample/input.qasm --shots=20

# pipの場合
ouqu-tp ideal simulate --input-qasm-file=sample/input.qasm --shots=20
```

### getval

```
# poetryの場合
poetry run ouqu-tp ideal getval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file

# pipの場合
ouqu-tp ideal getval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file
```

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、オブザーバブルで観測した値の期待値を求めます。

オブザーバブルは、openfermion 形式で保存しておく必要があります。

出力は観測した結果の厳密な期待値です。

入力 QASM ファイルのサンプルは、sample/input.qasm にあります。

openfermion_file のサンプルは、sample/fermion.txt にあります。

得られた結果のサンプルは、sample/gv_kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
# poetryの場合
poetry run ouqu-tp ideal getval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt

# pipの場合
ouqu-tp ideal getval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt
```

### sampleval

```
# poetryの場合
poetry run ouqu-tp ideal sampleval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --shots=shot回数

# pipの場合
ouqu-tp ideal sampleval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --shots=shot回数
```

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、オブザーバブルで shot 回観測します。

オブザーバブルは、openfermion 形式で保存しておく必要があります。

出力は shot 回観測した結果の実測平均値です。

ただし、オブザーバブルが複数の項の和として表される場合、それぞれ独立に shot 回づつ観測します。

入力 QASM ファイルのサンプルは、sample/input.qasm にあります。

openfermion_file のサンプルは、sample/fermion.txt にあります。

得られた結果のサンプルは、sample/sv_kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
# poetryの場合
poetry run ouqu-tp ideal sampleval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --shots=500

# pipの場合
ouqu-tp ideal sampleval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --shots=500
```

# ノイズがあるバージョン

ノイズがある場合を示します。

````
# poetryの場合
poetry run ouqu-tp noisy simulate --input-qasm-file=入力.qasm --shots=shot回数 --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率

poetry run ouqu-tp noisy getval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率

poetry run ouqu-tp noisy sampleval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --shots=shot回数 --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率


# pipの場合
ouqu-tp noisy simulate --input-qasm-file=入力.qasm--shots=shot回数 --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率

ouqu-tp noisy getval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率

ouqu-tp noisy sampleval --input-qasm-file=入力.qasm --input-openfermion-file=openfermion_file --shots=shot回数 --p1=p1の確率 --p2=p2の確率 --pm=pmの確率 --pp=ppの確率```
````

具体的には、p1,p2,pm,pp には 0 以上 1 以下の実数が入り、ノイズの確率を示します。

p1 は、1 ビットの量子ゲートのノイズの確率で、 コンパイルされた回路上で、1 ビットの量子ゲートがあるたびに、qulacs の DepolarizingNoise が入ります。

p2 は、2 ビットの量子ゲートのノイズの確率で、 コンパイルされた回路上で、2 ビットの量子ゲート(CX のみ)があるたびに、qulacs の TwoQubitDepolarizingNoise が入ります。

ノイズが入るのは、「コンパイルされた回路上」であることに注意してください。
例えば、手元で 2qubit gete 一つでも、コンパイルされたら 2qubit gate+1qubit gate2 つ みたいになることがあります。

それを防ぐためには、後述するオプション「--direct-qasm」を使うという方法があります。詳しくはそちらを見てく打差い

pm は、状態測定ノイズの確率で、 回路の終わりに、qulacs の DepolarizingNoise が入ります。

pp は、初期状態ノイズの確率で、 回路の始めに、qulacs の DepolarizingNoise が入ります。

全てのノイズについて、オプションとして確率を指定しなかった場合には初期値の 0 が入ります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
# poetryの場合
poetry run ouqu-tp noisy simulate --input-qasm-file=sample/input.qasm --shots=100 --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05

poetry run ouqu-tp noisy getval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05

poetry run ouqu-tp noisy sampleval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --shots=500 --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05


# pipの場合
ouqu-tp noisy simulate --input-qasm-file=sample/input.qasm --shots=100 --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05

ouqu-tp noisy getval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05

ouqu-tp noisy sampleval --input-qasm-file=sample/input.qasm --input-openfermion-file=sample/fermion.txt --shots=500 --p1=0.05 --p2=0.05 --pm=0.05 --pp=0.05
```

## オプション  --direct-qasm について
量子回路を入力するプログラム(つまり、make_Cnet以外のすべて)　に対して、オプション　 --direct-qasm が使用可能です。
--direct-qasmを使わない場合、一度QASMファイルをstaqに渡して、解釈しやすいようにしてからouqu-tpを実行しています。
--direct-qasmを使う場合、QASMを直接ouqu-tpに入れて回路を実行します。

ただし、読めるQASMは独自拡張を含んだり、　対応していない機能があったりします。詳しくは、QASMtoqulacsのドキュメントを呼んでください。
その場合の挙動は以下のようになります。


### trance 
本来はRZ,SqrtX,X,CNOT に分解するが、　渡されたQASMに2qubit以上のゲートがあった場合、そのゲートはそのまま出力される。
1qubitのゲートならそれはRZ,SqrtX,Xに分解する機構に渡せる。
### trance_res
tranceした後、CNOTをCResと1qubitゲートで表すので、　同様に、qubit以上のゲートがあった場合、そのゲートはそのまま出力される。
1qubitならRZ,SqrtX,Xになる。

### trance_pulse
1qubitでもCNOTでもCResでもないゲートが含まれている場合、エラーを出力する

### ideal系
特に問題なく渡せる。

### noisy系
2qubit以下のゲートであれば、問題なく渡せる。
3qubit 以上のゲートに対しては、ノイズのシミュレーションをどうすればいいのかわからないので、エラーになる。

また、staqを介さないことにより、ゲート表現が変わることがなくなり、渡されたQASM回路に忠実にノイズが入る。

## その他

qulacs の仕様上、openfermion に虚数部分が含まれていても、それを無視して実数を返します。

## 旧バージョンから変更点のまとめ
trance系の出力について変更がある
u1ゲートではなく、rzゲートになった(機能は変わらない)
空白が減って、staqのOPENQASM仕様になった
例:u1( 0.5000000000000001 ) q[ 0 ]; -> rz(0.5000000000000001) q[0];


## グローバーのアルゴリズムのサンプルについて
sample/grover_maker.pyは、 https://qiskit.org/textbook/ja/ch-algorithms/grover.html をもとに作られました。
実行すると、グローバーのアルゴリズムをqasm形式で表したものを返します。
この回路は、実行すると|110>と|101>が等確率で返ってきます。

下記は、それを様々なもので実行するためのコマンドです。
```
poetry run ouqu-tp ideal simulate --input-qasm-file=sample/grover_moto.qasm --shots=20
poetry run ouqu-tp noisy simulate --input-qasm-file=sample/grover_moto.qasm --shots=50 --p1=0.01 --p2=0.01 --pm=0.01 --pp=0.01
poetry run ouqu-tp ideal getval --input-qasm-file=sample/grover_moto.qasm --input-openfermion-file=sample/fer_sam.txt
poetry run ouqu-tp noisy getval --input-qasm-file=sample/grover_moto.qasm --input-openfermion-file=sample/fer_sam.txt --p1=0.01 --p2=0.01 --pm=0.01 --pp=0.01
poetry run ouqu-tp ideal sampleval --input-qasm-file=sample/grover_moto.qasm --input-openfermion-file=sample/fer_sam.txt --shots=900
poetry run ouqu-tp noisy sampleval --input-qasm-file=sample/grover_moto.qasm --input-openfermion-file=sample/fer_sam.txt --shots=900 --p1=0.01 --p2=0.01 --pm=0.01 --pp=0.01
```

なお、フェルミオンを実行した結果については、　ノイズなしなら-1が帰ってくるはずです。


#　エラー対応

QASMファイルをstaq経由で読む(--direct-qasm 無し)のとき、

```
Gate "sx" undeclared
```

のように、qelib1.incで定義されているはずのゲートが使えないことがあります。

これは、qiskitのqelib1.incに比べて、staqのqelibが古いのが原因です。

対処法として、読み込むファイルのinclude"qelib1.inc" の後に、(直下/)qelib_tuika.txt の内容をコピペすると動きます。
