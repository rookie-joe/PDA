# PDA annotation guideline  
### Here is instructions on your annotation:
- General Task Objective: To verify the semantic alignment between informal and formal theorem statement.
- Labeling criteria for **semantic alignment**: whether the output fulfills the instructions in translating semantically equivalent statements from formal language of Lean 4 to natural language (i.e., **informalization**), or from natural language to formal language of Lean 4 (i.e., **autoformalization**). *You only need to check the semantical alignment in statements, not in proof.*
- Important Notes: 
    - Do not change the keys or values other than where you put labels. In particular, DO NOT MODIFY the `"uuid"`.

### You will receive a file in which each sample contains the following keys for review:
- `"formal"`: the formal theorem statement and proof combined witten in Lean 4, which is extracted from Mathlib 4.
- `"nl_statement"`: the problem statement written in natural language.
- `"nl_proof"`: the proof or solution to the problem written in natural language. It provides a step-by-step explanation of how to solve the problem. 
- `"fl_statementproof"`: the formal theorem statement and proof combined written in Lean 4, which is the autoformalized output by the model to be evaluated.

### You need to annotate two items per sample:
1. `"human_eval_inform"`: Considering the definition of an informalization task, whether the output (`"nl_statement"`) is semantically aligned with the input (formal statement in `"formal"`). Label 'true' if aligned, 'false' if misaligned.
    - Note: If the `formal` field in a sample is 'null', it means the theorem does not contain a statement or proof in natural language. In this case, skip annotating `"human_eval_inform"` and enter 'null' instead.
2. `"human_eval_autoform"`: Considering the definition of an autoformalization task, whether the output (formal statement in `"fl_statementproof"`) is semantically aligned with the input (`"nl_statement"`). Label 'true' if aligned, 'false' if misaligned.

### Tips:
1. You can use the tool 'json editor' to help with reviewing and labeling the data file: https://jsoneditoronline.org/;
2. You can use this website to assist in reading the latex format of the informal statement in natural languages: https://www.latexlive.com/##.
