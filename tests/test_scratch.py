import pytest
import polars as pl
from bioeq.crossover2x2 import Crossover2x2  # explicit import


@pytest.fixture
def mock_data():
    """Provide mock dataset as pytest fixture."""
    return pl.DataFrame(
        {
            "Subject": [1, 1, 2, 2],
            "Treatment": ["Test", "Reference", "Test", "Reference"],
            "Period": [1, 2, 1, 2],
            "Time": [0, 1, 0, 1],
            "Concentration": [0.0, 5.0, 0.0, 3.0],
        }
    )


def test_crossover_initialization(mock_data):
    """Test Crossover2x2 object initialization."""
    co = Crossover2x2(
        data=mock_data,
        subject_col="Subject",
        seq_col="Treatment",
        period_col="Period",
        time_col="Time",
        conc_col="Concentration",
    )
    assert isinstance(co.data, pl.DataFrame)
    assert co.subject_col == "Subject"
    assert co.seq_col == "Treatment"
    assert co.period_col == "Period"
    assert co.time_col == "Time"
    assert co.conc_col == "Concentration"


def test_calculate_auc(mock_data):
    """Test AUC calculation."""
    co = Crossover2x2(
        data=mock_data,
        subject_col="Subject",
        seq_col="Treatment",
        period_col="Period",
        time_col="Time",
        conc_col="Concentration",
    )
    auc = co.calculate_auc()
    # Add assertions once calculate_auc is implemented
    assert auc is None  # Update when implemented
