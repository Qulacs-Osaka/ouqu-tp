# ouqu-tp

英語対応してなくてごめんなさい

# 使い方

これは、QASM を qulacs で実行したり、実機で可能なようにうまく回路を変形するライブラリです。

CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作る trance.sh と、

QASM ファイルを受け取り、量子状態を得た後、shot の回数だけ実行する simulate.sh

の二つの機能があります。

入出力例として、サンプルの各ファイルが、すでに data フォルダに入っています。参考にしてください。

注意点:このトランスパイラは、グローバル位相を完全に無視します。

## 必要な環境

### 手元で動作させる場合

- python

- Poetry

- staq

の 少なくとも3 つが必要です。

残りはpoetryが自動的にインストールしてくれるはずです。

### staq をインストールしようとして文字化けする場合

インストールする工程の一つに、コンパイル作業がありますが、そこで文字コードが原因でコンパイルエラーになることがあります。(定数が2行目まで続いています　など)

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
poetry を使ってインストールしてください。

```
poetry install
```

## trance.sh

`trance.sh 入力.qasm CNOT 制約.txt 出力.qasm`

CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作ります

サンプルの CNOT の制約は data/CNOT_net.txt にあります

サンプルの入力 QASM ファイルは data/input.qasm にあります

サンプルの出力 QASM ファイルは data/output.qasm にあります

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
trance.sh data/input.qasm data/CNOT_net.txt data/output.qasm
```

(data/cpl.qasm 　は、中間表現です。QASM 形式で、　 U ゲートと CNOT だけで構成されます)

### 初期状態にある data/CNOT_net.txt を例にした,CNOT 制約ファイルの説明

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
```

細かい仕様

3 行目:connected 数 は実は使っていなくて、　 EOF まで読んでる
control,terget のところに END というアルファベット 3 文字の入力が来ると、終了になる

## simulate.sh

`simulate.sh 入力.qasm 出力.txt shot回数`

QASMファイル形式で量子回路を入力して、その回路に(000..0)を入力して、結果を受け取る

それを、shotの回数だけ実行します。

shot回数は整数である必要があります。

出力の各行が量子状態に対応していて、　行の中で、一番「右」が0番のbitです。

入力 QASM ファイルのサンプルは、data/input.qasm にあります。

得られた結果のサンプルは、data/kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
simulate.sh data/input.qasm data/kekka.txt
```

## getval.sh

`getval.sh 入力.qasm 出力.txt openfermion_file `

QQASMファイル形式で量子回路を入力して、その回路に(000..0)を入力して、オブザーバブルで観測します。

オブザーバブルは、openfermion形式で保存しておく必要があります。

出力は観測した結果の数値一つです。

入力 QASM ファイルのサンプルは、data/input.qasm にあります。

openfermion_file のサンプルは、data/fermion.txtにあります。

得られた結果のサンプルは、data/gv_kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
getval.sh data/input.qasm data/gv_kekka.txt data/fermion.txt
```

現状、入力QASMファイルのbit数と、fermionのビット数(添え字の最大値+1)が、 ピッタリ一致しないと動きません。

これは、内部的な話をすると、qulacsではfermionをファイルから読み込むときにビット数が自動で付与されてしまうのが原因です。

qulacsと、qulacs-osakaにプルリクを投げました。

通れば、入力QASMファイルのbit数が、fermionのビット数以上なら動くようになります。

## re_simulate.sh

`simulate.sh 出力.txt shot回数`

## re_getval.sh

`getval.sh 出力.txt openfermion_file`



この2つは、QASMファイルは前回入力したものを使う場合のコマンドです。

具体的にいうと、re_ が付かないシェルでは、staqを用いて入力したファイルをqulacsが処理しやすい形式にした後、data/cpl.qasmに保存されています。
そのdata/cpl.qasmを、再び使います。

trance.shでもcpl.qasmは更新されます。