import pytest
from src.utils.logging import setup_logging

def test_logging_setup(caplog):
    setup_logging()
    with caplog.at_level("INFO"):
        print("Test log message")
    assert "Test log message" in caplog.text

# Additional utility tests can be added here as needed.