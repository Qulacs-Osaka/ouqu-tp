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

<<<<<<< HEAD
CNOTの制約のサンプルはdata/CNOT_net.txtにあります

入力QASMファイルのサンプルはdata/input.qasmにあります

出力QASMファイルのサンプルはdata/output.qasmにあります
=======
サンプルの入力 QASM ファイルは data/input.qasm にあります

サンプルの出力 QASM ファイルは data/output.qasm にあります

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
trance.sh data/input.qasm data/CNOT_net.txt data/output.qasm
```
>>>>>>> f2e15aa813d755580dfc5c8f44b13b332a91715c

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

<<<<<<< HEAD
simulate.sh 入力.qasm 出力.txt shot回数

QASMファイルを受け取り、量子状態を得た後、shotの回数だけ実行します。
=======
`simulate.sh 入力.qasm 出力.txt`

QASM ファイルを受け取り、量子状態を得た後、shot の回数だけ実行します。
>>>>>>> f2e15aa813d755580dfc5c8f44b13b332a91715c

shot回数は整数である必要があります。

kekkaの各行が量子状態に対応していて、　行の中で、一番「右」が0番のbitです。

<<<<<<< HEAD
入力QASMファイルのサンプルは、data/input.qasmにあります。

得られた結果のサンプルは、data/kekka.txtにあります。

=======
入力 QASM ファイルのサンプルは、data/input.qasm にあります。

得られた結果のサンプルは、data/kekka.txt にあります。

kekka の各行が量子状態に対応していて、　一番右が 0 番の bit です。
>>>>>>> f2e15aa813d755580dfc5c8f44b13b332a91715c

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
simulate.sh data/input.qasm data/kekka.txt shots
```
