# Protocol for comparative evaluation of model informalization quality
## Introduction
The protocol provides guidance for evaluating the quality of informalization of two sampled models (gpt4-o and gemini-pro-1.5). 
Two models are tasked to translate theorem statements and their proof written in Lean 4 syntax to natural language (i.e., informalization), so that the natural language problem statement and proof can be understood by readers without any lean 4 knowledge. 

Given a theorem and proof, the models are prompted to respond following the format below:
- Theorem: (the given theorem and proof in lean 4, to be translated)
- Problem: (translated theorem statement in natural language)
- Explanation: (proof in natural language, explaining the functions in lean 4)
- Proof: (proof in natural language, understandable by any human reader without the knowledge of lean 4 functions)

## File Structure
You are given two model output .json files (sample size = 10). In the file, each sample contains five items:
- "nl": (past informalized output. Ignore)
- "formal": formal statement and proof in lean 4 (i.e., Theorem)
- "gemini_output" / gpt4o_output: complete model output
- "nl_problem": extracted from model output (i.e., Problem)
- "nl_explanation": extracted from model output (i.e., Explanation)
- "nl_proof": extracted from model output (i.e., Proof)

Among them, your annotations focus on the quality of "nl_problem" and "nl_proof" per sample.

## Task

For both model output .json files, you need to annotate three items:

1. informalization success (T/F): whether the translation from **"formal"** to **"nl_problem" and "nl_proof"** is semantically equivalent. The natural-language translation should accurately convey the same logical structure and content as the original statement and proof in Lean 4.
2. informal proof correctness (T/F): whether the informalized proof **"nl_proof"** successfully proves the problem statement **"nl_problem"**, and can be independently understood without prior knowledge of Lean 4.
3. model preference (T/F): Compare the informalization output (i.e., **"nl_problem" + "nl_proof"**) between gemini and gpt4o, choose which one is preferable based on the criteria described below. Label T if prefered, F if not.

## Quality Criteria
The ideal informalized output should meet the following criteria:
1. semantically equivalent to the Lean 4 theorem and proof. (informalization success = T)
2. both problem statement and proof use intuitive terms without Lean 4 functions mentioned, proves the intended theorem succesfully, and can be independently understood without prior knowledge of Lean 4. (informal proof correctness = T)

Check the instruction and demo examples in the fewshot prompt for reference of an ideal informalization case.
You can use tools like https://jsoneditoronline.org/ to compare two model output files more easily.