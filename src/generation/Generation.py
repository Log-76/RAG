import torch
from ..parsing import MinimalSource
from transformers import AutoModelForCausalLM, AutoTokenizer
from ..utils import error
from ..utils.extract_data import retrieve_data_from_minimal_source


class Generation():
    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

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
                    " context. If the context does not contain the answer"
                    ", say so explicitly. Be concise.")
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
