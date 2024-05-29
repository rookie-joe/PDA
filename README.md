# Process-Driven Autoformalization in Lean 4

We note that we have already release our novel proposed benchmark, **Form**alization for **L**ean **4** (**<span style="font-variant: small-caps;">forml4</span>**), and **We will release the code and corresponding finetuned autoformalizer and process-enhanced verifier soon**. This repository is the official implementation of Process-Driven Autoformalization in Lean 4.



## Repository Structure

```
PDA
├── code
│   ├── Automatic-Lean4-Compilation [ref]
│   └── Training-Scripts [todo]    
│       
├── data
│   ├── basic_test.json
│   ├── random_test.json
│   ├── real_test.jsonl
│   └── train.json
```

## Dataset 

The `data` directory includes both training  and testing data (**<span style="font-variant: small-caps;">forml4</span>**) for benchmarking the autoformalization task in Lean 4. This dataset is a key resource for developing and evaluating models that can automate the process of formalizing mathematical statements and proofs.

### Contents of the Dataset

The dataset is organized into the following files, ensuring a comprehensive approach to both training and testing your models:

- `train.json`: The training data file containing 14509 examples to train models. It includes both the formal and informal statements necessary for learning the autoformalization.
- `basic_test.json`: The basic test set (970) is specifically designed to evaluate a model's capability to formalize fundamental theorems. 
- `random_test.json`: The random test set (979) contains a diverse and randomly selected set of problems. 
- `real_test.jsonl`: The real test set represents the out-of-domain test set, featuring 1,000 natural language mathematics questions and answers distilled from the Arithmo test set. 



## Code 



- [x] **Applying Lean 4 Compiler**: Please visit our GitHub repository for more details about how to automate your Lean 4 installation and compilation: [**Automatic Lean 4 Compilation Guide**](https://github.com/rookie-joe/automatic-lean4-compilation)

- [ ] Training autoformalizer and verifier based on (**<span style="font-variant: small-caps;">forml4</span>**) 




## Results

### Performance Limitations of Existing LLMs on **<span style="font-variant: small-caps;">forml4</span>**

| **Model**                     | **Random** |        |        | **Basic** |        |        | **Real** |        |        |
| ----------------------------- | ---------- | ------ | ------ | --------- | ------ | ------ | -------- | ------ | ------ |
|                               | Greedy     | Pass@1 | Pass@5 | Greedy    | Pass@1 | Pass@5 | Greedy   | Pass@1 | Pass@5 |
| **Closed-Source LLMs**        |            |        |        |           |        |        |          |        |        |
| GPT-3.5-Turbo [1]             | 0.41       | 0.32   | 0.73   | 0.29      | 0.00   | 0.66   | 5.10     | 3.80   | 17.00  |
| GPT-4-Turbo [2]               | 0.49       | 0.41   | 3.42   | 1.47      | 1.14   | 4.38   | 10.20    | 8.70   | 25.10  |
| **Open-Source LLMs**          |            |        |        |           |        |        |          |        |        |
| DeepSeek-Math-Base-7B [3]     | 0.17       | 0.21   | 0.95   | 0.34      | 0.22   | 0.81   | 0.00     | 0.00   | 0.00   |
| DeepSeek-Math-Instruct-7B [3] | 0.58       | 0.22   | 1.71   | 1.16      | 0.47   | 3.04   | 0.30     | 1.60   | 5.30   |
| LLEMMA-7B [4]                 | 0.00       | 0.00   | 0.77   | 0.17      | 0.10   | 0.45   | 0.00     | 0.00   | 0.00   |
| LLEMMA-34B [4]                | 0.00       | 0.00   | 0.18   | 0.00      | 0.00   | 0.00   | 0.00     | 0.00   | 0.00   |
| InternLM-Math-7B [5]          | 0.00       | 0.00   | 0.18   | 0.19      | 0.14   | 0.26   | 1.10     | 1.00   | 3.70   |
| InternLM-Math-20B [5]         | 0.00       | 0.00   | 0.00   | 0.00      | 0.00   | 0.00   | 0.20     | 0.70   | 2.30   |
| Mistral-Instruct-v0.2-7B [6]  | 0.28       | 0.21   | 1.86   | 0.45      | 0.77   | 1.82   | 0.30     | 0.50   | 1.90   |



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

| Dataset | OSV<br />MP1 | OSV <br />Acc | OSV <br />Recall | OSV + <br />MP1 | OSV + <br />Acc | OSV + <br /> Recall | PSV <br /> MP1 | PSV <br /> Acc | PSV <br />Recall | PSV + <br /> MP1 | PSV +<br />Acc | PSV + <br />Recall |
| ------- | ------------ | ------------- | ---------------- | --------------- | --------------- | ------------------- | -------------- | -------------- | ---------------- | ---------------- | -------------- | ------------------ |
| Basic   | 40.71        | 81.34         | 80.12            | 45.13           | 84.22           | 83.18               | 41.49          | 84.59          | 82.73            | 47.30            | 89.14          | 94.17              |
| Random  | 36.14        | 81.16         | 81.07            | 38.21           | 83.13           | 84.45               | 37.52          | 84.68          | 83.47            | 44.32            | 84.20          | 93.70              |
| Real    | 25.75        | 84.45         | 86.21            | 33.41           | 84.45           | 86.21               | 33.42          | 84.34          | 81.08            | 45.10            | 94.18          | 89.31              |



## Contributing

To contribute to this project, please follow the guidelines provided in `CONTRIBUTING.md`. We welcome contributions from the community, including bug fixes, enhancements, or documentation.





## References

1. OpenAI "GPT-3.5 Turbo", 2023

2. Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. "Gpt-4 technical report." _arXiv preprint arXiv:2303.08774_, 2023

3. Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. "Deepseekmath: Pushing the limits of mathematical reasoning in open language models." _CoRR, abs/2402.03300_, 2024 

4. Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Albert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck. "Llemma: An open language model for mathematics." _CoRR, abs/2310.10631_, 2023

5. Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao, Zhaoye Fei, Yichuan Ma, Jiawei Hong, Kuikun Liu, Ziyi Wang, Yudong Wang, Zijian Wu, Shuaibin Li, Fengzhe Zhou, Hongwei Liu, Songyang Zhang, Wenwei Zhang, Hang Yan, Xipeng Qiu, Jiayu Wang, Kai Chen, and Dahua Lin. "Internlm-math: Open math large language models toward verifiable reasoning." _CoRR, abs/2402.06332_, 2024.

6. Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. "Mistral 7b." _CoRR, abs/2310.06825_, 2023.



## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), a Creative Commons Attribution 4.0 International License.

Feel free to reach out with questions or for collaboration.
