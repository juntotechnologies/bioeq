# Concise notes basedon reading info/02_Statistical-Approaches-to-Establishing-Bioequivalence.pdf

common terms:

1. `within-subject variability`: natural variation in PK param (e.g. Cmax, AUC) within same individual across repeated administrations of same formulation. Highly variable drugs (HVDs) require scaled BE to be studied.
    - Managed through 2 period, 2 seq (crossover study) designs where each subject serves as its own control.
    - High within-subject variability might necessitate larger sample sizes or regulatory adjustments such as scaled BE limits for HVDs.

2. `subject-by-formulation interaction`: refers to the differences in BA of test and reference formulations due to the subject's unique physiology.
    - important to be accounted for in individual BE studies
    - smoothed over in mean BE studies because population-level averages so not a concern there
    - to account for the interaction term explicitly, needs additional statistical modeling (mixed-effects model)

3. `mixed effects models`
    - account for both `fixed` and `random` effects
      - `fixed`: params that apply to whole population (e.g. average effect of treatment), like avg diff in Cmax between test and ref formulations
      - `random`: patient-specific (e.g. subject-by-formulation interaction) or other random variations not explained by fixed effects
    - enables analysis with multiple sources of variability (within-subject, between-subject)

4. `sequence`: order in which treatments/formulations/druges are given; used as a param. in a model to determine sequence-related effects
5. `period`: timeframe in which a treatment is administered (in 2x2 crossover, 2 periods; 1 is first administration of T or R, 2 is second administration after washout period to fully elim. 1st drug); used as a param. in a model to determine period-related effects

There are 3 types of bioequivalence calculations

1. `mean bioequivalence` (Most commonly used and simple)

- 3 components:
  - `population-level averages`
  - `confidence-intervals` (90% CI for test/ref ratio for PK means, must fall in 80-125% range to show BE)
  - `variability considerations` (within-subject, not subject-by-formulation)
- gold standard
- FDA & EMA require mean BE for approving generic drugs
- compares geometric means of PK params (Cmax & AUC) between test & ref
- used for following reasons
  - simple, well-established, aligns with regulatory guidelines
  - suitable for 2 period/2 seq (2x2) crossover designs

1. `populational bioequivalence`

- extends `mean BE` by incorporating *both* population means and variances to compare ref & test
- key components:
  - `population-level averages`
  - `variances`: it also looks at `total variability` (between- & within-subject) to ensure test formulation doesn't introduce excessive variability in the population
  - `statistical focus`: incorporates standard deviations of PK metrics into BE calc
  - Rarely used, more theoretical

3. `individual bioequivalence`

- accounts for within-subject variability and subject-by-formulation interactions
- reference/constant/mixed scaling are valid approaches
- occasionally used since has special use-cases
