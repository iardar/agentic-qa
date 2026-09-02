from pathlib import Path
from typing import Protocol

from agentic_qa.models import TestExecutionResult


class TestRunner(Protocol):
    def run(
        self,
        test_path: Path,
    ) -> TestExecutionResult:
        """Execute a generated pytest test."""
        ...
