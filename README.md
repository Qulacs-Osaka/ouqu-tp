# ouqu-tp

**ouqu-tp** is a library that allows you to run OpenQASM on qulacs and to transpile circuits to run on real devices.

# Feature

**ouqu-tp** includes the following features:

- Generates runnable OpenQASM files for real quantum computers by applying CNOT constraints and transpiling input OpenQASM files.
- Accepts an OpenQASM file, prepares a quantum state, and executes measurements based on the specified number of shots.
- Accepts an OpenQASM file, prepares a quantum state, receives an observable in OpenFermion format, and precisely calculates the expectation value.
- Accepts an OpenQASM file, prepares a quantum state, receives an observable in OpenFermion format, and estimates the expectation value of observables through sampling based on the specified number of shots.

# Setup

For installation instructions, please refer to the [Setup Guide](Setup.md).

# How To Use

For usage instructions, please refer to the [How to Use Guide](HowToUse.md). (in Japanese)

# How to Contribute

For Contributing, please refer to the [How to contribute Guide](CONTRIBUTING_en.md).

# LICENSE

ouqu-tp is released under the [Apache License 2.0](LICENSE).
