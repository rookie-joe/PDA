# Human Evaluation Results

This sub-directory contains human evaluation results for three stages of PDA:
- **Before informalization (stage I)**: We conduct a human evaluation on cross-model preference comparison between gpt-4o and gemini-pro-1.5 (sample size = 10);
- **After informalization (stage II)**: After informalizating the FormL4 dataset, we conduct a manual quality check on informalization success by randomly sampling from three different test sets (sample size = 60).
- **After autoformalization training (stage III)**: After completing training and enhancing the autoformalizer model, the model's autoformalization output was evaluated by human evaluators (sample size = 80).



## Breakdown
The `annotation` sub-directory contains two folders:

- `model_comparison` folder contains:
    - `eval_protocol.md`: human evaluation protocol for annotating the informalization success and model preference comparison in stage I.
    - `gemini_sample10_merged_annotation` & `gpt4o_sample10_merged_annotation`: human evaluation labels for annotating the informalization success and model preference comparison in stage I.

- `informalization_autoformalization` folder contains:
    - `annotation_protcol.md`: human evaluation protocol for annotating the informalization success in stage II and autoformalization success and III.
    - `Final_FormL4_Annotation.json`: human evaluation results for annotating the informalization success in stage II and autoformalization success and III. Impact factors are also labeled and included, such as 'pda_validity' and 'model'. See the annotation protocol for detailed information.
