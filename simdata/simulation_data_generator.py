import numpy as np
import polars as pl
from pathlib import Path


def generate_crossover_data(
    n_subjects=12,
    periods=2,
    time_points=None,
    test_reference_ratio=0.95,
    inter_subject_cv=0.2,
    intra_subject_cv=0.15,
    residual_error=0.1,
    seed=42,
):
    """
    Generates simulation data for a two-period, two-sequence crossover bioequivalence study.

    Parameters:
    -----------
    n_subjects : int
        Number of subjects in the study (default: 12).
    periods : int
        Number of periods (default: 2).
    time_points : list
        List of time points for PK sampling (default: [0, 0.5, 1, 2, 4, 6, 8, 12, 24]).
    test_reference_ratio : float
        True ratio of Test/Reference formulations (default: 0.95).
    inter_subject_cv : float
        Coefficient of variation for between-subject variability (default: 0.2).
    intra_subject_cv : float
        Coefficient of variation for within-subject variability (default: 0.15).
    residual_error : float
        Standard deviation for residual error (default: 0.1).
    seed : int
        Random seed for reproducibility (default: 42).

    Returns:
    --------
    pl.DataFrame
        Simulated dataset with columns:
        - SubjectID: Subject identifier
        - Period: Study period (1 or 2)
        - Sequence: Sequence assignment (RT or TR)
        - Formulation: Treatment formulation (Reference or Test)
        - Time (hr): Time point
        - Concentration (ng/mL): Observed concentration
    """
    if time_points is None:
        time_points = [0, 0.5, 1, 2, 4, 6, 8, 12, 24]

    np.random.seed(seed)

    sequences = ["TR", "RT"]
    formulations = ["Reference", "Test"]

    # Between-subject variability
    subject_effects = np.random.normal(0, inter_subject_cv, n_subjects)

    data = []

    for subject_idx, subject in enumerate(range(1, n_subjects + 1)):
        # Assign sequence alternating between TR and RT
        sequence = sequences[subject_idx % 2]
        
        # Within-subject variability per period
        period_effects = np.random.normal(0, intra_subject_cv, periods)

        for period in range(1, periods + 1):
            if (sequence == "TR" and period == 1) or (sequence == "RT" and period == 2):
                formulation = formulations[0]  # Reference
                formulation_effect = 1.0
            else:
                formulation = formulations[1]  # Test
                formulation_effect = test_reference_ratio

            for time in time_points:
                # Base PK model with first-order absorption and elimination
                ka = 1.0  # Absorption rate constant
                ke = 0.1  # Elimination rate constant
                f = 1.0   # Bioavailability
                dose = 100  # Nominal dose
                vd = 10    # Volume of distribution
                
                # True concentration based on one-compartment model
                if time == 0:
                    true_concentration = 0
                else:
                    true_concentration = (
                        (f * dose * formulation_effect / vd)
                        * (ka / (ka - ke))
                        * (np.exp(-ke * time) - np.exp(-ka * time))
                    )
                
                # Add subject and period effects (multiplicative on log scale)
                subject_effect = np.exp(subject_effects[subject_idx])
                period_effect = np.exp(period_effects[period - 1])
                
                # Add random residual error
                error = np.random.normal(0, residual_error)
                observed_concentration = max(
                    0, true_concentration * subject_effect * period_effect * np.exp(error)
                )

                data.append(
                    {
                        "SubjectID": subject,
                        "Period": period,
                        "Sequence": sequence,
                        "Formulation": formulation,
                        "Time (hr)": time,
                        "Concentration (ng/mL)": observed_concentration,
                    }
                )

    return pl.DataFrame(data)


def generate_parallel_data(
    n_subjects_per_arm=20,
    time_points=None,
    test_reference_ratio=0.95,
    inter_subject_cv=0.2,
    residual_error=0.1,
    seed=42,
):
    """
    Generates simulation data for a parallel design bioequivalence study.

    Parameters:
    -----------
    n_subjects_per_arm : int
        Number of subjects per treatment arm (default: 20).
    time_points : list
        List of time points for PK sampling (default: [0, 0.5, 1, 2, 4, 6, 8, 12, 24]).
    test_reference_ratio : float
        True ratio of Test/Reference formulations (default: 0.95).
    inter_subject_cv : float
        Coefficient of variation for between-subject variability (default: 0.2).
    residual_error : float
        Standard deviation for residual error (default: 0.1).
    seed : int
        Random seed for reproducibility (default: 42).

    Returns:
    --------
    pl.DataFrame
        Simulated dataset with columns:
        - SubjectID: Subject identifier
        - Formulation: Treatment formulation (Reference or Test)
        - Time (hr): Time point
        - Concentration (ng/mL): Observed concentration
    """
    if time_points is None:
        time_points = [0, 0.5, 1, 2, 4, 6, 8, 12, 24]

    np.random.seed(seed)

    formulations = ["Reference", "Test"]
    total_subjects = n_subjects_per_arm * 2

    # Between-subject variability
    subject_effects = np.random.normal(0, inter_subject_cv, total_subjects)

    data = []

    for subject_idx, subject in enumerate(range(1, total_subjects + 1)):
        # Assign formulation (first half to Reference, second half to Test)
        formulation_idx = 0 if subject <= n_subjects_per_arm else 1
        formulation = formulations[formulation_idx]
        
        # Formulation effect
        formulation_effect = 1.0 if formulation == "Reference" else test_reference_ratio

        for time in time_points:
            # Base PK model with first-order absorption and elimination
            ka = 1.0  # Absorption rate constant
            ke = 0.1  # Elimination rate constant
            f = 1.0   # Bioavailability
            dose = 100  # Nominal dose
            vd = 10    # Volume of distribution
            
            # True concentration based on one-compartment model
            if time == 0:
                true_concentration = 0
            else:
                true_concentration = (
                    (f * dose * formulation_effect / vd)
                    * (ka / (ka - ke))
                    * (np.exp(-ke * time) - np.exp(-ka * time))
                )
            
            # Add subject effect (multiplicative on log scale)
            subject_effect = np.exp(subject_effects[subject_idx])
            
            # Add random residual error
            error = np.random.normal(0, residual_error)
            observed_concentration = max(
                0, true_concentration * subject_effect * np.exp(error)
            )

            data.append(
                {
                    "SubjectID": subject,
                    "Formulation": formulation,
                    "Time (hr)": time,
                    "Concentration (ng/mL)": observed_concentration,
                }
            )

    return pl.DataFrame(data)


if __name__ == "__main__":
    # Create simdata directory if it doesn't exist
    output_dir = Path("simdata")
    output_dir.mkdir(exist_ok=True)
    
    # Generate crossover design dataset
    crossover_data = generate_crossover_data(n_subjects=12)
    crossover_file = output_dir / "crossover_simdata.csv"
    crossover_data.write_csv(crossover_file)
    print(f"Crossover simulated data saved to {crossover_file}")
    
    # Generate parallel design dataset
    parallel_data = generate_parallel_data(n_subjects_per_arm=20)
    parallel_file = output_dir / "parallel_simdata.csv"
    parallel_data.write_csv(parallel_file)
    print(f"Parallel simulated data saved to {parallel_file}") 