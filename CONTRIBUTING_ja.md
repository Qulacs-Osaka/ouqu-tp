# How to contribute
## Prerequisite
poetry をインストールしてください．
poetry は依存解決，パッケージのビルドと公開のためのツールです．

Linux と macOS におけるインストール方法は
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

Windows では
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

詳細な解説: [poetry documentation](https://python-poetry.org/docs/#installation)

## Using poetry
poetry の基本的な使用方法を紹介します．
詳しくは [Basic usage](https://python-poetry.org/docs/basic-usage) と [Commands](https://python-poetry.org/docs/cli/) を参照してください．

### Virtual environment
poetry は依存パッケージを管理するために仮想環境を作成します．
VSCode を使う場合はプロジェクトのルートに作成すると便利です．
まず設定を変更します．
```bash
poetry config virtualenvs.in-project true
```
そして VSCode の設定で `./.venv/bin/python`(Windows では `./.venv/Scripts/python.exe`) をプロジェクトの Python インタプリタとして指定します．

### Dependency management
poetry は依存パッケージのリストを `pyproject.toml` で管理します．
このファイルに新しい依存パッケージを追加するには
```bash
poetry add numpy
```
を実行します．
開発のためだけに使うパッケージをインストールするときは `-D` フラグをつけます．
```bash
poetry add -D black
```

そして依存パッケージをインストールします．
```bash
poetry install
```
このコマンドは `poetry.lock` を更新します．
このファイルによってどの開発者もまったく同じバージョンの依存パッケージをインストールできるため，このファイルをコミットするようにしてください．

以下のコマンドで依存パッケージを最新のバージョンに更新できます．
```bash
poetry update
```

### Run scripts and commands
仮想環境内でスクリプトやコマンドを実行できます．
```bash
poetry run python main.py
poetry run python
```

言い換えると，`python main.py` と実行しただけでは仮想環境にインストールしたパッケージを利用することはできません．

### Build and publish
wheel アーカイブをビルドするには以下を実行します．
```bash
poetry build
```

パッケージを公開するには [How to Publish a Python Package to PyPI using Poetry](https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-using-poetry-aa804533fc6f) を参照してください．

## Start coding
1. このリポジトリをクローンします．
2. `main` ブランチと同期します．
```bash
git switch main
git pull
```

3. 開発しようとしている機能を説明する名前をつけたブランチを作成します．ブランチの名前のフォーマットは `${ISSUE_NUMBER}-${FEATURE}` です．
```bash
git switch -c 99-wonderful-model
```

4. 依存パッケージをインストールします．直近にインストールした依存パッケージがなければこれは必要ありません．
```bash
poetry install
```

5. コードを書きます．新しいファイルを作った際は，後の手順のためにそのファイルを git のインデックスに追加してください．
```bash
git add NEW_FILE
```

6. コードをフォーマットし，リンタを実行し，テストをします．
```
make check
make test
```

フォーマットあるいはリンタのエラーがあった場合はこのコマンドで自動修正を試みることができます．
```
make format
```

まだエラーが残っているかもしれません．それらのエラーは自動的に修正できないため，手で修正します．

7. コーディングが終わったら，変更をコミットしてプッシュします．
```bash
git add -p
git commit
# For the first push in the branch
git push -u origin 99-wonderful-model
# After first push
git push
```

8. そのブランチで開発すべき機能ができたらプルリクエスト(PR)を出します． 基本的に他の人にレビューを受けるようにします．レビュアーが承認してすべての CI がパスしたら `main` にマージします．

## Testing
新しい機能を開発したときにはテストを書くようにします． このテストは基本的に自動で実行されるものです．

1. `tests` ディレクトリに `test_*.py` というファイルを作ります． テストの内容を大まかに表すファイル名をつけます．
2. そのファイルの中に `test_` で始まる関数を作ります． そこに実装した機能が満たすべき条件を書きます． たとえば和を計算する関数のテストは以下のようになります．
```python
from skqulacs import add # This function does not exist in the module.
def test_add():
    assert 3 == add(1, 2)
```

3. テストを実行します．
```bash
make test
```
アサーションに失敗すると赤色で内容が表示されます． それが表示されなければ全てのテストに通っています．

特定のファイルにあるテストだけを実行したいときがあると思います．
そういうときはテストしたいファイルとともに `make` を実行してください．
```
make tests/test_sample.py
```

テストには `pytest` を使用しています． 詳しい使い方は[ドキュメント](https://docs.pytest.org/en/6.2.x/)を参照してください．

## Handle linter error
ほとんどのリンタのエラーは修正すべきですが，どうしても修正できないエラーに遭遇するかもしれません．
そういった場合は，コメントを追加することでエラーを無視することができます．

たとえば，このコードをリンタにかけると，
```python
example = lambda: "example"
```

このようなエラーが出力されるはずです．
```
E731 do not assign a lambda expression, use a def
```

`E731` はエラーコードで，続く一文はエラーの内容です．
ここで `# noqa E731` を行の最後に追加することでこのエラーを無視することができます．
```python
example = lambda: "example"  # noqa E731
```

`E731` の代わりに任意のエラーコードを使用できます．
詳しくは [flake8 document](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html#in-line-ignoring-errors) を参照してください．

この方法はある種のワークアラウンドです．
この方法をとるかどうかを PR のレビューで議論するようにしてください．

## CI
GitHub Actions で CI を実行します． 基本的に CI に通っていないブランチをマージしてはいけません．
CI ではテストとコードフォーマット，リンタのエラーがないことの確認をします．
CI の目的には次のようなものがあります．
* コードが正常に動作していることを全体で共有する
* 手元では気づかなかったエラーを発見する
* コードがフォーマットされておりリンタのエラーがない状態であることを強制することで，余計な diff が生まれないようにする