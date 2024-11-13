# Setup

## 必要な環境

### VSCode + devcontainer 環境を使う場合

VSCodeでdevcontainerを使って環境構築ができます。
詳しくは[ドキュメント](https://github.com/Qulacs-Osaka/qulacs-developer-docs/blob/main/doc/Learn-Usage/devcontainer-manual.md)を参照して下さい。ouqu-tpをcloneするには以下のコマンドを利用して下さい。(**scikit-qulacsではないことに注意！**)

```
git clone https://github.com/Qulacs-Osaka/ouqu-tp.git
```
### Docker 環境を使う場合

環境構築用のDockerfileが.devcontainerディレクトリ下に用意されています。
以下のコマンドを使うと必要なソフトウェアが導入された状態の作業用仮想環境に入ることができます。
Docker 内で行った/ouqu-tp ディレクトリ下への操作は Docker 外でも反映されるように設定しています。

```
docker build .devcontainer -t ouqu-tp-docker-image
docker run -it --mount type=bind,source=`pwd`,target=/ouqu-tp ouqu-tp-docker-image
```

### Docker 環境を使う場合

環境構築用のDockerfileが.devcontainerディレクトリ下に用意されています。
以下のコマンドを使うと必要なソフトウェアが導入された状態の作業用仮想環境に入ることができます。
Docker 内で行った/ouqu-tp ディレクトリ下への操作は Docker 外でも反映されるように設定しています。

```
docker build .devcontainer -t ouqu-tp-docker-image
docker run -it --mount type=bind,source=`pwd`,target=/ouqu-tp ouqu-tp-docker-image
```

### ローカルで動作させる場合

#### 必要なツール

- python
- Poetry(推奨) または pip
- staq

の3つが必要です。

他に必要なツールは poetry や pip が自動的にインストールします。

#### staq をインストールしようとして文字化けする場合

インストールする工程の一つに、コンパイル作業がありますが、そこで文字コードが原因でコンパイルエラーになることがあります。(定数が 2 行目まで続いていますなど)
このような場合は、ソースの文字コードを一括で BOM 付 UTF-8 にしたらコンパイルできる可能性があります。

## 動作前に

依存しているライブラリをインストールする必要があります。
poetry や pip を使ってインストールしてください。

```
# poetryの場合
poetry install

# pipの場合
pip install .
```
