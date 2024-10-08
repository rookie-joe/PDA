'''
calculate the average scores for both "autoform" and "inform" tasks, inter-rater agreement, intra-rater standard deviation, 
and then group these analyses based on the pda_valid, model, and source labels.
'''

import json
import numpy as np
import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy import stats

################################################################################################################
print("Avg and IAA stats")
print("-"*60)

# Load your JSON data
with open('Final_FormL4_Annotation.json', 'r', encoding='utf-8') as f:
    annotated_samples = json.load(f)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(annotated_samples)

# Calculate average scores for autoform and inform
for task in ['eval_inform', 'eval_autoform']:
    # Collect relevant columns for this task
    relevant_columns = [col for col in df.columns if col.startswith(f'human') and task in col]
    
    # Convert None to int (e.g., fill None with 0) before averaging
    for col in relevant_columns:
        # print(col)
        # print(df[col])
        df[col] = df[col].fillna(-1).astype(int)  # Fill None and NaN values with -1
        # print(df[col])

    # # Filter out samples with None for 'formal' if the task is 'eval_inform'
    # if task == 'eval_inform':
    #     df = df[df['formal'].notna()]
    
    # Replace -1 with NaN for mean calculation
    df[relevant_columns] = df[relevant_columns].replace(-1, np.nan)

    # Calculate average for this task across samples
    df[f'avg_{task}'] = df[relevant_columns].mean(axis=1)

# Now calculate the overall averages
overall_avg_autoform = df['avg_eval_autoform'].mean()
overall_avg_inform = df['avg_eval_inform'].mean()

# Calculate inter-rater agreement using Fleiss' Kappa
def calculate_fleiss_kappa(data, task):
    contingency_table = []
    for sample in data:
        # Create a row for the current sample
        row = [0, 0]  # Assuming binary classification (0 or 1)
        for i in range(1, 5):  # Assuming human1 to human4
            col_name = f'human{i}_{task}'
            if col_name in sample and sample[col_name] is not None:
                if sample[col_name] in [0, 1]:
                    row[int(sample[col_name])] += 1  # Count the number of votes for each label
        contingency_table.append(row)
    
    return fleiss_kappa(np.array(contingency_table))

# kappa_autoform = calculate_fleiss_kappa(df.to_dict(orient='records'), 'eval_autoform')
# kappa_inform = calculate_fleiss_kappa(df.to_dict(orient='records'), 'eval_inform')

# Calculate intra-rater standard deviation
intra_rater_std_dev = {
    'autoform': df[[col for col in df.columns if 'eval_autoform' in col]].std(axis=0).mean(),
    'inform': df[[col for col in df.columns if 'eval_inform' in col]].std(axis=0).mean(),
}

# Output the overall results
print(f"Overall average autoform score: {overall_avg_autoform:.2f}")
print(f"Overall average inform score: {overall_avg_inform:.2f}")
# print(f"Fleiss' Kappa for autoform: {kappa_autoform:.4f}")
# print(f"Fleiss' Kappa for inform: {kappa_inform:.4f}")
print(f"Intra-rater standard deviation for autoform: {intra_rater_std_dev['autoform']:.2f}")
print(f"Intra-rater standard deviation for inform: {intra_rater_std_dev['inform']:.2f}")
print("-"*60)


################################################################################################################
print("Factorial Analaysis: ANOVA")
print("-"*60)

# Melt the DataFrame to long format for ANOVA
df_melted = pd.melt(df, id_vars=['pda_valid', 'model', 'source'], 
                    value_vars=['avg_eval_autoform', 'avg_eval_inform'],
                    var_name='task', value_name='average_score')

# Convert categorical variables to category dtype
df_melted['pda_valid'] = df_melted['pda_valid'].astype('category')
df_melted['model'] = df_melted['model'].astype('category')
df_melted['source'] = df_melted['source'].astype('category')

# Create a group column for post-hoc tests
df_melted['group'] = df_melted['pda_valid'].astype(str) + "_" + df_melted['source'].astype(str)

# Now filter the melted DataFrame for each task
df_autoform = df_melted[df_melted['task'] == 'avg_eval_autoform']
df_inform = df_melted[df_melted['task'] == 'avg_eval_inform']

# ANOVA for autoform
model_autoform = ols('average_score ~ pda_valid * model * source', data=df_autoform).fit()
anova_results_autoform = anova_lm(model_autoform)
print("ANOVA Results for Autoform:")
print(anova_results_autoform)

# Tukey's HSD for autoform
tukey_results_autoform = pairwise_tukeyhsd(endog=df_autoform['average_score'], groups=df_autoform['group'], alpha=0.05)
print("\n\nTukey's HSD Results for Autoform:")
print(tukey_results_autoform)

# ANOVA for inform
model_inform = ols('average_score ~ pda_valid * model * source', data=df_inform).fit()
anova_results_inform = anova_lm(model_inform)
print("\n\nANOVA Results for Inform:")
print(anova_results_inform)

# Tukey's HSD for inform
tukey_results_inform = pairwise_tukeyhsd(endog=df_inform['average_score'], groups=df_inform['group'], alpha=0.05)
print("\n\nTukey's HSD Results for Inform:")
print(tukey_results_inform)

################################################################################################################
print('\n\nGrouping Avg Stats Comparisons\n', '-'*60)
# Function to calculate average scores and Fleiss' Kappa for each group
def compare_groups(df, task):
    # Group by the specified factor and calculate the average scores
    avg_scores = df.groupby(task)[['avg_eval_autoform', 'avg_eval_inform']].mean().reset_index()
    return avg_scores

def compare_groups_with_math(df):
    # Calculate average scores for autoform, including all sources
    source_avg_autoform = df.groupby('source')[['avg_eval_autoform']].mean().reset_index()

    # Calculate average scores for inform, excluding math
    source_avg_inform = df[df['source'] != 'math'].groupby('source')[['avg_eval_inform']].mean().reset_index()

    return source_avg_autoform, source_avg_inform

# Get average scores for each factor
pda_valid_comparison = compare_groups(df, 'pda_valid')
model_comparison = compare_groups(df, 'model')
source_comparison_autoform, source_comparison_inform = compare_groups_with_math(df)

# Print the results
print("Average Scores by PDA Validity:")
print(pda_valid_comparison)
print("\nAverage Scores by Model:")
print(model_comparison)
print("\nAverage Scores by Source (Autoform including 'math'):")
print(source_comparison_autoform)
print("\nAverage Scores by Source (Inform excluding 'math'):")
print(source_comparison_inform)

################################################################################################################
print('-'*60, '\n\n', 'Simple T-test:', '-'*60)
from scipy import stats

# # Function to perform t-tests between groups
# def perform_t_tests(df, task):
#     results = []
#     groups = df[task].unique()
    
#     for i in range(len(groups)):
#         for j in range(i + 1, len(groups)):
#             group1 = df[df[task] == groups[i]]['average_score']
#             group2 = df[df[task] == groups[j]]['average_score']
#             t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)  # Use Welch's t-test
#             results.append((groups[i], groups[j], t_stat, p_value))
    
#     return pd.DataFrame(results, columns=[task + '_1', task + '_2', 't_stat', 'p_value'])

# # Conduct t-tests for each factor
# pda_valid_t_test_results = perform_t_tests(df_melted, 'pda_valid')
# model_t_test_results = perform_t_tests(df_melted, 'model')
# source_t_test_results = perform_t_tests(df_melted, 'source')

# # Print the results
# print("\nT-Test Results for PDA Validity:")
# print(pda_valid_t_test_results)
# print("\nT-Test Results for Model:")
# print(model_t_test_results)
# print("\nT-Test Results for Source:")
# print(source_t_test_results)


# Conduct t-tests on the factors for the two dependent variables: autoform and inform
print('\n\nT-test Comparisons\n', '-'*60)

# Function to perform t-tests for two groups
def perform_ttest(df, factor, task):
    unique_groups = df[factor].unique()

    # Ensure there are only two groups for t-test
    if len(unique_groups) == 2:
        group1 = df[df[factor] == unique_groups[0]][f'avg_{task}']
        group2 = df[df[factor] == unique_groups[1]][f'avg_{task}']

        t_stat, p_value = stats.ttest_ind(group1.dropna(), group2.dropna(), equal_var=False)
        return t_stat, p_value
    else:
        print(f"Cannot perform t-test on {factor} for {task}: More than two groups present.")
        return None, None

# Perform t-tests for autoform and inform across different factors
for factor in ['pda_valid', 'model', 'source']:
    for task in ['eval_autoform', 'eval_inform']:
        t_stat, p_value = perform_ttest(df, factor, task)
        if t_stat is not None:
            print(f"T-test for {factor} on {task}: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")
