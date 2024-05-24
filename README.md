# Process-Driven Autoformalization in Lean 4

**We will release the code and corresponding finetuned process-enhanced verifier soon**. This repository is the official implementation of  Process-Driven Autoformalization in Lean 4.



## Repository Structure

```
FORML4
├── code
│   └── Automatic-Lean4-Compilation
│       ├── REPL
│       │   ├── Lean
│       │   │   └── InfoTree
│       │   └── Util
│       └── test
└── data
    └── sample
        ├── test
        └── train
```



# Requirements



Below we outlier the steps and Please visit our GitHub repository for more details about  how to automate your Lean 4 installation: [**Automatic Lean 4 Compilation Guide**](https://github.com/rookie-joe/automatic-lean4-compilation)



## Prerequisites

To set up your environment to run the code, you need to have Linux. Other platforms can follow Lean 4 documentation for setup.

To install requirements for Lean 4 and other dependencies:

- Install elan:



```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

- For Linux users, install additional dependencies:



```bash
wget -q https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/install_debian.sh && bash install_debian.sh ; rm -f install_debian.sh && source ~/.profile
```

For non-Linux platforms, refer to the [Lean4 setup documentation](https://lean-lang.org/lean4/doc/setup.html).



## Installation

To work with **Automatic Lean4 Compilation**:

1. Clone the repository:



```bash
git clone https://github.com/xx/automatic-lean4-compilation
```

1. Navigate to the directory:



```bash
cd automatic-lean4-compilation
```

1. Install mathlib using lake:



```bash
lake update
```

1. Verify the installation by running tests with the Lean compiler:



```bash
echo '{ "cmd" : "def f := 2" }'| lake exe repl
echo '{"path": "test/test.lean", "allTactics": true}' | lake exe repl
```

- A successful test will output `{"env": 0}`.



## Usage

After installation, you can benchmark and evaluate the autoformalization as follows:

```bash
python3 pass_rate_new.py --input_path {input_path} --output_path {output_path}
```

- `input_path`: Directory containing `*.json` files with `"statement"` and predependencies for Lean4 compilation.
- `output_path`: A text file where the compilation process and final results will be written.





# Dataset [todo]

The `data` directory includes both training and testing data for benchmarking the autoformalization task in Lean 4. It provides sampled cases due to size limitations, giving an overview of the benchmark.



# Contributing

To contribute to this project, please follow the guidelines provided in `CONTRIBUTING.md`. We welcome contributions from the community, including bug fixes, enhancements, or documentation.





# License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), a Creative Commons Attribution 4.0 International License.

Feel free to reach out with questions or for collaboration.
