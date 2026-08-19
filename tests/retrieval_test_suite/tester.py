import os
import sys
import time
import subprocess

from src.utils.terminal_utils import TerminalFormatter as clr
from src.utils.terminal_utils import error as err

class RetrievalTester:
    def __init__(self, moulinette_path: str = "./moulinette-ubuntu"):
        self.moulinette_path = moulinette_path
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.docs_dataset = os.path.join(self.project_root,
            "data/datasets/private/AnsweredQuestions/dataset_docs_private.json")
        self.code_dataset = os.path.join(self.project_root,
            "data/datasets/private/AnsweredQuestions/dataset_code_private.json")
        self.docs_unanswered = os.path.join(self.project_root,
            "data/datasets/private/UnansweredQuestions/dataset_docs_private.json")
        self.code_unanswered = os.path.join(self.project_root,
            "data/datasets/private/UnansweredQuestions/dataset_code_private.json")
        self.search_output_dir = os.path.join(self.project_root, "data/output/search_results")

    def run_indexing(self) -> None:
        print(clr.apply("bold", "yellow", ">>> Test: Indexing (limit: 300s)"))
        start = time.time()
        try:
            res = subprocess.run(["uv", "run", "python", "-m", "src", "index",
                            "--max_chunk_size", "2000"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if res.stdout:
                print(res.stdout, end="")
            if res.returncode != 0:
                raise subprocess.CalledProcessError(res.returncode, res.args)
            duration = time.time() - start
            print("\n " + "=" * 50)
            print(clr.apply(None, "yellow", "  Indexing Performance Result:"))
            if duration <= 300:
                print(clr.apply(None, "cyan",
                    f"  PASSED: Indexing completed in {duration:.2f}s (Limit: 300s)"))
            else:
                print(clr.apply(None, "magenta",
                    f"  FAILED: Indexing exceeded the limit. Took {duration:.2f}s (Limit: 300s)"))
            print(" " + "=" * 50 + "\n")
        except subprocess.CalledProcessError as e:
            err(f"Indexing crashed: {e}")

    def run_throughput(self) -> None:
        print(clr.apply("bold", "yellow", ">>> Test: Warm Retrieval Throughput (200 questions in <= 90s)"))
        os.makedirs(self.search_output_dir, exist_ok=True)
        start = time.time()
        try:
            print(clr.apply(None, "cyan", f"  Executing search for Docs..."))
            res1 = subprocess.run(["uv", "run", "python", "-m", "src", "search_dataset", "--dataset_path", self.docs_unanswered, "--k", "10", "--save_directory", self.search_output_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if res1.stdout: print(res1.stdout, end="")
            if res1.returncode != 0: raise subprocess.CalledProcessError(res1.returncode, res1.args)
            
            print(clr.apply(None, "cyan", f"  Executing search for Code..."))
            res2 = subprocess.run(["uv", "run", "python", "-m", "src", "search_dataset", "--dataset_path", self.code_unanswered, "--k", "10", "--save_directory", self.search_output_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if res2.stdout: print(res2.stdout, end="")
            if res2.returncode != 0: raise subprocess.CalledProcessError(res2.returncode, res2.args)
            duration = time.time() - start
            print("\n " + "=" * 50)
            print(clr.apply(None, "yellow", "  Warm Retrieval Throughput Result:"))
            if duration <= 90:
                print(clr.apply(None, "cyan", f"  PASSED: 200 questions retrieved in {duration:.2f}s (Limit: 90s)"))
            else:
                print(clr.apply(None, "magenta", f"  FAILED: Warm retrieval exceeded the limit. Took {duration:.2f}s (Limit: 90s)"))
            print(" " + "=" * 50 + "\n")
        except subprocess.CalledProcessError as e:
            err(f"search_dataset crashed: {e}")

    def _get_results_file(self, keyword: str) -> str | None:
        results_files = []
        # Search the standard output dir, as well as evaluations/retrieval
        search_dirs = [self.search_output_dir, os.path.join(self.project_root, "evaluations", "retrieval")]
        for sdir in search_dirs:
            if not os.path.exists(sdir):
                continue
            for root, _, files in os.walk(sdir):
                for file in files:
                    if keyword in file and file.endswith(".json"):
                        results_files.append(os.path.join(root, file))
        if not results_files:
            return None
        return max(results_files, key=os.path.getmtime)

    def run_docs_recall(self) -> None:
        print(clr.apply("bold", "yellow", ">>> Test: Docs Recall@5 (threshold: 0.80)"))
        res_file = self._get_results_file("docs")
        if not res_file:
            err("No docs search results found.")
            return

        print(f"Evaluating: {res_file}")
        cmd = [self.moulinette_path, "evaluate_student_search_results", res_file, self.docs_dataset, "--k", "10", "--max_context_length", "2000", "--threshold", "0.80"]
        try:
            # We don't check=True so we can inspect output even on failure
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print(res.stdout)
            if res.returncode == 0 and "PASS" in res.stdout:
                print(clr.apply(None, "cyan", "PASSED: Docs Recall@5 meets threshold"))
            else:
                print(clr.apply(None, "magenta", "Docs Recall@5 below threshold or evaluation failed."))
                if res.stderr:
                    print(res.stderr)
        except Exception as e:
            err(f"FAILED: Docs evaluation crashed: {e}")

    def run_code_recall(self) -> None:
        print(clr.apply("bold", "yellow", ">>> Test: Code Recall@5 (threshold: 0.50)"))
        res_file = self._get_results_file("code")
        if not res_file:
            err("No code search results found.")
            return

        print(f"Evaluating: {res_file}")
        cmd = [self.moulinette_path, "evaluate_student_search_results", res_file, self.code_dataset, "--k", "10", "--max_context_length", "2000", "--threshold", "0.50"]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print(res.stdout)
            if res.returncode == 0 and "PASS" in res.stdout:
                print(clr.apply(None, "cyan", "PASSED: Code Recall@5 meets threshold"))
            else:
                print(clr.apply(None, "magenta", "FAILED: Code Recall@5 below threshold or evaluation failed."))
                if res.stderr:
                    print(res.stderr)
        except Exception as e:
            err(f"Code evaluation crashed: {e}")
