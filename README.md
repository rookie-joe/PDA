# Process-Driven Autoformalization in Lean 4

We note that we will release our novel proposed benchmark, **Form**alization for **L**ean **4** (**<span style="font-variant: small-caps;">forml4</span>**), and **We will release the code and corresponding finetuned process-enhanced verifier soon**. This repository is the official implementation of Process-Driven Autoformalization in Lean 4.



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



## Requirements



Below we outlier the steps and Please visit our GitHub repository for more details about  how to automate your Lean 4 installation: [**Automatic Lean 4 Compilation Guide**](https://github.com/rookie-joe/automatic-lean4-compilation)



### Prerequisites

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



### Installation

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



### Usage

After installation, you can benchmark and evaluate the autoformalization as follows:

```bash
python3 pass_rate_new.py --input_path {input_path} --output_path {output_path}
```

- `input_path`: Directory containing `*.json` files with `"statement"` and predependencies for Lean4 compilation.
- `output_path`: A text file where the compilation process and final results will be written.



## Dataset [todo]

The `data` directory includes both training and testing data (**<span style="font-variant: small-caps;">forml4</span>**) for benchmarking the autoformalization task in Lean 4. It provides sampled cases due to size limitations, giving an overview of the benchmark.



## Results

### Performance Limitations of Existing LLMs on **<span style="font-variant: small-caps;">forml4</span>**

| **Model**                     | **Random Test** |        |        | **Basic Test** |        |        | **Real Test** |        |        |
| ----------------------------- | --------------- | ------ | ------ | -------------- | ------ | ------ | ------------- | ------ | ------ |
|                               | Greedy          | Pass@1 | Pass@5 | Greedy         | Pass@1 | Pass@5 | Greedy        | Pass@1 | Pass@5 |
| **Closed-Source LLMs**        |                 |        |        |                |        |        |               |        |        |
| GPT-3.5-Turbo~[1]             | 0.41            | 0.32   | 0.73   | 0.29           | 0.00   | 0.66   | 5.10          | 3.80   | 17.00  |
| GPT-4-Turbo~[2]               | 0.49            | 0.41   | 3.42   | 1.47           | 1.14   | 4.38   | 10.20         | 8.70   | 25.10  |
| **Open-Source LLMs**          |                 |        |        |                |        |        |               |        |        |
| DeepSeek-Math-Base-7B~[3]     | 0.17            | 0.21   | 0.95   | 0.34           | 0.22   | 0.81   | 0.00          | 0.00   | 0.00   |
| DeepSeek-Math-Instruct-7B~[3] | 0.58            | 0.22   | 1.71   | 1.16           | 0.47   | 3.04   | 0.30          | 1.60   | 5.30   |
| LLEMMA-7B~[4]                 | 0.00            | 0.00   | 0.77   | 0.17           | 0.10   | 0.45   | 0.00          | 0.00   | 0.00   |
| LLEMMA-34B~[4]                | 0.00            | 0.00   | 0.18   | 0.00           | 0.00   | 0.00   | 0.00          | 0.00   | 0.00   |
| InternLM-Math-7B~[5]          | 0.00            | 0.00   | 0.18   | 0.19           | 0.14   | 0.26   | 1.10          | 1.00   | 3.70   |
| InternLM-Math-20B~[5]         | 0.00            | 0.00   | 0.00   | 0.00           | 0.00   | 0.00   | 0.20          | 0.70   | 2.30   |
| Mistral-Instruct-v0.2-7B~[6]  | 0.28            | 0.21   | 1.86   | 0.45           | 0.77   | 1.82   | 0.30          | 0.50   | 1.90   |



### Autoformalization Enhancement

#### Performance Comparison of the Enhanced Autoformalizer

We evaluate and compare the performance of an enhanced autoformalization model that incorporates a verifier in its process. This model is denoted as "RFT + Verifier (Ours)" and is compared against baseline and RFT (Rejective Sampling Fine-tuning) models. The RFT approach selects outputs that successfully compile for further fine-tuning of the baseline model, whereas our method additionally checks for correctness as evaluated by the verifier. The results are summarized in the following table.

| Model                 | Quantity | Quality (Acc.) | Test Sets - Basic | Test Sets - Random | Test Sets - Real |
| --------------------- | -------- | -------------- | ----------------- | ------------------ | ---------------- |
| Baseline              | -        | -              | 40.92             | 35.88              | 23.90            |
| RFT                   | + 65K    | 100%           | 44.50             | 38.70              | 26.50            |
| Verifier (Ours)       | + 74K    | 80.50%         | 43.80             | 38.04              | 25.70            |
| RFT + Verifier (Ours) | + 60K    | 100%           | 46.28             | 39.38              | 27.90            |





#### Comparative Performance of the Enhanced Verifier Models

Next, we further evaluated an enhanced verifier by applying it to outputs from the RFT+Verifier model. The evaluation was conducted in relation to a pre-defined experimental setup, comparing process-supervised training (PSV +), which builds upon the previous PSV model, and outcome-supervised training (OSV +), which improves upon OSV. The results can be seen in the table below.

| Dataset | OSV - MP1 | OSV - Acc | OSV - Recall | OSV + - MP1 | OSV + - Acc | OSV + - Recall | PSV - MP1 | PSV - Acc | PSV - Recall | PSV + - MP1 | PSV + - Acc | PSV + - Recall |
| ------- | --------- | --------- | ------------ | ----------- | ----------- | -------------- | --------- | --------- | ------------ | ----------- | ----------- | -------------- |
| Basic   | 40.71     | 81.34     | 80.12        | 45.13       | 84.22       | 83.18          | 41.49     | 84.59     | 82.73        | 47.30       | 89.14       | 94.17          |
| Random  | 36.14     | 81.16     | 81.07        | 38.21       | 83.13       | 84.45          | 37.52     | 84.68     | 83.47        | 44.32       | 84.20       | 93.70          |
| Real    | 25.75     | 84.45     | 86.21        | 33.41       | 84.45       | 86.21          | 33.42     | 84.34     | 81.08        | 45.10       | 94.18       | 89.31          |



## Contributing

To contribute to this project, please follow the guidelines provided in `CONTRIBUTING.md`. We welcome contributions from the community, including bug fixes, enhancements, or documentation.



## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), a Creative Commons Attribution 4.0 International License.

Feel free to reach out with questions or for collaboration.
