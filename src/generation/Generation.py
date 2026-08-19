import torch
from typing import Any
from ..parsing import MinimalSource
from ..minimal_search_results import MinimalSearchResults, MinimalAnswer
from transformers import AutoModelForCausalLM, AutoTokenizer
from ..utils import error
from ..utils import retrieve_data_from_minimal_source


class Generation():
    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self.model_name: str = model_name
        self.tokenizer: Any | None = None
        self.model: Any = None

    def load_model(self) -> None:
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32
                    )
            self.model.eval()
        except Exception as e:
            error(f"Failed to load model {self.model_name}: {e}")
            exit()

    def build_prompt(self, data_to_extract: list[MinimalSource],
                     question: str) -> list[dict[str, str]]:
        try:
            system_context = (
                    "You are a technical assistant answering questions"
                    " about a codebase. Answer ONLY using the provided"
                    " context. Do not describe unrelated usage details."
                    " If the context does not contain the answer"
                    ", say so explicitly. Be concise. "
                    "Only answer the question.")
            system_block = []
            for x in data_to_extract:
                text = retrieve_data_from_minimal_source(x)
                if not text:
                    continue
                system_block.append(f"[Source: {x.file_path}]\n{text}")
            context = ("\n\n".join(system_block)
                       if system_block
                       else "(no relevant context found)"
                       )
            user_context = f"Context:\n{context}\n\nQuestion: {question}"
            return [
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_context}
                ]
        except Exception as e:
            error(f"Error while building prompt {question}: {e}")
            raise

    def generate_answer(
        self,
        search_result: MinimalSearchResults
    ) -> MinimalAnswer:
        try:
            if self.model is None or self.tokenizer is None:
                self.load_model()
            messages = self.build_prompt(
                search_result.retrieved_sources,
                search_result.question
            )
            if self.tokenizer is None:
                raise RuntimeError("Le tokenizer doit être "
                                   "chargé avant de générer.")
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False
            )
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1024,
                    do_sample=False,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
            answer_text = self.tokenizer.decode(
                generated_tokens,
                skip_special_tokens=True
            ).strip()
            return MinimalAnswer(
                question_id=search_result.question_id,
                question=search_result.question,
                retrieved_sources=search_result.retrieved_sources,
                answer=answer_text
            )
        except Exception as e:
            error(f"ERROR: {e}")
            raise e
