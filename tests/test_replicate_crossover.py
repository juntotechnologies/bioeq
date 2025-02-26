import pytest
import polars as pl
import numpy as np
from pathlib import Path
from bioeq.replicate_crossover import ReplicateCrossover


def generate_partial_replicate_data(n_subjects=12, seed=42):
    """Generate test data for a 3-way partial replicate design"""
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
            within_subject_effect = np.random.normal(0, 0.15)  # 15% within-subject variability
            
            # Generate concentration data for this subject/period
            for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
                # Base PK model (similar to simulation_data_generator.py)
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


def generate_full_replicate_data(n_subjects=12, seed=42):
    """Generate test data for a 4-way full replicate design"""
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
            within_subject_effect = np.random.normal(0, 0.15)  # 15% within-subject variability
            
            # Generate concentration data for this subject/period
            for time in [0, 0.5, 1, 2, 4, 6, 8, 12, 24]:
                # Base PK model (similar to simulation_data_generator.py)
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


@pytest.fixture
def partial_replicate_data():
    """Fixture to provide simulated data for a partial replicate design"""
    return generate_partial_replicate_data()


@pytest.fixture
def full_replicate_data():
    """Fixture to provide simulated data for a full replicate design"""
    return generate_full_replicate_data()


def test_partial_replicate_initialization(partial_replicate_data):
    """Test that the ReplicateCrossover class initializes correctly with partial replicate data"""
    analyzer = ReplicateCrossover(
        data=partial_replicate_data,
        design_type="partial",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Check that params_df has the expected columns
    essential_columns = [
        "SubjectID", "Period", "Sequence", "Formulation", 
        "AUC", "Cmax", "Tmax", "log_AUC", "log_Cmax"
    ]
    
    for col in essential_columns:
        assert col in analyzer.params_df.columns, f"Column {col} missing from params_df"
    
    # Check design type was stored correctly
    assert analyzer.design_type == "partial", "Design type was not correctly stored"
    
    # Check that we have the expected number of rows
    # In a 3-way design, each subject has 3 periods
    expected_rows = len(partial_replicate_data["SubjectID"].unique()) * 3
    assert len(analyzer.params_df) == expected_rows, f"Expected {expected_rows} rows, got {len(analyzer.params_df)}"


def test_full_replicate_initialization(full_replicate_data):
    """Test that the ReplicateCrossover class initializes correctly with full replicate data"""
    analyzer = ReplicateCrossover(
        data=full_replicate_data,
        design_type="full",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Check that params_df has the expected columns
    essential_columns = [
        "SubjectID", "Period", "Sequence", "Formulation", 
        "AUC", "Cmax", "Tmax", "log_AUC", "log_Cmax"
    ]
    
    for col in essential_columns:
        assert col in analyzer.params_df.columns, f"Column {col} missing from params_df"
    
    # Check design type was stored correctly
    assert analyzer.design_type == "full", "Design type was not correctly stored"
    
    # Check that we have the expected number of rows
    # In a 4-way design, each subject has 4 periods
    expected_rows = len(full_replicate_data["SubjectID"].unique()) * 4
    assert len(analyzer.params_df) == expected_rows, f"Expected {expected_rows} rows, got {len(analyzer.params_df)}"


def test_invalid_design_type(partial_replicate_data):
    """Test that an invalid design type raises a ValueError"""
    with pytest.raises(ValueError):
        analyzer = ReplicateCrossover(
            data=partial_replicate_data,
            design_type="invalid",
            subject_col="SubjectID",
            seq_col="Sequence",
            period_col="Period",
            time_col="Time (hr)",
            conc_col="Concentration (ng/mL)",
            form_col="Formulation"
        )


def test_pk_parameter_calculation(partial_replicate_data):
    """Test that PK parameters are calculated correctly"""
    analyzer = ReplicateCrossover(
        data=partial_replicate_data,
        design_type="partial",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Manual calculation for one subject/period
    subject = partial_replicate_data["SubjectID"].unique()[0]
    period = 1
    subject_data = partial_replicate_data.filter(
        (pl.col("SubjectID") == subject) & 
        (pl.col("Period") == period)
    )
    
    # Calculate expected AUC
    times = subject_data["Time (hr)"].to_numpy()
    concs = subject_data["Concentration (ng/mL)"].to_numpy()
    expected_auc = np.trapezoid(concs, times)
    
    # Calculate expected Cmax
    expected_cmax = subject_data["Concentration (ng/mL)"].max()
    
    # Get actual values
    actual_row = analyzer.params_df.filter(
        (pl.col("SubjectID") == subject) & 
        (pl.col("Period") == period)
    )
    
    actual_auc = actual_row["AUC"].item()
    actual_cmax = actual_row["Cmax"].item()
    
    # Check that calculated values are close to expected
    assert np.isclose(actual_auc, expected_auc, rtol=1e-10)
    assert np.isclose(actual_cmax, expected_cmax, rtol=1e-10)


def test_within_subject_cv_calculation(full_replicate_data):
    """Test that within-subject CV is calculated correctly for reference product"""
    analyzer = ReplicateCrossover(
        data=full_replicate_data,
        design_type="full",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Calculate within-subject CV for log_AUC
    cv_results = analyzer.calculate_within_subject_cv("log_AUC")
    
    # Check that results dictionary has expected keys
    assert "within_subject_cv" in cv_results
    assert "mse" in cv_results
    assert "parameter" in cv_results
    
    # Check that parameter name is correct
    assert cv_results["parameter"] == "log_AUC"
    
    # Check that CV is a reasonable value (greater than 0)
    assert cv_results["within_subject_cv"] > 0
    
    # For our simulation, CV should be around 15%
    assert 10 <= cv_results["within_subject_cv"] <= 20, f"Expected CV ~15%, got {cv_results['within_subject_cv']}%"


def test_rsabe_execution(full_replicate_data):
    """Test that reference-scaled average bioequivalence analysis runs without errors"""
    analyzer = ReplicateCrossover(
        data=full_replicate_data,
        design_type="full",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Run RSABE analysis
    results = analyzer.run_rsabe("log_AUC")
    
    # Check that results dictionary has expected keys
    assert "within_subject_cv" in results
    assert "point_estimate" in results
    assert "model_summary" in results
    assert "formula" in results
    assert "be_conclusion" in results
    
    # Check that the formula includes the expected terms
    assert "Formulation" in results["formula"]
    assert "Sequence" in results["formula"]
    assert "Period" in results["formula"]
    
    # Check that point estimate is a reasonable value
    # For our simulation, it should be around 95%
    assert 85 <= results["point_estimate"] <= 105, f"Expected point estimate ~95%, got {results['point_estimate']}%"


def test_summarize_pk_parameters(partial_replicate_data):
    """Test that the summary function produces correct results"""
    analyzer = ReplicateCrossover(
        data=partial_replicate_data,
        design_type="partial",
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Generate summary statistics
    summary = analyzer.summarize_pk_parameters()
    
    # Check that result is a DataFrame
    assert isinstance(summary, pl.DataFrame)
    
    # Check that it has expected columns
    expected_columns = ["Parameter", "Formulation", "N", "Mean", "SD", "Median", "Min", "Max", "CV%"]
    for col in expected_columns:
        assert col in summary.columns, f"Column {col} missing from summary"
    
    # Check that it has expected rows for each parameter and formulation
    assert len(summary) >= 2, "Summary should have at least 2 rows (1 per formulation per parameter)"
    
    # Check that each formulation is represented
    assert "Test" in summary["Formulation"].unique()
    assert "Reference" in summary["Formulation"].unique()
    
    # Check that AUC and Cmax are summarized
    assert "AUC" in summary["Parameter"].unique()
    assert "Cmax" in summary["Parameter"].unique() 