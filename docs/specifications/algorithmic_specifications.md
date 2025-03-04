# BioEq Algorithmic Specifications

This document provides detailed specifications of the algorithms implemented in the BioEq package, including mathematical bases and references to established scientific literature.

## 1. Pharmacokinetic Parameter Calculations

### 1.1 Area Under the Curve (AUC)

#### Implementation Details
The AUC is calculated using the trapezoidal rule:

```
AUC = Σ [(Ci + Ci+1) × (ti+1 - ti)] / 2
```

where:
- Ci is the concentration at time point i
- ti is the time at point i

#### References
- Gabrielsson, J., & Weiner, D. (2012). *Pharmacokinetic and Pharmacodynamic Data Analysis: Concepts and Applications*. Swedish Pharmaceutical Press, 5th edition.
- FDA Guidance for Industry (2014). *Bioavailability and Bioequivalence Studies Submitted in NDAs or INDs — General Considerations*. Section III.A.

### 1.2 AUC Extrapolation to Infinity

#### Implementation Details
AUC extrapolated to infinity is calculated as:

```
AUC∞ = AUClast + Clast / λz
```

where:
- AUClast is the AUC from time 0 to the last measured time point
- Clast is the last measured concentration
- λz is the terminal elimination rate constant

#### References
- Rowland, M., & Tozer, T. N. (2010). *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. Lippincott Williams & Wilkins, 4th edition.
- European Medicines Agency (2010). *Guideline on the Investigation of Bioequivalence*. Section 4.1.4.

### 1.3 Terminal Elimination Rate Constant and Half-Life

#### Implementation Details
The terminal elimination rate constant (λz) is estimated using log-linear regression of the terminal phase:

```
log(C) = log(C0) - λz × t
```

Half-life is calculated as:

```
t1/2 = ln(2) / λz
```

The terminal phase is identified using the last three non-zero concentration points.

#### References
- Shargel, L., Wu-Pong, S., & Yu, A. B. (2012). *Applied Biopharmaceutics & Pharmacokinetics*. McGraw-Hill Medical, 6th edition.
- FDA Statistical Approaches to Establishing Bioequivalence (2001). Section III.A.

## 2. Statistical Analysis Methods

### 2.1 ANOVA for Crossover Designs

#### Implementation Details
For a 2×2 crossover design, the ANOVA model is:

```
Yijk = μ + Si + Pj + Fk + Cik + εijk
```

where:
- Yijk is the response (log-transformed PK parameter)
- μ is the overall mean
- Si is the sequence effect
- Pj is the period effect
- Fk is the formulation effect
- Cik is the subject within sequence effect
- εijk is the random error

#### References
- Jones, B., & Kenward, M. G. (2014). *Design and Analysis of Cross-Over Trials*. Chapman and Hall/CRC, 3rd edition.
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section III.B.2.

### 2.2 Mixed Effects Models

#### Implementation Details
The mixed effects model extends the ANOVA by treating subjects as random effects:

```
Yijk = μ + Si + Pj + Fk + γik + εijk
```

where γik represents the random effect of subject i in sequence k.

#### References
- Chow, S. C., & Liu, J. P. (2008). *Design and Analysis of Bioavailability and Bioequivalence Studies*. Chapman and Hall/CRC, 3rd edition.
- European Medicines Agency (2010). *Guideline on the Investigation of Bioequivalence*. Section 4.1.8.

### 2.3 T-tests for Parallel Designs

#### Implementation Details
For parallel designs, a two-sample t-test is used to compare means between test and reference groups:

```
t = (X̄T - X̄R) / √(s²(1/nT + 1/nR))
```

where:
- X̄T and X̄R are the means of the test and reference groups
- s² is the pooled variance
- nT and nR are the sample sizes

Welch's t-test is used to accommodate potentially unequal variances.

#### References
- Welch, B. L. (1947). The generalization of "Student's" problem when several different population variances are involved. *Biometrika*, 34(1/2), 28-35.
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section III.B.1.

### 2.4 Calculation of 90% Confidence Intervals

#### Implementation Details
For log-transformed data, the 90% confidence interval for the test/reference ratio is calculated as:

```
exp(log(T/R) ± t(0.95, df) × SE(log(T/R)))
```

where:
- T/R is the test/reference ratio
- t(0.95, df) is the 95th percentile of the t-distribution with df degrees of freedom
- SE(log(T/R)) is the standard error of the log-transformed ratio

#### References
- Schuirmann, D. J. (1987). A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. *Journal of Pharmacokinetics and Biopharmaceutics*, 15(6), 657-680.
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section III.B.3.

## 3. Data Handling Procedures

### 3.1 Handling Missing Data

#### Implementation Details
Missing data points are excluded from calculations. For AUC calculations, the trapezoidal rule is applied to available data points.

#### References
- Little, R. J., & Rubin, D. B. (2019). *Statistical Analysis with Missing Data*. John Wiley & Sons, 3rd edition.
- European Medicines Agency (2010). *Guideline on Missing Data in Confirmatory Clinical Trials*. Section 4.

### 3.2 Calculation of Summary Statistics

#### Implementation Details
Summary statistics (mean, standard deviation, coefficient of variation, median, min, max) are calculated for each PK parameter by treatment group.

CV% is calculated as:
```
CV% = (SD / Mean) × 100
```

#### References
- Zhang, P. (2016). *Statistical Analysis in Pharmaceutical Sciences*. John Wiley & Sons, 1st edition.
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section IV.A.

## 4. Bioequivalence Assessment

#### Implementation Details
Bioequivalence is established if the 90% confidence interval for the test/reference ratio of geometric means for the primary PK parameters (AUC and Cmax) falls within the 80-125% limits.

#### References
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section III.A.
- European Medicines Agency (2010). *Guideline on the Investigation of Bioequivalence*. Section 4.1.8.
- Schuirmann, D. J. (1987). A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. *Journal of Pharmacokinetics and Biopharmaceutics*, 15(6), 657-680.

## 5. Reference-Scaled Average Bioequivalence (RSABE)

### 5.1 Within-Subject Variability Calculation

#### Implementation Details
For replicate designs, the within-subject variability of the reference formulation is calculated using the following approach:

1. For each subject, calculate the variance of log-transformed PK parameters (AUC or Cmax) across multiple administrations of the reference product.
2. Average these variances across all subjects to obtain the mean squared error (MSE), which represents the within-subject variance (s²ᵂᵣ).
3. Convert this to a coefficient of variation using the formula:
   
   ```
   CV% = sqrt(exp(s²ᵂᵣ) - 1) × 100
   ```

#### References
- FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence (2001). Section III.B.4.
- Davit, B. M., et al. (2012). Highly Variable Drugs: Observations from Bioequivalence Data Submitted to the FDA for New Generic Drug Applications. *The AAPS Journal*, 14(1), 148-158.

### 5.2 Reference-Scaled Average Bioequivalence Analysis

#### Implementation Details
For highly variable drugs (within-subject CV ≥ 30%), the FDA allows scaling of bioequivalence limits based on the variability of the reference product. The approach uses a linearized criterion:

```
(μᵀ - μᵣ)² - θ·s²ᵂᵣ ≤ 0
```

where:
- μᵀ and μᵣ are the means for test and reference products
- s²ᵂᵣ is the within-subject variance for the reference product
- θ is a regulatory constant (0.893 for FDA approach)

This criterion can be restated in terms of expanded bioequivalence limits:

```
exp(±k·sᵂᵣ)
```

where:
- k = ln(1.25)/sᵂᵣ if sᵂᵣ < ln(1.25)/ln(√2)
- k = ln(√2) if sᵂᵣ ≥ ln(1.25)/ln(√2)

This limits the expansion to 50-200% regardless of how variable the reference product is.

The test is implemented using a mixed effects model with the following components:
1. Fixed effects for sequence, period, and formulation
2. Random effect for subject (nested within sequence)
3. Estimation of the test-reference difference and its variance
4. Application of the linearized criterion

#### References
- FDA Guidance for Industry: Bioequivalence Studies With Pharmacokinetic Endpoints for Drugs Submitted Under an ANDA (2013).
- Davit, B. M., et al. (2008). Comparing Generic and Innovator Drugs: A Review of 12 Years of Bioequivalence Data from the United States Food and Drug Administration. *The Annals of Pharmacotherapy*, 42(10), 1493-1497.
- Haidar, S. H., et al. (2008). Bioequivalence Approaches for Highly Variable Drugs and Drug Products. *Pharmaceutical Research*, 25(1), 237-241. 