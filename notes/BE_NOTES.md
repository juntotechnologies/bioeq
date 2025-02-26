
1. Study Design
Use a two-treatment crossover design:
Healthy subjects receive both test (T) and reference (R) products on separate occasions.
Random assignment to the two sequences of administration (e.g., T-R or R-T).
Evaluate either single-dose or multiple-dose regimens.
2. Primary Measures
Common pharmacokinetic (PK) measures for BE:
AUC (Area Under the Curve): Total drug exposure.
Cmax (Peak Concentration): Maximum drug concentration observed.
Logarithmic transformation of PK data is recommended to stabilize variance and ensure normality.
3. Average Bioequivalence (ABE)
Statistical Basis:
Compare population geometric means of T and R products.
Use the two one-sided tests procedure to determine equivalence:
Test if T is not significantly less than R.
Test if T is not significantly greater than R.
Confidence Interval:
Compute a 90% confidence interval (CI) for the ratio of averages (T/R).
BE is established if the CI falls within the predefined limits, typically 80% to 125%.
4. Variability in Population and Individual-Level BE
Population BE:
Assesses both averages and total variability across the population.
Useful for understanding population-wide consistency.
Individual BE:
Accounts for:
Within-subject variability for T and R.
Subject-by-formulation interaction variance: Variation in individual response differences to T and R.
Helps ensure consistent performance at the individual level.
5. Statistical Considerations
Logarithmic Transformation:
Transform PK data (e.g., AUC, Cmax) to the natural log scale before analysis.
Use transformed data for mean ratio and confidence interval calculations.
Sequence Effects:
Evaluate the effect of administration sequence (T-R vs. R-T) on the outcomes.
Incorporate in the statistical model if necessary.
Outliers:
Identify and handle outlier data points, as they can skew results.
6. Implementation Outline for the Package
Core Functions:
Import PK data and handle transformations (log scale).
Perform calculations for ABE:
Compute geometric means and ratios.
Calculate 90% confidence intervals.
Check if CI falls within 80%-125%.
Include optional extensions for Population and Individual BE:
Assess total variability for PBE.
Evaluate within-subject variability and subject-by-formulation interaction variance for IBE.
Statistical Models:
Use ANOVA or mixed-effects models for BE analysis.
Implement sequence effect testing, if needed.
Visualization:
Plot confidence intervals, variability measures, and comparisons between T and R products.
7. Regulatory Limits
Predefined BE limits are typically 80% to 125% for the ratio of product averages.
These limits may vary for specific drug types, e.g., narrow therapeutic index drugs.
By incorporating these elements, your Python package can robustly analyze BE studies and support ABE, PBE, and IBE frameworks.

### Bioequivalence (BE) Study Workflow

When analyzing data for a bioequivalence study, follow this structured workflow to ensure consistency and respect for the study design.

1. Group by Subject (subj)
Analyze data for each subject individually to account for intra-subject variability. Each subject's data is handled separately.

2. Sequence (seq)
Separate data by treatment sequence (e.g., TR, RT). This step accounts for cross-over designs where treatments are administered in different orders.

3. Period (prd)
Split the data by period (e.g., Period 1, Period 2). Each period corresponds to a specific timeframe in the study, typically associated with a single drug administration.

4. Drug (drug)
Within each period, separate Test (T) and Reference (R) treatments. Compare pharmacokinetic (PK) parameters between the two drugs.

5. Time (time)
Organize data by sampling time points. Concentration-time curves for each drug are created and analyzed to calculate key PK parameters:

Cmax: Maximum concentration.
AUC: Area under the concentration-time curve.
6. Concentration (conc)
Use the concentration values at each time point to compute PK metrics. These metrics are the basis for statistical comparisons to determine bioequivalence.

Hierarchy of Analysis
The recommended order of operations is:

subj → seq → prd → drug → time → conc

Example Workflow for a Single Subject
Subject 1 (subj=1), Sequence = TR:
Period 1 (prd=1): Analyze Test (T) drug concentrations over time.
Period 2 (prd=2): Analyze Reference (R) drug concentrations over time.
Special Case: Parallel Designs
For parallel designs, skip seq and prd. Compare Test (T) vs. Reference (R) directly across subjects.

This workflow ensures consistency, respects the study design, and captures key sources of variability for accurate bioequivalence analysis.
