import pytest
import polars as pl
from bioeq import BioEq  # Assuming the class is in a file named bioeq.py


@pytest.fixture
def mock_data():
    """
    Provide a mock dataset as a pytest fixture.
    """
    return pl.DataFrame({
        "Subject": [1, 1, 2, 2],
        "Treatment": ["Test", "Reference", "Test", "Reference"],
        "Period": [1, 2, 1, 2],
        "Time": [0, 1, 0, 1],
        "Concentration": [0.0, 5.0, 0.0, 3.0]
    })


@pytest.fixture
def bioeq(mock_data):
    """
    Provide a BioEq object initialized with the mock dataset.
    """
    # Simulate loading the dataset by directly assigning it
    bioeq = BioEq(
        subject_col="Subject",
        seq_col="Treatment",
        period_col="Period",
        time_col="Time",
        conc_col="Concentration"
    )
    bioeq.simdata1 = mock_data  # Directly set the dataset
    return bioeq


def test_initialization(bioeq):
    """
    Test that the BioEq object initializes with the correct columns.
    """
    assert bioeq.subject_col == "Subject"
    assert bioeq.seq_col == "Treatment"
    assert bioeq.period_col == "Period"
    assert bioeq.time_col == "Time"
    assert bioeq.conc_col == "Concentration"
    assert isinstance(bioeq.simdata1, pl.DataFrame)


def test_missing_columns():
    """
    Test that compute_auc raises a ValueError for missing required columns.
    """
    # Create a dataset missing the 'Time' column
    data = pl.DataFrame({
        "Subject": [1, 2],
        "Treatment": ["Test", "Reference"],
        "Concentration": [5.0, 3.0]
    })
    bioeq = BioEq(
        subject_col="Subject",
        seq_col="Treatment",
        period_col="Period",
        time_col="Time",
        conc_col="Concentration"
    )
    bioeq.simdata1 = data  # Directly set the incomplete dataset

    with pytest.raises(ValueError, match="Dataset is missing required columns:"):
        bioeq.compute_auc()


def test_data_integrity(bioeq):
    """
    Test that the loaded dataset retains its structure.
    """
    assert "Subject" in bioeq.simdata1.columns
    assert "Time" in bioeq.simdata1.columns
    assert "Concentration" in bioeq.simdata1.columns
    assert bioeq.simdata1.shape == (4, 5)


def test_validate_colvals_placeholder(bioeq):
    """
    Test that _validate_colvals exists and can be called without error.
    """
    try:
        bioeq._validate_colvals()
    except Exception as e:
        pytest.fail(f"_validate_colvals raised an unexpected exception: {e}")
