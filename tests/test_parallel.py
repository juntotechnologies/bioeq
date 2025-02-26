import pytest
import polars as pl
import numpy as np
from pathlib import Path
from bioeq.parallel import ParallelDesign


@pytest.fixture
def simulated_parallel_data():
    """Fixture to provide simulated parallel design data for testing"""
    try:
        # First try to load from file
        file_path = Path("simdata/parallel_simdata.csv")
        if file_path.exists():
            return pl.read_csv(file_path)
    except Exception:
        pass
        
    # Otherwise import the generator and create data
    try:
        from simdata.simulation_data_generator import generate_parallel_data
        return generate_parallel_data(n_subjects_per_arm=10)
    except ImportError:
        # Create minimal test data if the generator is not available
        data = []
        for subject in range(1, 21):  # 20 subjects
            if subject <= 10:
                formulation = "Reference"
            else:
                formulation = "Test"
                
            for time in [0, 1, 2, 4, 8]:
                if formulation == "Reference":
                    conc = 10 * np.exp(-0.1 * time) + np.random.normal(0, 0.5)
                else:
                    conc = 9.5 * np.exp(-0.1 * time) + np.random.normal(0, 0.5)
                    
                data.append({
                    "SubjectID": subject,
                    "Formulation": formulation,
                    "Time (hr)": time,
                    "Concentration (ng/mL)": max(0, conc)
                })
                
        return pl.DataFrame(data)


def test_parallel_initialization(simulated_parallel_data):
    """Test that the ParallelDesign class initializes correctly"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Check that params_df has all the expected columns
    expected_columns = [
        "SubjectID", "Formulation", 
        "AUC", "Cmax", "Tmax", "log_AUC", "log_Cmax", "t_half", "AUC_inf"
    ]
    
    # Allow some flexibility in the half-life calculations 
    # which might be None for some subjects
    essential_columns = [
        "SubjectID", "Formulation", 
        "AUC", "Cmax", "Tmax", "log_AUC", "log_Cmax"
    ]
    
    for col in essential_columns:
        assert col in analyzer.params_df.columns, f"Column {col} missing from params_df"
    
    # Check that we have the expected number of rows
    expected_rows = len(simulated_parallel_data["SubjectID"].unique())  # should be one row per subject
    assert len(analyzer.params_df) == expected_rows, f"Expected {expected_rows} rows, got {len(analyzer.params_df)}"


def test_pk_parameter_calculation(simulated_parallel_data):
    """Test that PK parameters are calculated correctly"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Manual calculation for one subject
    subject = simulated_parallel_data["SubjectID"].unique()[0]
    subject_data = simulated_parallel_data.filter(
        pl.col("SubjectID") == subject
    )
    
    # Calculate expected AUC
    times = subject_data["Time (hr)"].to_numpy()
    concs = subject_data["Concentration (ng/mL)"].to_numpy()
    expected_auc = np.trapezoid(concs, times)
    
    # Calculate expected Cmax
    expected_cmax = subject_data["Concentration (ng/mL)"].max()
    
    # Get actual values
    actual_row = analyzer.params_df.filter(
        pl.col("SubjectID") == subject
    )
    
    actual_auc = actual_row["AUC"].item()
    actual_cmax = actual_row["Cmax"].item()
    
    # Check that calculated values are close to expected
    assert np.isclose(actual_auc, expected_auc, rtol=1e-10)
    assert np.isclose(actual_cmax, expected_cmax, rtol=1e-10)


def test_run_anova(simulated_parallel_data):
    """Test that the ANOVA function runs without errors"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Run ANOVA on log-transformed AUC
    result = analyzer.run_anova("log_AUC")
    
    # Check that result is a dictionary
    assert isinstance(result, dict)
    
    # Check that anova_table exists in the result
    assert "anova_table" in result
    
    # Check formula
    assert "formula" in result
    assert "Formulation" in result["formula"]


def test_run_ttest(simulated_parallel_data):
    """Test that the t-test function runs without errors"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Run t-test on log-transformed AUC
    result = analyzer.run_ttest("log_AUC")
    
    # Check that result is a dictionary
    assert isinstance(result, dict)
    
    # Check that t-statistic and p-value exist in the result
    assert "t_statistic" in result
    assert "p_value" in result
    
    # Check that mean values are included
    assert "means" in result
    assert len(result["means"]) == 2  # One for each formulation
    
    # Check that sample sizes are included
    assert "sample_sizes" in result
    assert len(result["sample_sizes"]) == 2  # One for each formulation


def test_point_estimate(simulated_parallel_data):
    """Test that the point estimate function calculates results correctly"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Calculate point estimate for log-transformed AUC
    result = analyzer.calculate_point_estimate("log_AUC")
    
    # Check that result is a dictionary
    assert isinstance(result, dict)
    
    # Check that point_estimate exists in the result
    assert "point_estimate" in result
    
    # Check that confidence intervals exist in the result
    assert "lower_90ci" in result
    assert "upper_90ci" in result
    
    # Check that BE assessment exists in the result
    assert "be_criteria_met" in result
    
    # Point estimate should be a percentage
    assert 50 <= result["point_estimate"] <= 150, f"Point estimate {result['point_estimate']} is outside typical range"


def test_summarize_pk_parameters(simulated_parallel_data):
    """Test that the summary function produces correct results"""
    analyzer = ParallelDesign(
        data=simulated_parallel_data,
        subject_col="SubjectID",
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
    
    # Test that the N values match expected counts
    test_count = len(analyzer.params_df.filter(pl.col("Formulation") == "Test"))
    ref_count = len(analyzer.params_df.filter(pl.col("Formulation") == "Reference"))
    
    # Get N for AUC parameter by formulation
    auc_summary = summary.filter(pl.col("Parameter") == "AUC")
    test_summary_n = auc_summary.filter(pl.col("Formulation") == "Test")["N"].item() if "Test" in auc_summary["Formulation"] else 0
    ref_summary_n = auc_summary.filter(pl.col("Formulation") == "Reference")["N"].item() if "Reference" in auc_summary["Formulation"] else 0
    
    assert test_summary_n == test_count
    assert ref_summary_n == ref_count 