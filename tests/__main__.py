"""
Main entry point for the RAG test suite UI.
"""

import subprocess
import os
import sys
from datetime import datetime

from src.utils.terminal_utils import TerminalFormatter as clr
from src.utils.terminal_utils import error as err

class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            if hasattr(f, 'write'):
                f.write(obj)
                f.flush()
    def flush(self):
        for f in self.files:
            if hasattr(f, 'flush'):
                f.flush()
    def isatty(self):
        for f in self.files:
            if hasattr(f, 'isatty'):
                return f.isatty()
        return False

from tests.retrieval_test_suite.tester import RetrievalTester
from tests.answer_test_suite.tester import AnswerTester
from tests.edgy_test_suite.tester import EdgyTester

class RAGtester:

    def __init__(self) -> None:
        """Init test suite components."""
        self.retrieval_tester = RetrievalTester()
        self.answer_tester = AnswerTester()
        self.edgy_tester = EdgyTester()

    def run(self) -> None:
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.eval_dir = os.path.join(self.project_root, "evaluations", self.timestamp)
        os.makedirs(self.eval_dir, exist_ok=True)
        log_path = os.path.join(self.eval_dir, "result.log")

        f = open(log_path, "w", encoding="utf-8")
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, f)  # type: ignore

        try:
            print('\n' + ' ' + '=' * 60)
            print(clr.apply('bold', 'white', '  RAG against the machine: Test Suite'))
            print(' ' + '=' * 60)

            options = {
                1: ['Test Indexing Performance (limit: 300s)', self.retrieval_tester.run_indexing],
                2: ['Test Warm Retrieval Throughput (200 questions in <= 90s)', self.retrieval_tester.run_throughput],
                3: ['Test Docs Retrieval (Recall@5 >= 0.80)', self.retrieval_tester.run_docs_recall],
                4: ['Test Code Retrieval (Recall@5 >= 0.50)', self.retrieval_tester.run_code_recall],
                5: ['Test Edge Cases (Pytest)', self.edgy_tester.run],
                6: ['Test Answer Quality (Interactive)', self.run_answer_tester],
            }

            print(clr.apply('bold', 'white', f'  {"n.":<3}Description'))
            print(' ' + '-' * 60)

            for k, v in options.items():
                print(f'  {k:<3}{v[0]}')

            print(' ' + '-' * 60)
            raw = input(clr.apply('bold', 'white', '  Pick an option: '))
            print()

            try:
                choice = int(raw.strip())
                print()

                if choice in options:
                    target_method = options[choice][1]
                    target_method()
                else:
                     err(' Invalid option.\n')
                print()

            except ValueError:
                err(' Please enter a valid number.\n')
            except subprocess.CalledProcessError as e:
                err(f' The pipeline crashed or returned an error code: {e}\n')
            except Exception as e:
                err(f' An unexpected error occurred: {e}\n')

        finally:
            print(f"\nResults saved to: {log_path}")
            sys.stdout = original_stdout
            f.close()

    def run_answer_tester(self) -> None:
        n_str = input(clr.apply('bold', 'white', '  How many questions to test? (Enter integer or "a" for all): ')).strip()
        self.answer_tester.run(n_str, eval_dir=getattr(self, 'eval_dir', None))


if __name__ == "__main__":
    tester = RAGtester()
    tester.run()
