import pytest
import numpy as np
import polars as pl
from bioeq.validation import ValidationReport, validate_auc_calculation, validate_cmax_calculation


def test_validation_report_creation():
    """Test that a validation report can be created with the correct initial values."""
    report = ValidationReport("Test_Report", "0.1.2")
    
    assert report.report_name == "Test_Report"
    assert report.version == "0.1.2"
    assert len(report.validation_results) == 0
    assert report.summary["total_tests"] == 0
    assert report.summary["passed_tests"] == 0
    assert report.summary["failed_tests"] == 0
    assert report.summary["pass_rate"] == 0.0


def test_validation_report_add_result():
    """Test that results can be added to a validation report."""
    report = ValidationReport("Test_Report", "0.1.2")
    
    # Add a passing test
    report.add_result(
        test_name="Passing Test",
        expected=10.0,
        actual=10.0,
        tolerance=1e-6
    )
    
    # Add a failing test
    report.add_result(
        test_name="Failing Test",
        expected=10.0,
        actual=11.0,
        tolerance=1e-6
    )
    
    assert len(report.validation_results) == 2
    assert report.summary["total_tests"] == 2
    assert report.summary["passed_tests"] == 1
    assert report.summary["failed_tests"] == 1
    assert report.summary["pass_rate"] == 50.0
    
    # Check the first result (passing)
    assert report.validation_results[0]["test_name"] == "Passing Test"
    assert report.validation_results[0]["expected"] == "10.0"
    assert report.validation_results[0]["actual"] == "10.0"
    assert report.validation_results[0]["passed"] == True
    
    # Check the second result (failing)
    assert report.validation_results[1]["test_name"] == "Failing Test"
    assert report.validation_results[1]["expected"] == "10.0"
    assert report.validation_results[1]["actual"] == "11.0"
    assert report.validation_results[1]["passed"] == False


def test_validation_report_zero_expected():
    """Test that validation handles the case where expected value is zero."""
    report = ValidationReport("Test_Report", "0.1.2")
    
    # Test with expected = 0 and actual very close to 0
    report.add_result(
        test_name="Zero Expected Test",
        expected=0.0,
        actual=1e-7,
        tolerance=1e-6
    )
    
    # Test with expected = 0 and actual larger than tolerance
    report.add_result(
        test_name="Zero Expected Failing Test",
        expected=0.0,
        actual=1e-5,
        tolerance=1e-6
    )
    
    assert report.validation_results[0]["passed"] == True
    assert report.validation_results[1]["passed"] == False


def test_auc_validation():
    """Test the AUC validation function with a simple dataset."""
    # Create a validation report
    report = ValidationReport("AUC_Test", "0.1.2")
    
    # Run AUC validation
    validate_auc_calculation(report)
    
    # Check that the test was added to the report
    assert len(report.validation_results) == 1
    assert report.validation_results[0]["test_name"] == "AUC Calculation"
    assert report.validation_results[0]["passed"] == True


def test_cmax_validation():
    """Test the Cmax validation function with a simple dataset."""
    # Create a validation report
    report = ValidationReport("Cmax_Test", "0.1.2")
    
    # Run Cmax validation
    validate_cmax_calculation(report)
    
    # Check that the test was added to the report
    assert len(report.validation_results) == 1
    assert report.validation_results[0]["test_name"] == "Cmax Calculation"
    assert report.validation_results[0]["passed"] == True
    
    # Verify expected value is correct (should be 10.0 from the test dataset)
    expected_cmax = 10.0
    assert float(report.validation_results[0]["expected"]) == expected_cmax 