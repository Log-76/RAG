from pathlib import Path
from tqdm import tqdm
from ..minimal_search_results import MinimalAnswer
from ..student_search import StudentSearchResults
from ..student_search import StudentSearchResultsAndAnswer
from ..utils import error
from .Generation import Generation


class AnswerOrchestrator():
    """
    Orchestrates answer generation over a whole dataset of search
    results: load -> generate answers -> persist.
    """
    def __init__(self, generation: Generation) -> None:
        self.generation: Generation = generation

    def load_search_results(
        self,
        path: Path
    ) -> StudentSearchResults | None:
        """
        Loads and validates a StudentSearchResults JSON file.
        Returns None (and logs the error) on any failure, so the
        caller can fail gracefully instead of crashing.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return StudentSearchResults.model_validate_json(f.read())
        except Exception as e:
            error(f"Failed to load search results from {path}: {e}")
            return None

    def generate_all_answers(
        self,
        search_results: StudentSearchResults
    ) -> list[MinimalAnswer]:
        """
        Generates an answer for every question in search_results.
        A question that fails to generate is still included in the
        output, with an explicit failure message as its answer, so
        the output count always matches the input count.
        """
        answers: list[MinimalAnswer] = []
        for result in tqdm(
            search_results.search_results,
            desc="Generating answers",
            unit="question"
        ):
            try:
                answers.append(self.generation.generate_answer(result))
            except Exception as e:
                error(
                    f"Failed to generate answer for "
                    f"{result.question_id}: {e}"
                )
                answers.append(MinimalAnswer(
                    question_id=result.question_id,
                    question=result.question,
                    retrieved_sources=result.retrieved_sources,
                    answer=f"Generation failed: {e}"
                ))
        return answers

    def run(
        self,
        student_search_results_path: Path,
        save_directory: Path
    ) -> None:
        """
        Runs the full answer_dataset pipeline: load search results,
        generate an answer for every question, save the result
        under save_directory using the same file name as the input.
        """
        search_results = self.load_search_results(
            student_search_results_path
        )
        if search_results is None:
            return
        answers = self.generate_all_answers(search_results)
        output = StudentSearchResultsAndAnswer(
            search_results=answers,
            k=search_results.k
        )

        try:
            save_directory.mkdir(parents=True, exist_ok=True)
            output_path = save_directory / student_search_results_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output.model_dump_json(indent=2))
            print(
                f"Saved student_search_results_and_answer to {output_path}"
            )
        except Exception as e:
            error(f"Failed to save answers to {save_directory}: {e}")
