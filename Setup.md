# Setup

## Setting Up the Environment for Users

#### Tools required for installation

- Install [staq](https://github.com/softwareQinc/staq/wiki/Installation-instructions) (setup yourself)
- Install python
- Install ouqu-tp with the following command:

```
pip install ouqu-tp
```


## Setting Up the Environment for Developers

### To run in a VSCode + Devcontainer environment

In VSCode, you can set up the environment using a devcontainer.

For more details, please refer to the [documentation](https://github.com/Qulacs-Osaka/qulacs-developer-docs/blob/main/doc/Learn-Usage/devcontainer-manual.md).
To clone ouqu-tp, use the following command. (**Note: This is not scikit-qulacs!**)

```
git clone https://github.com/Qulacs-Osaka/ouqu-tp.git
```

### To run in a Docker environment

The Dockerfile for setting up the environment is provided under the `.devcontainer` directory.
By using the following command, you can enter a virtual environment pre-configured with the necessary software.
Any operations performed under the `/ouqu-tp` directory inside Docker will also be reflected outside Docker.

```
docker build .devcontainer -t ouqu-tp-docker-image
docker run -it --mount type=bind,source=`pwd`,target=/ouqu-tp ouqu-tp-docker-image
```

### To run locally

#### Tools required for installation

- Install [staq](https://github.com/softwareQinc/staq/wiki/Installation-instructions) (setup yourself)
- Install python
- Install Poetry (recommended) or pip

Other tools will be automatically installed by Poetry or pip.

#### If garbled characters occur when installing staq

One of the steps in the installation process involves compilation, during which errors may occur due to character encoding issues (e.g., "constants continue onto line 2").
In such cases, converting the source code's character encoding to UTF-8 with BOM may resolve the compilation errors.

## Before Running ouqu-tp

You need to install the required dependencies.
Use either Poetry or pip to install them.

Using Poetry:
```
poetry install
```

Using pip:
```
pip install .
```
