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


def generate_crossover_2x2(n_subjects=24, seed=42):
    """
    Generate simulated data for a 2x2 crossover design
    """
    np.random.seed(seed)

    # Define sequences
    sequences = ["TR", "RT"]

    # Initialize data list
    data = []

    for subject in range(1, n_subjects + 1):
        # Assign sequence (alternating)
        sequence = sequences[(subject - 1) % len(sequences)]

        # Subject-specific parameter
        subject_effect = np.random.normal(0, 0.2)  # 20% between-subject variability

        for period in range(1, 3):  # 2 periods
            # Determine formulation based on sequence and period
            if sequence == "TR":
                formulation = "Test" if period == 1 else "Reference"
            else:  # "RT"
                formulation = "Reference" if period == 1 else "Test"

            # Formulation effect (Test is 95% of Reference)
            formulation_effect = 0.95 if formulation == "Test" else 1.0

            # Period effect (slight decrease in period 2)
            period_effect = 1.0 if period == 1 else 0.95

            # Within-subject variability for the period
            within_subject_effect = np.random.normal(0, 0.1)  # 10% within-subject variability

            # Generate concentration data for this subject/period
            for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
                # Base PK model
                if time == 0:
                    conc = 0
                else:
                    ka = 1.0  # absorption rate
                    ke = 0.1  # elimination rate
                    dose = 100
                    vd = 10

                    conc = (
                        (dose * formulation_effect / vd)
                        * (ka / (ka - ke))
                        * (np.exp(-ke * time) - np.exp(-ka * time))
                    )

                # Apply effects (multiplicative on the concentration)
                conc = conc * np.exp(subject_effect) * period_effect * np.exp(within_subject_effect)

                # Add random error
                error = np.random.normal(0, 0.05)  # 5% residual error
                observed_conc = max(0, conc * np.exp(error))

                data.append({
                    "SubjectID": subject,
                    "Period": period,
                    "Sequence": sequence,
                    "Formulation": formulation,
                    "Time (hr)": time,
                    "Concentration (ng/mL)": observed_conc
                })

    return pl.DataFrame(data)


def generate_parallel_design(n_subjects=40, seed=42):
    """
    Generate simulated data for a parallel design
    """
    np.random.seed(seed)

    # Define formulations
    formulations = ["Test", "Reference"]

    # Initialize data list
    data = []

    for subject in range(1, n_subjects + 1):
        # Assign formulation (alternating)
        formulation = formulations[(subject - 1) % len(formulations)]

        # Subject-specific parameter
        subject_effect = np.random.normal(0, 0.3)  # 30% between-subject variability

        # Formulation effect (Test is 95% of Reference)
        formulation_effect = 0.95 if formulation == "Test" else 1.0

        # Generate concentration data for this subject
        for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
            # Base PK model
            if time == 0:
                conc = 0
            else:
                ka = 1.0  # absorption rate
                ke = 0.1  # elimination rate
                dose = 100
                vd = 10

                conc = (
                    (dose * formulation_effect / vd)
                    * (ka / (ka - ke))
                    * (np.exp(-ke * time) - np.exp(-ka * time))
                )

            # Apply effects (multiplicative on the concentration)
            conc = conc * np.exp(subject_effect)

            # Add random error
            error = np.random.normal(0, 0.05)  # 5% residual error
            observed_conc = max(0, conc * np.exp(error))

            data.append({
                "SubjectID": subject,
                "Formulation": formulation,
                "Time (hr)": time,
                "Concentration (ng/mL)": observed_conc
            })

    return pl.DataFrame(data)


def generate_partial_replicate_data(n_subjects=12, seed=42):
    """
    Generate simulated data for a 3-way partial replicate design (TRR, RTR, RRT)
    
    This design is commonly used for highly variable drugs and allows for
    the estimation of within-subject variability for the reference product.
    """
    np.random.seed(seed)
    
    # Define sequences for partial replicate (TRR, RTR, RRT)
    sequences = ["TRR", "RTR", "RRT"]
    
    # Initialize data list
    data = []
    
    for subject in range(1, n_subjects + 1):
        # Assign sequence (cycling through sequences)
        sequence = sequences[(subject - 1) % len(sequences)]
        
        # Subject-specific parameter
        subject_effect = np.random.normal(0, 0.2)  # 20% between-subject variability
        
        for period in range(1, 4):  # 3 periods
            # Determine formulation based on sequence and period
            if sequence == "TRR":
                formulation = "Test" if period == 1 else "Reference"
            elif sequence == "RTR":
                formulation = "Reference" if period in [1, 3] else "Test"
            elif sequence == "RRT":
                formulation = "Reference" if period in [1, 2] else "Test"
                
            # Formulation effect (Test is 95% of Reference)
            formulation_effect = 0.95 if formulation == "Test" else 1.0
            
            # Period effect (slight decrease over periods)
            period_effect = 1.0 - (period - 1) * 0.05
            
            # Within-subject variability for the period
            # Higher within-subject variability (30%) to simulate a highly variable drug
            within_subject_effect = np.random.normal(0, 0.3)
            
            # Generate concentration data for this subject/period
            for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
                # Base PK model
                if time == 0:
                    conc = 0
                else:
                    ka = 1.0  # absorption rate
                    ke = 0.1  # elimination rate
                    dose = 100
                    vd = 10
                    
                    conc = (
                        (dose * formulation_effect / vd)
                        * (ka / (ka - ke))
                        * (np.exp(-ke * time) - np.exp(-ka * time))
                    )
                
                # Apply effects (multiplicative on the concentration)
                conc = conc * np.exp(subject_effect) * period_effect * np.exp(within_subject_effect)
                
                # Add random error
                error = np.random.normal(0, 0.1)  # 10% residual error
                observed_conc = max(0, conc * np.exp(error))
                
                data.append({
                    "SubjectID": subject,
                    "Period": period,
                    "Sequence": sequence,
                    "Formulation": formulation,
                    "Time (hr)": time,
                    "Concentration (ng/mL)": observed_conc
                })
    
    return pl.DataFrame(data)


def generate_full_replicate_data(n_subjects=24, seed=42):
    """
    Generate simulated data for a 4-way full replicate design (TRTR, RTRT)
    
    This design is commonly used for highly variable drugs and provides the most
    information about within-subject variability for both test and reference products.
    """
    np.random.seed(seed)
    
    # Define sequences for full replicate (TRTR, RTRT)
    sequences = ["TRTR", "RTRT"]
    
    # Initialize data list
    data = []
    
    for subject in range(1, n_subjects + 1):
        # Assign sequence (alternating)
        sequence = sequences[(subject - 1) % len(sequences)]
        
        # Subject-specific parameter
        subject_effect = np.random.normal(0, 0.2)  # 20% between-subject variability
        
        for period in range(1, 5):  # 4 periods
            # Determine formulation based on sequence and period
            if sequence == "TRTR":
                formulation = "Test" if period % 2 == 1 else "Reference"
            elif sequence == "RTRT":
                formulation = "Reference" if period % 2 == 1 else "Test"
                
            # Formulation effect (Test is 95% of Reference)
            formulation_effect = 0.95 if formulation == "Test" else 1.0
            
            # Period effect (slight decrease over periods)
            period_effect = 1.0 - (period - 1) * 0.05
            
            # Within-subject variability for the period
            # Higher within-subject variability (30%) to simulate a highly variable drug
            within_subject_effect = np.random.normal(0, 0.3)
            
            # Generate concentration data for this subject/period
            for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
                # Base PK model
                if time == 0:
                    conc = 0
                else:
                    ka = 1.0  # absorption rate
                    ke = 0.1  # elimination rate
                    dose = 100
                    vd = 10
                    
                    conc = (
                        (dose * formulation_effect / vd)
                        * (ka / (ka - ke))
                        * (np.exp(-ke * time) - np.exp(-ka * time))
                    )
                
                # Apply effects (multiplicative on the concentration)
                conc = conc * np.exp(subject_effect) * period_effect * np.exp(within_subject_effect)
                
                # Add random error
                error = np.random.normal(0, 0.1)  # 10% residual error
                observed_conc = max(0, conc * np.exp(error))
                
                data.append({
                    "SubjectID": subject,
                    "Period": period,
                    "Sequence": sequence,
                    "Formulation": formulation,
                    "Time (hr)": time,
                    "Concentration (ng/mL)": observed_conc
                })
    
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
    
    # Generate and save the datasets
    crossover_2x2_data = generate_crossover_2x2()
    parallel_design_data = generate_parallel_design()
    partial_replicate_data = generate_partial_replicate_data()
    full_replicate_data = generate_full_replicate_data()
    
    # Save to CSV files
    crossover_2x2_data.write_csv(output_dir / "crossover_2x2_simdata.csv")
    parallel_design_data.write_csv(output_dir / "parallel_design_simdata.csv")
    partial_replicate_data.write_csv(output_dir / "partial_replicate_simdata.csv")
    full_replicate_data.write_csv(output_dir / "full_replicate_simdata.csv")
    
    print("Simulation data generated and saved to CSV files.") 