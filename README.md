# ouqu-tp

英語対応してなくてごめんなさい

# 使い方

これは、QASM を qulacs で実行したり、実機で可能なようにうまく回路を変形するライブラリです。

- CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作る機能
- QASM ファイルを受け取り、量子状態を得た後、shot の回数だけ実行する機能
- QASM ファイルを受け取り、量子状態を得た後、オブザーバブルを openfermion の形式で受けとり、期待値を厳密に求める機能
- QASM ファイルを受け取り、量子状態を得た後、オブザーバブルを openfermion の形式で受けとり、shot の回数サンプリングしてオブザーバブルの値を求める機能

の四つの機能が実装されています。

入出力例として、サンプルの各ファイルが、すでに sample フォルダに入っています。参考にしてください。

注意点:このトランスパイラは、グローバル位相を完全に無視します。

## 必要な環境

### 手元で動作させる場合

- python

- Poetry(推奨) または pip

- staq

の 少なくとも 3 つが必要です。

残りは poetry や pip が自動的にインストールしてくれるはずです。

### staq をインストールしようとして文字化けする場合

インストールする工程の一つに、コンパイル作業がありますが、そこで文字コードが原因でコンパイルエラーになることがあります。(定数が 2 行目まで続いていますなど)

私の場合、ソースの文字コードを一括で BOM 付 UTF-8 にしたらコンパイルできました。

### Docker 環境を使う場合

Dockerfile が用意されています。
以下のコマンドを使うと必要なソフトウェアが導入された状態の作業用仮想環境に入ることができます。
Docker 内で行った/ouqu-tp ディレクトリ下への操作は Docker 外でも反映されるように設定しています。

```
docker build . -t ouqu-tp-docker-image
docker run -it --mount type=bind,source=`pwd`,target=/ouqu-tp ouqu-tp-docker-image
```

## 動かす前に

依存しているライブラリをインストールする必要があります。
poetry や pip を使ってインストールしてください。

```
# poetryの場合
poetry install

# pipの場合
pip install .
```

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

## その他

qulacs の仕様上、openfermion に虚数部分が含まれていても、それを無視して実数を返します。
