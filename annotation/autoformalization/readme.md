# Dataset README

This dataset contains a collection of math problems and their corresponding proofs. Each item in the dataset is represented as a JSON object with the following key-value pairs:

## Key-Value Pairs

1. `"nl_statement"`: This key represents the problem statement in natural language. It describes the math problem that needs to be solved. In the given example, the problem statement is about finding the area of the shaded region common to both squares when a square with side length 1 is rotated about one vertex by an angle α, where 0° < α < 90° and cos α = 4/5.

2. `"nl_proof"`: This key contains the proof or solution to the math problem in natural language. It provides a step-by-step explanation of how to solve the problem. In the given example, the proof describes the geometric relationships and calculations needed to determine the area of the shaded region.

3. `"fl_statementproof"`: This key represents the formal language version of the problem statement and proof combined. It is written in a formal language or notation, such as Lean4. In the given example, the formal language version is a theorem named `area_of_half_square_rotated` that states the equality between `1 / 2` and `(2 : ℝ) / 4` using the `norm_num` tactic.

4. `"pda_valid"`: This key indicates whether the `fl_statementproof` can pass the Lean4 compiler with or without the proof. It is important to note that all samples in this dataset without a proof can pass the Lean4 compiler, meaning the statement is syntactically true. When `"pda_valid"` is `true`, it means that the statement along with the proof cannot pass the Lean4 compiler, indicating that either the statement cannot be proven or the proof is not correct.

5. `"source"`: This key specifies the source or origin of the math problem. It can be used to categorize or label the problems based on their source. In the given example, the source is labeled as `"math"`, indicating that the problem belongs to the mathematics domain.

## PDA Validity

The `"pda_valid"` key is a boolean value that indicates whether the `fl_statementproof` can pass the Lean4 compiler with or without the proof.

- If `"pda_valid"` is `true`, it means that the statement along with the proof cannot pass the Lean4 compiler. This suggests that either the statement cannot be proven or the proof is not correct.
- If `"pda_valid"` is `false`, it means that the statement alone (without the proof) can pass the Lean4 compiler, indicating that the statement is syntactically true.

It's important to note that all samples in this dataset without a proof can pass the Lean4 compiler, ensuring the syntactic correctness of the statements.

Please note that the provided example is just one instance of the dataset, and the actual dataset may contain multiple JSON objects with different math problems and proofs.