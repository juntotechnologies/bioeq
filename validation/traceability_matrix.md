# BioEq Traceability Matrix

This document maps functional requirements to their implementation in code and verification through tests.

## Area Under the Curve (AUC) Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-2.1.1 | Calculate AUC using trapezoidal rule | `_calculate_auc()` in both `Crossover2x2` and `ParallelDesign` | `test_pk_parameter_calculation()` in both test files | Complete |
| FR-2.1.2 | Handle non-uniform time points | `np.trapezoid()` in `_calculate_auc()` | Included in `test_pk_parameter_calculation()` | Complete |
| FR-2.1.3 | Calculate AUC from time zero to last time point | `_calculate_auc()` | `test_pk_parameter_calculation()` | Complete |
| FR-2.1.4 | Calculate AUC extrapolated to infinity | `_calculate_auc_extrapolated()` | Not specifically tested | Partial |
| FR-2.1.5 | Report percentage of AUC extrapolated | Not implemented | Not tested | Planned |

## Maximum Concentration (Cmax) Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-2.2.1 | Determine maximum observed concentration | `_calculate_cmax()` | `test_pk_parameter_calculation()` | Complete |
| FR-2.2.2 | Identify time point of Cmax (Tmax) | `_calculate_tmax()` | Not specifically tested | Partial |

## Elimination Parameters Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-2.3.1 | Calculate terminal elimination rate constant | `_calculate_half_life()` | Not specifically tested | Partial |
| FR-2.3.2 | Calculate elimination half-life | `_calculate_half_life()` | Not specifically tested | Partial |
| FR-2.3.3 | Provide criteria for selecting terminal phase points | Fixed selection of last 3 points in `_calculate_half_life()` | Not tested | Partial |

## Crossover Design Analysis Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-3.1.1 | Perform ANOVA for 2×2 crossover designs | `run_anova()` in `Crossover2x2` | `test_run_anova()` | Complete |
| FR-3.1.2 | Include sequence, period, and treatment effects | Formula in `run_anova()` | `test_run_anova()` | Complete |
| FR-3.1.3 | Calculate least-squares means | Not explicitly implemented | Not tested | Planned |
| FR-3.1.4 | Implement mixed-effects models | `run_nlme()` in `Crossover2x2` | `test_run_nlme()` | Complete |

## Parallel Design Analysis Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-3.2.1 | Perform t-tests comparing test and reference | `run_ttest()` in `ParallelDesign` | `test_run_ttest()` | Complete |
| FR-3.2.2 | Perform ANOVA with treatment as only factor | `run_anova()` in `ParallelDesign` | `test_run_anova()` | Complete |

## Bioequivalence Assessment Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-3.3.1 | Calculate point estimates for Test/Reference ratio | `calculate_point_estimate()` in both classes | `test_point_estimate()` | Complete |
| FR-3.3.2 | Calculate 90% confidence intervals | `calculate_point_estimate()` | `test_point_estimate()` | Complete |
| FR-3.3.3 | Assess bioequivalence criteria (80-125%) | `calculate_point_estimate()` | `test_point_estimate()` | Complete |
| FR-3.3.4 | Perform analyses on log-transformed parameters | `_calculate_log_transform()` | Indirectly in point estimate tests | Complete |

## Data Management Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-4.1 | Accept data in standardized formats | Not directly implemented, relies on Polars | Not tested | Planned |
| FR-4.2 | Validate input data | `_validate_data()` and `_validate_colvals()` | Not specifically tested | Partial |
| FR-4.3 | Handle missing data appropriately | Partial implementation | Not specifically tested | Partial |
| FR-4.4 | Provide data summary statistics | `summarize_pk_parameters()` | `test_summarize_pk_parameters()` | Complete |

## Reporting Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-5.1 | Generate summary tables of PK parameters | `summarize_pk_parameters()` | `test_summarize_pk_parameters()` | Complete |
| FR-5.2 | Produce statistical output in standard format | Print statements in analysis methods | Not specifically tested | Partial |
| FR-5.3 | Export results to standard formats | `export_results()` | Not tested | Partial |
| FR-5.4 | Provide measures of variability | Included in `summarize_pk_parameters()` | `test_summarize_pk_parameters()` | Complete |

## Validation and Quality Control Requirements

| Req ID | Requirement Description | Implementation | Test Coverage | Status |
|--------|-------------------------|----------------|--------------|--------|
| FR-6.1 | Provide detailed documentation of methods | Docstrings in code | Not applicable | Partial |
| FR-6.2 | Include references to established literature | Not implemented | Not applicable | Planned |
| FR-6.3 | Maintain traceability | This document | Not applicable | Initiated |
| FR-6.4 | Include comprehensive test coverage | Test modules | Test coverage reports | Partial |
| FR-7.1 | Produce consistent results | Deterministic implementations | Indirectly tested | Partial |
| FR-7.2 | Maintain calculation precision | Using appropriate data types | Not specifically tested | Partial |
| FR-7.3 | Validate inputs and provide error messages | Validation methods | Not specifically tested | Partial |
| FR-7.4 | Maintain audit trail | Not implemented | Not tested | Planned |

## Status Summary

- **Complete**: 15 requirements
- **Partial**: 16 requirements
- **Planned**: 7 requirements
- **Total**: 38 requirements

This traceability matrix will be updated as development progresses. 