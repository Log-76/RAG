import pytest
import os

class EdgyTester:
    def run(self) -> None:
        """Run the pytest edge cases test suite."""
        test_file = os.path.join(os.path.dirname(__file__), "test_edge_cases.py")
        pytest.main(["-v", test_file])
