import numpy as np
import polars as pl

def generate_simulation_data(n_subjects=5, periods=2, time_points=None, sigma=1.0, seed=42):
    """
    Generates simulation data for a two-period, two-sequence crossover bioequivalence study.

    Parameters:
    n_subjects (int): Number of subjects in the study.
    periods (int): Number of periods (default: 2).
    time_points (list): List of time points (default: [0, 0.5, 1, 2, 4, 6, 8]).
    sigma (float): Standard deviation for concentration variability.
    seed (int): Random seed for reproducibility.

    Returns:
    pl.DataFrame: Simulated dataset.
    """
    if time_points is None:
        time_points = [0, 0.5, 1, 2, 4, 6, 8]

    np.random.seed(seed)

    sequences = ['TR', 'RT']
    formulations = ['Reference', 'Test']

    data = []

    for subject in range(1, n_subjects + 1):
        # Assign sequence randomly to subjects
        sequence = np.random.choice(sequences)

        for period in range(1, periods + 1):
            formulation = formulations[0] if (sequence == 'TR' and period == 1) or (sequence == 'RT' and period == 2) else formulations[1]

            for time in time_points:
                # Simulate concentration values using an exponential decay model with added noise
                true_concentration = 50 * np.exp(-0.5 * time)  # Exponential decay model
                observed_concentration = max(0, true_concentration + np.random.normal(0, sigma))

                data.append({
                    'SubjectID': subject,
                    'Period': period,
                    'Sequence': sequence,
                    'Formulation': formulation,
                    'Time (hr)': time,
                    'Concentration (ng/mL)': observed_concentration
                })

    return pl.DataFrame(data)

# Generate the dataset
data = generate_simulation_data(n_subjects=5)  # Reduced to 5 subjects for minimal dataset

# Save to CSV
output_file = "./bioeq_simdata_1.csv"
data.write_csv(output_file)

# Display first few rows of the dataset
print(f"Simulated data saved to {output_file}")
print(data.head())
