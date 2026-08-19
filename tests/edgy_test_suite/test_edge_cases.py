import subprocess
import pytest
import sys

def run_command(args: list[str]) -> str:
    """Helper to run a CLI command and return stderr. We allow it to fail since these are edge cases."""
    result = subprocess.run(["uv", "run", "python", "-m", "src"] + args, capture_output=True, text=True)
    return result.stderr

def test_empty_query():
    stderr = run_command(["search", "", "--k", "10"])
    assert "Traceback" not in stderr, f"Traceback found in empty query test:\n{stderr}"

def test_gibberish_query():
    stderr = run_command(["search", "asdfghjkl zxcvbnm qwertyuiop", "--k", "10"])
    assert "Traceback" not in stderr, f"Traceback found in gibberish query test:\n{stderr}"

def test_k_zero():
    stderr = run_command(["answer", "What is vLLM?", "--k", "0"])
    assert "Traceback" not in stderr, f"Traceback found in k=0 test:\n{stderr}"

def test_invalid_dataset():
    stderr = run_command(["search_dataset", "--dataset_path", "/nonexistent/dataset.json", "--k", "10"])
    assert "Traceback" not in stderr, f"Traceback found in invalid dataset test:\n{stderr}"


def test_max_chunk_size_exceeded():
    stderr = run_command(["index", "--max_chunk_size", "2001"])
    assert "Traceback" not in stderr, f"Traceback found in chunk size test:\n{stderr}"
