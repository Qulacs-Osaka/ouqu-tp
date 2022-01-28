# ouqu-tp

英語対応してなくてごめんなさい

# 使い方

これは、QASM を qulacs で実行したり、実機で可能なようにうまく回路を変形するライブラリです。



CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作る trance.sh と、

QASM ファイルを受け取り、量子状態を得た後、shot の回数だけ実行する simulate.shと、

QASM ファイルを受け取り、量子状態を得た後、オブザーバブルをopenfermionの形式で受けとり、期待値を厳密に求めるgetval.shと、

QASM ファイルを受け取り、量子状態を得た後、オブザーバブルをopenfermionの形式で受けとり、shotの回数サンプリングしてオブザーバブルの値を求めるsampleval.sh

の四つの機能があります。

さらに、それらのノイズがある場合のバージョンの、simulate_noise.sh,getval_noise.sh,sampleval_noise.sh

が存在します。

re_系のやつは一度止まりました。後で復活する可能性があります。

入出力例として、サンプルの各ファイルが、すでに data フォルダに入っています。参考にしてください。

注意点:このトランスパイラは、グローバル位相を完全に無視します。

## 必要な環境

### 手元で動作させる場合

- python

- Poetry

- staq

の 少なくとも 3 つが必要です。

残りは poetry が自動的にインストールしてくれるはずです。

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
poetry を使ってインストールしてください。

```
poetry install
```

## trance.sh

`trance.sh 入力.qasm CNOT制約.txt 出力.qasm`

CNOT の制約と QASM ファイルから、実機で可能な QASM ファイルを作ります

サンプルの CNOT の制約は data/CNOT_net.txt にあります

サンプルの入力 QASM ファイルは data/input.qasm にあります

サンプルの出力 QASM ファイルは data/output.qasm にあります

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
trance.sh data/input.qasm data/CNOT_net.txt data/output.qasm
```

(data/cpl.qasm は、中間表現です。QASM 形式で、 U ゲートと CNOT だけで構成されます)

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

3 行目:connected 数 は実は使っていなくて、 EOF まで読んでる
control,terget のところに END というアルファベット 3 文字の入力が来ると、終了になる


# ノイズがないバージョン

## simulate.sh

`simulate.sh 入力.qasm 出力.txt shot回数`

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、結果を受け取る

それを、shot の回数だけ実行します。

shot 回数は整数である必要があります。

出力の各行が量子状態に対応していて、行の中で、一番「右」が 0 番の bit です。

入力 QASM ファイルのサンプルは、data/input.qasm にあります。

得られた結果のサンプルは、data/kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
simulate.sh data/input.qasm data/sim_kekka.txt 20
```

## getval.sh

`getval.sh 入力.qasm 出力.txt openfermion_file `

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、オブザーバブルで観測した値の期待値を求めます。

オブザーバブルは、openfermion 形式で保存しておく必要があります。

出力は観測した結果の厳密な期待値です。

入力 QASM ファイルのサンプルは、data/input.qasm にあります。

openfermion_file のサンプルは、data/fermion.txt にあります。

得られた結果のサンプルは、data/gv_kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
getval.sh data/input.qasm data/gv_kekka.txt data/fermion.txt
```

[添え字とqubitに関しての問題はこちらを参照してください] (# 添え字ビット数一致問題)

## sampleval.sh

`sampleval.sh 入力.qasm 出力.txt openfermion_file shot回数`

QASM ファイル形式で量子回路を入力して、その回路に(000..0)を入力して、オブザーバブルでshot回観測します。

オブザーバブルは、openfermion 形式で保存しておく必要があります。

出力はshot回観測した結果の実測平均値です。

ただし、オブザーバブルが複数の項の和として表される場合、それぞれ独立にshot回づつ観測します。

入力 QASM ファイルのサンプルは、data/input.qasm にあります。

openfermion_file のサンプルは、data/fermion.txt にあります。

得られた結果のサンプルは、data/sv_kekka.txt にあります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
sampleval.sh data/input.qasm data/sv_kekka.txt data/fermion.txt 500
```

[添え字とqubitに関しての問題はこちらを参照してください] (#添え字ビット数一致問題)

# ノイズがあるバージョン

ノイズがある場合を示します。

`simulate_noise.sh 入力.qasm 出力.txt shot回数 p1 p2 pm pp`
`getval_noise.sh 入力.qasm 出力.txt openfermion_file p1 p2 pm pp`
`sampleval_noise.sh 入力.qasm 出力.txt openfermion_file shot回数 p1 p2 pm pp`

具体的には、p1,p2,pm,ppには0以上1以下の実数が入り、ノイズの確率を示します。

p1は、1ビットの量子ゲートのノイズの確率で、 コンパイルされた回路上で、1ビットの量子ゲートがあるたびに、qulacsのDepolarizingNoiseが入ります。

p2は、2ビットの量子ゲートのノイズの確率で、 コンパイルされた回路上で、2ビットの量子ゲート(CXのみ)があるたびに、qulacsのTwoQubitDepolarizingNoiseが入ります。

ノイズが入るのは、「コンパイルされた回路上」であることに注意してください。
例えば、手元で2qubit gete一つでも、コンパイルされたら2qubit gate+1qubit gate2つ みたいになることがあります。

pmは、状態測定ノイズの確率で、 回路の終わりに、qulacsのDepolarizingNoiseが入ります。

ppは、初期状態ノイズの確率で、 回路の始めに、qulacsのDepolarizingNoiseが入ります。

例えば、サンプルを実行する場合は以下のコマンドを実行してください。

```
simulate_noise.sh data/input.qasm data/sim_noise_kekka_noise.txt 100 0.05 0.05 0.05 0.05
getval_noise.sh data/input.qasm data/gv_noise_kekka.txt data/fermion.txt 0.05 0.05 0.05 0.05
sampleval_noise.sh data/input.qasm data/sv_noise_kekka.txt data/fermion.txt 500 0.05 0.05 0.05 0.05
```


# 添え字ビット数一致問題
現状、入力 QASM ファイルの bit 数と、fermion のビット数(添え字の最大値+1)が、 ピッタリ一致しないと動きません。

これは、内部的な話をすると、qulacs では fermion をファイルから読み込むときにビット数が自動で付与されてしまうのが原因です。

qulacs と、qulacs-osaka にプルリクを投げました。

通れば、入力 QASM ファイルの bit 数が、fermion のビット数以上なら動くようになります。