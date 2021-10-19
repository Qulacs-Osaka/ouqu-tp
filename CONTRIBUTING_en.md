# How to contribute
## Prerequisite
Install poetry. This tool resolves dependencies, build the package, and publish it.

Installation in Linux and macOS:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

In Windows:
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

Detailed instruction: [poetry documentation](https://python-poetry.org/docs/#installation)

## Using poetry
We introduce basic usage of poetry here.
For further information, refer to [Basic usage](https://python-poetry.org/docs/basic-usage) and [Commands](https://python-poetry.org/docs/cli/).

### Virtual environment
poetry creates a virtual environment to manage dependencies.
When you use VSCode, it is useful to create it under the root of the project.
First, change configuration.
```bash
poetry config virtualenvs.in-project true
```
And in VSCode setting, select `./.venv/bin/python`(`./.venv/Scripts/python.exe` in Windows) as Python interpreter of the project.

### Dependency management
poetry manages list of dependencies in `pyproject.toml`.
To add a new dependency to the file, run
```bash
poetry add numpy
```

If you want to install a package only for development, add `-D` flag.
```bash
poetry add -D black
```

And install dependencies
```bash
poetry install
```
This command updates `poetry.lock`. Any developer can install exact same version of dependencies with this file, so be sure to commit this file.

You can update dependencies to latest versions with following command.
```bash
poetry update
```

### Run scripts and commands
You can run scripts and commands in the virtual environment.
```bash
poetry run python main.py
poetry run python
```

In other words, you cannot use packages you installed in the virtual environment if you just run `python main.py`.

### Build and publish
To build the project to wheel archive, just run:
```bash
poetry build
```

For publish the package, refer to [How to Publish a Python Package to PyPI using Poetry](https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-using-poetry-aa804533fc6f).

## Start coding
1. Clone this repository.
2. Synchronize with `main` branch.
```bash
git switch main
git pull
```

3. Create branch with name describing a feature you are going to develop. Branch name format is `${ISSUE_NUMBER}-${FEATURE}`
```bash
git switch -c 99-wonderful-model
```

4. Install dependencies. This is not needed when there is no dependency installed recently.
```bash
poetry install
```

5. Then write your code. If you create a new file, add it to git index for following steps.
```bash
git add NEW_FILE
```

6. Format, lint, and test your code.
```
make check
make test
```

If you have format or lint error, you can use this command to try fixing it automatically.
```
make format
```

There might remain some errors. They cannot be fixed automatically, so fix them manually.

7. After coding, commit and push changes.
```bash
git add -p
git commit
# For the first push in the branch
git push -u origin 99-wonderful-model
# After first push
git push
```

8. Create a pull request(PR) after you finish the development at the branch. Basically you need someone to review your code. After reviewer approved and all CI passed, merge the branch to `main`.

## Testing
Write tests when you develop a new feature. Tests are executed automatically.

1. Create `test_*.py` in `tests` directory. Describe what to test in the file name.
2. Create a function whose name starts with `test_`. Write assertion to check if a function you developed is compliant with a specification. For example, a test for a function calculating sum of two integers is like following.
```python
from your_module import add
def test_add():
    assert 3 == add(1, 2)
```

3. Then run tests.
```bash
make test
```
If the assertion fails, error contents are displayed with red. If you do not see that, all test are successful.

You might want to run tests only in specific files.
In that case, run `make` with file(s) you want to test.
```bash
make tests/test_sample.py
```

We use `pytest` for testing. Detailed instructions are available in the [document](https://docs.pytest.org/en/6.2.x/).

## Handle linter error
Most linter errors must be fixed, but you may encounter some linter errors which you cannot fix.
In this case, you can ignore the error by adding some comments.

For example, if you check this code with linter,
```python
example = lambda: "example"
```

you will got an error something like this:
```
E731 do not assign a lambda expression, use a def
```

`E731` is error code and following text is the contents of the error.
You can ignore this error by adding `# noqa E731` at the end of line.
```python
example = lambda: "example"  # noqa E731
```

Any linter error code is acceptable instead of `E731`.
You can find more information at [flake8 document](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html#in-line-ignoring-errors).

This method is a kind of workaround.
You should discuss on a PR review whether this approach is adopted.

## CI
Run CI at GitHub Actions. You should not merge a branch unless CI passes.
In CI, we run tests and check code format and linter error.
The purpose of CI is
* Share our code works properly in the team.
* Find error you cannot notice at your local machine.
* Avoid unnecessary diff by forcing code format and linter error.
