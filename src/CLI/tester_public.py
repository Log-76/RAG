import os
import time
import subprocess
from src.utils.terminal_utils import TerminalFormatter as clr
from src.utils.terminal_utils import error as err


class RetrievalTester:
    """Automates performance and quality testing for the RAG system.

    Handles benchmarking indexing speed, warm retrieval throughput,
    and evaluating
    Recall metrics against ground-truth public datasets via an external binary.

    Attributes:
        moulinette_path (str): Path to the evaluation binary.
        project_root (str): Root directory of the project.
        docs_dataset (str): Path to the answered documentation dataset.
        code_dataset (str): Path to the answered code dataset.
        docs_unanswered (str): Path to the unanswered documentation dataset.
        code_unanswered (str): Path to the unanswered code dataset.
        search_output_dir (str): Directory where search outputs are saved.
    """
    def __init__(self, moulinette_path: str = "./moulinette-ubuntu"):
        """Initializes dataset paths and test environment configurations.

        Args:
            moulinette_path: Relative or absolute path
            to the evaluation binary.
        """
        self.moulinette_path = moulinette_path
        temp = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.project_root = temp
        self.docs_dataset = os.path.join(self.project_root,
                                         "data/datasets/public/"
                                         "AnsweredQuestions/"
                                         "dataset_docs_public.json")
        self.code_dataset = os.path.join(self.project_root,
                                         "data/datasets/public/"
                                         "AnsweredQuestions/"
                                         "dataset_code_public.json")
        self.docs_unanswered = os.path.join(self.project_root,
                                            "data/datasets/public/"
                                            "UnansweredQuestions/"
                                            "dataset_docs_public.json")
        self.code_unanswered = os.path.join(self.project_root,
                                            "data/datasets/public/"
                                            "UnansweredQuestions/"
                                            "dataset_code_public.json")
        self.search_output_dir = os.path.join(self.project_root,
                                              "data/output/search_results")

    def run_indexing(self) -> None:
        """Measures corpus indexing performance against
        a 300-second threshold.

        Executes the indexing CLI command via a subprocess
        and validates whether
        the process completes within the required time limit.
        """
        print(clr.apply("bold", "yellow", ">>> Test: Indexing (limit: 300s)"))
        start = time.time()
        try:
            res = subprocess.run(["uv", "run", "python", "-m",
                                  "src", "index",
                                  "--max_chunk_size", "2000"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True)
            if res.stdout:
                print(res.stdout, end="")
            if res.returncode != 0:
                raise subprocess.CalledProcessError(res.returncode, res.args)
            duration = time.time() - start
            print("\n " + "=" * 50)
            print(clr.apply(None, "yellow", "  Indexing Performance Result:"))
            if duration <= 300:
                print(clr.apply(None, "cyan",
                                "  PASSED: Indexing completed"
                                f"in {duration:.2f}s (Limit: 300s)"))
            else:
                print(clr.apply(None, "magenta",
                                "  FAILED: Indexing exceeded the limit."
                                f"Took {duration:.2f}s (Limit: 300s)"))
            print(" " + "=" * 50 + "\n")
        except subprocess.CalledProcessError as e:
            err(f"Indexing crashed: {e}")

    def run_throughput(self) -> None:
        """Benchmarks batch retrieval throughput against a 90-second limit.

        Executes search retrieval for 200 questions across
        documentation and code
        unanswered datasets, asserting total processing time
        stays under target.
        """
        print(clr.apply("bold", "yellow", ">>> Test: Warm Retrieval"
                        "hroughput (200 questions in <= 90s)"))
        os.makedirs(self.search_output_dir, exist_ok=True)
        start = time.time()
        try:
            print(clr.apply(None, "cyan", "  Executing search for Docs..."))
            res1 = subprocess.run(["uv", "run", "python", "-m",
                                   "src", "search_dataset",
                                   "--dataset_path",
                                   self.docs_unanswered,
                                   "--k", "10", "--save_directory",
                                   self.search_output_dir],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, text=True)
            if res1.stdout:
                print(res1.stdout, end="")
            if res1.returncode != 0:
                raise subprocess.CalledProcessError(res1.returncode, res1.args)
            print(clr.apply(None, "cyan", "  Executing search for Code..."))
            res2 = subprocess.run(["uv", "run", "python",
                                   "-m", "src", "search_dataset",
                                   "--dataset_path", self.code_unanswered,
                                   "--k", "10", "--save_directory",
                                   self.search_output_dir],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, text=True)
            if res2.stdout:
                print(res2.stdout, end="")
            if res2.returncode != 0:
                raise subprocess.CalledProcessError(res2.returncode, res2.args)
            duration = time.time() - start
            print("\n " + "=" * 50)
            print(clr.apply(None, "yellow",
                            "  Warm Retrieval Throughput Result:"))
            if duration <= 90:
                print(clr.apply(None, "cyan",
                                "  PASSED: 200 questions retrieved"
                                f"in {duration:.2f}s (Limit: 90s)"))
            else:
                print(clr.apply(None, "magenta",
                                "  FAILED: Warm retrieval exceeded "
                                f"the limit. Took {duration:.2f}s "
                                "(Limit: 90s)"))
            print(" " + "=" * 50 + "\n")
        except subprocess.CalledProcessError as e:
            err(f"search_dataset crashed: {e}")

    def _get_results_file(self, dataset_path: str) -> str | None:
        """Locate the results file that corresponds exactly to dataset_path.

        `search_dataset` always writes its output using the same file
        name as the input dataset (see CLI.search_dataset:
        `output_path = process_save_dir / processed_dataset_path.name`).
        So instead of guessing via a loose keyword match (which matches
        both "dataset_code_public.json" AND "dataset_code_private.json")
        combined with "most recently modified" (which can silently pick
        up a stale or private run), we look for the *exact* expected
        file name. This guarantees we only ever evaluate the results
        that actually correspond to the public dataset being tested.
        """
        expected_name = os.path.basename(dataset_path)
        search_dirs = [self.search_output_dir,
                       os.path.join(self.project_root,
                                    "evaluations", "retrieval")]
        for sdir in search_dirs:
            if not os.path.exists(sdir):
                continue
            for root, _, files in os.walk(sdir):
                if expected_name in files:
                    return os.path.join(root, expected_name)
        return None

    def run_docs_recall(self) -> None:
        print(clr.apply("bold", "yellow",
                        ">>> Test: Docs Recall@5 (threshold: 0.80)"))
        res_file = self._get_results_file(self.docs_unanswered)
        if not res_file:
            err("No docs search results found.")
            return

        print(f"Evaluating: {res_file}")
        cmd = [self.moulinette_path, "evaluate_student_search_results",
               res_file, self.docs_dataset, "--k", "10",
               "--max_context_length", "2000", "--threshold", "0.80"]
        try:
            # We don't check=True so we can inspect output even on failure
            res = subprocess.run(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True)
            print(res.stdout)
            if res.returncode == 0 and "PASS" in res.stdout:
                print(clr.apply(None, "cyan",
                                "PASSED: Docs Recall@5 meets threshold"))
            else:
                print(clr.apply(None, "magenta",
                                "Docs Recall@5 below threshold "
                                "or evaluation failed."))
                if res.stderr:
                    print(res.stderr)
        except Exception as e:
            err(f"FAILED: Docs evaluation crashed: {e}")

    def run_code_recall(self) -> None:
        """Evaluates Recall@5 metric for documentation queries
        (threshold: 0.80).

        Runs the external evaluation binary comparing
        student search results against
        the ground-truth answered documentation dataset.
        """
        print(clr.apply("bold", "yellow", ">>> Test: "
                                          "Code Recall@5 (threshold: 0.50)"))
        res_file = self._get_results_file(self.code_unanswered)
        if not res_file:
            err("No code search results found.")
            return

        print(f"Evaluating: {res_file}")
        cmd = [self.moulinette_path,
               "evaluate_student_search_results",
               res_file, self.code_dataset, "--k", "10",
               "--max_context_length",
               "2000", "--threshold", "0.50"]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True)
            print(res.stdout)
            if res.returncode == 0 and "PASS" in res.stdout:
                print(clr.apply(None, "cyan", "PASSED: Code Recall@5 "
                                              "meets threshold"))
            else:
                print(clr.apply(None, "magenta", "FAILED: Code Recall@5"
                                                 "below threshold or "
                                                 "evaluation failed."))
                if res.stderr:
                    print(res.stderr)
        except Exception as e:
            err(f"Code evaluation crashed: {e}")
