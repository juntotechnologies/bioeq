import pytest
import polars as pl
from bioeq import BioEq, Crossover2x2  # Assuming the class is in a file named bioeq.py

# @pytest.fixture
# def mock_data():
#     """
#     Provide a mock dataset as a pytest fixture.
#     """
#     return pl.DataFrame(
#         {
#             "Subject": [1, 1, 2, 2],
#             "Treatment": ["Test", "Reference", "Test", "Reference"],
#             "Period": [1, 2, 1, 2],
#             "Time": [0, 1, 0, 1],
#             "Concentration": [0.0, 5.0, 0.0, 3.0],
#         }
#     )


# @pytest.fixture
# def bioeq1(mock_data):
#     """
#     Provide a BioEq object initialized with the mock dataset.
#     """
#     # Simulate loading the dataset by directly assigning it
#     bioeq1 = BioEq(
#         subject_col="Subject",
#         seq_col="Treatment",
#         period_col="Period",
#         time_col="Time",
#         conc_col="Concentration",
#     )

#     return bioeq1


# @pytest.fixture
# def bioeq2(mock_data):
#     """
#     Provide a BioEq object initialized with the mock dataset.
#     """
#     # Simulate loading the dataset by directly assigning it
#     bioeq2 = BioEq(
#         # subject_col="Subject", # comment this out
#         seq_col="Treatment",
#         period_col="Period",
#         time_col="Time",
#         conc_col="Concentration",
#     )

#     return bioeq2


# def test_initialization(bioeq):
#     """
#     Test that the BioEq object initializes with the correct columns.
#     """
#     assert bioeq.subject_col == "Subject"
#     assert bioeq.seq_col == "Treatment"
#     assert bioeq.period_col == "Period"
#     assert bioeq.time_col == "Time"
#     assert bioeq.conc_col == "Concentration"
#     assert isinstance(bioeq.simdata1, pl.DataFrame)

#     print(bioeq.subject_col)

# def test_missing_columns():
#     """
#     Test that compute_auc raises a ValueError for missing required columns.
#     """
#     # Create a dataset missing the 'Time' column

#     bioeq = BioEq(
#         subject_col="Subject",
#         seq_col="Treatment",
#         period_col="Period",
#         time_col="Time",
#         conc_col="Concentration",
#     )
#     print(bioeq.simdata1)


#     # with pytest.raises(ValueError, match="Dataset is missing required columns:"):
#     #     bioeq.compute_auc()


# def test_data_integrity(bioeq):
#     """
#     Test that the loaded dataset retains its structure.
#     """
#     assert "Subject" in bioeq.simdata1.columns
#     assert "Time" in bioeq.simdata1.columns
#     assert "Concentration" in bioeq.simdata1.columns
#     assert bioeq.simdata1.shape == (4, 5)

@pytest.fixture
def pull_simdata():
    simdata = pl.read_csv(
        source="https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    )
    return simdata

# AHA! Can put the fixture without the parentheses as a parameter and THEN I can use it in the test :)!!
def test_basics(pull_simdata):

    # Crossover2x2()
    # BioEq(conc_col = 'Conc', period_col = 'Period', seq_col = 'Sequence', subject_col='Subject', time_col='Time')
    print(pull_simdata)

    # co_class = Crossover2x2(
    #     data=simdata,
    #     subject_col="SubjectID",
    #     seq_col="Sequence",
    #     period_col="Period",
    #     time_col="Time (hr)",
    #     conc_col="Concentration (ng/mL)",
    # )

    # print(co_class)

    pass

def test_calculate_auc():
    # Crossover2x2(
    # )
    pass
