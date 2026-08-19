import os
import random
import subprocess
import sys
import re
import json

from src.utils.terminal_utils import TerminalFormatter as clr
from src.utils.terminal_utils import error as err

class AnswerTester:
    def __init__(self, moulinette_path: str = "./moulinette-ubuntu"):
        self.moulinette_path = moulinette_path
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.dataset_path = os.path.join(self.project_root, "data/datasets/private/AnsweredQuestions/dataset_docs_private.json")
        self.results_dir = os.path.join(self.project_root, "data/output/search_results")
        
    def get_latest_results(self):
        results_files = []
        for root, _, files in os.walk(self.results_dir):
            for file in files:
                if "docs" in file and "private" in file and file.endswith(".json"):
                    results_files.append(os.path.join(root, file))
        if not results_files:
            eval_dir = os.path.join(self.project_root, "evaluations/retrieval")
            if os.path.exists(eval_dir):
                for root, _, files in os.walk(eval_dir):
                    for file in files:
                        if "docs" in file and "private" in file and file.endswith(".json"):
                            results_files.append(os.path.join(root, file))
        
        if not results_files:
            return None
        return max(results_files, key=os.path.getmtime)

    def run(self, n_questions: str = "3", eval_dir: str = None) -> None:
        print(clr.apply(None, "yellow", "--- Answer Quality Examination ---"))
        
        questions_path = os.path.join(os.path.dirname(__file__), "valid_questions.json")
        try:
            with open(questions_path, "r", encoding="utf-8") as f:
                questions = json.load(f)
        except Exception as e:
            err(f"Failed to load valid questions: {e}")
            return
            
        if not questions:
            err("No valid questions found in JSON file.")
            return
            
        print(f"Found {len(questions)} valid questions.")
        
        if n_questions == 'a':
            selected = list(questions.values())
        else:
            try:
                n = int(n_questions)
                max_key = len(questions)
                n = min(n, max_key)
                
                chosen_keys = set()
                while len(chosen_keys) < n:
                    chosen_keys.add(str(random.randint(1, max_key)))
                    
                selected = [questions[k] for k in chosen_keys]
            except ValueError:
                err("Invalid parameter for n_questions. Expected an integer or 'a'.")
                return
                
        for i, q in enumerate(selected, 1):
            res = subprocess.run(["uv", "run", "python", "-m", "src", "answer", q, "--k", "10"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            answer_text = ""
            if res.stdout:
                match = re.search(r'Answer:\n(.*?)==================================================', res.stdout, re.DOTALL)
                if match:
                    answer_text = match.group(1).strip()
                else:
                    answer_text = res.stdout.strip()
                    
            print(clr.apply(None, "yellow", f"\n--- Answer {i}/{len(selected)} ---"))
            print("==================================================")
            print(f"Question: {q}")
            print("--------------------------------------------------")
            print("Answer:\n" + answer_text)
            print("==================================================")
            
        print(clr.apply(None, "yellow", "\nReview the answers above. Pass criteria: 2/3 satisfactory."))
