*This project has been created as part of the 42 curriculum by ele-roux.*

# RAG against the machine

## Description

**RAG against the machine** is a Retrieval-Augmented Generation (RAG) system that
answers natural-language questions about the [vLLM](https://github.com/vllm-project/vllm)
codebase.

Instead of relying on a language model's frozen training knowledge, the system:

1. **Indexes** the vLLM repository (source code and documentation) into a searchable
   lexical index.
2. **Retrieves** the most relevant snippets for a given question.
3. **Augments** a prompt with those snippets.
4. **Generates** a grounded, natural-language answer using `Qwen/Qwen3-0.6B`.

Retrieval quality is measured with **recall@k**, comparing the source locations the
system retrieves against a ground-truth dataset of question/answer pairs.

## Instructions

### Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) as the package/project manager
- The vLLM source tree available under `data/raw/`
- ~a few GB of free disk space (model weights + dependencies)

### Installation

```bash
make install
# equivalent to: uv sync
```

### Running the pipeline

```bash
# 1. Build the index (chunks the corpus, persists it under data/processed/)
uv run python -m src index --max_chunk_size 2000

# 2. Search a single question
uv run python -m src search "How to configure the OpenAI server?" --k 5

# 3. Search a whole dataset of questions
uv run python -m src search_dataset \
  --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json \
  --k 10 \
  --save_directory data/output/search_results/UnansweredQuestions

# 4. Generate a grounded answer for a single question
uv run python -m src answer "How to configure the OpenAI server?" --k 5

# 5. Generate answers for a whole dataset of search results
uv run python -m src answer_dataset \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --save_directory data/output/search_results_and_answer/UnansweredQuestions

# 6. Evaluate recall@k against a ground-truth dataset (local iteration only —
#    the official score during defense is computed by the moulinette)
uv run python -m src evaluate \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json
```

### Makefile targets

| Target        | Description                                      |
|---------------|---------------------------------------------------|
| `make install`| Install dependencies via `uv sync`                |
| `make run`    | Run the CLI                                        |
| `make debug`  | Run the CLI under `pdb`                            |
| `make clean`  | Remove caches (`__pycache__`, `.mypy_cache`, ...)  |
| `make lint`   | Run `flake8` and `mypy`                            |

## System Architecture

The pipeline is split into independent stages, each with its own responsibility:

```
data/raw/ (vLLM repo)
      │
      ▼
┌─────────────┐     ┌────────────┐     ┌──────────────┐     ┌────────────────┐
│  Chunking   │ ──▶ │  Indexing  │ ──▶ │  Retrieving  │ ──▶ │   Generation    │
│ (src/parsing│     │  (BM25 +   │     │ (top-k query │     │ (Qwen/Qwen3-0.6B│
│  /indexing) │     │  tokenizer)│     │   search)     │     │  + prompt)      │
└─────────────┘     └────────────┘     └──────────────┘     └────────────────┘
      │                    │                    │                     │
      ▼                    ▼                    ▼                     ▼
 chunked sources     data/processed/     MinimalSearchResults    MinimalAnswer
                      (persisted BM25       (JSON output)          (JSON output)
                          index)
```

- **`src/indexing/`** — reads `data/raw/`, chunks every file, builds and persists a
  BM25 index under `data/processed/`.
- **`src/retrieving/`** — loads the persisted index, tokenizes a query, and returns
  the top-k matching `MinimalSource` locations.
- **`src/generation/`** — takes the retrieved sources, builds a prompt within the
  model's token budget, and calls `Qwen/Qwen3-0.6B` to produce a grounded answer.
- **`src/parsing/`** — the pydantic data models shared between every stage
  (`MinimalSource`, `UnansweredQuestion`, `AnsweredQuestion`, `RagDataset`,
  `MinimalSearchResults`, `MinimalAnswer`, `StudentSearchResults`,
  `StudentSearchResultsAndAnswer`).
- **`src/CLI/`** — the Python Fire command-line entry point wiring all stages
  together (`index`, `search`, `search_dataset`, `answer`, `answer_dataset`,
  `evaluate`).

## Chunking Strategy

A Python file and a Markdown page do not break apart the same way, so two distinct
chunking strategies are implemented:

- **Python code chunking**: uses `RecursiveCharacterTextSplitter.from_language`
  (from `langchain-text-splitters`) with `Language.PYTHON`, so splits respect
  function/class boundaries instead of cutting in the middle of a definition.
- **Markdown / text chunking**: uses a plain `RecursiveCharacterTextSplitter`,
  splitting on paragraph and sentence boundaries.

Chunk size is configurable via `--max_chunk_size` (default: 2000 characters), which
matches the moulinette's `max_context_length` — chunks are never allowed to exceed
this size, since an over-long source invalidates the whole output.

## Retrieval Method

Retrieval uses **BM25** (`rank_bm25`) as the lexical ranking method. At indexing
time, every chunk is tokenized (word-level tokens, identifier splitting for
`snake_case`/`camelCase`, and light suffix-stemming), and a `BM25Okapi` index is
built over the tokenized corpus.

At query time, the question is tokenized the exact same way, scored against the
index, and the top-k `MinimalSource` locations (file path + character range) are
returned.

## Performance Analysis

_Fill in with your own measured numbers before submitting, e.g.:_

| Metric                        | Result       | Requirement           |
|--------------------------------|--------------|------------------------|
| Indexing time (full corpus)    | 11s       | ≤ 5 minutes            |
| Retrieval throughput (200 q)   | 17s       | ≤ 90 seconds           |
| Recall@5 — docs questions      | 80%       | ≥ 80%                  |
| Recall@5 — code questions      | 54%       | ≥ 50%                  |

Run `make lint` and the local `evaluate` command (or the provided moulinette) to
reproduce these numbers.

## Design Decisions

- **BM25 over TF-IDF**: chosen for its length-normalization and saturation
  properties, which behave more predictably across the very different lengths of
  code chunks vs. documentation chunks.
- **Shared tokenizer**: indexing and querying both go through the same tokenizer
  function, so the corpus vocabulary and the query vocabulary are always built
  identically — this avoids silent recall loss from vocabulary mismatch.
- **Pydantic models as the contract between stages**: every stage exchanges data
  exclusively through the models defined in `src/parsing/`, so each stage can be
  developed, tested, and swapped independently.
- **Graceful degradation per question**: a single malformed or unanswerable
  question in a dataset never aborts the whole batch — it is logged and given an
  empty result instead, so `search_dataset`/`answer_dataset` always produce a
  complete output file.

## Challenges Faced

- **Vocabulary mismatch between indexing and querying**: an early version
  tokenized the corpus and the queries differently (subword-splitting and
  stemming were only applied at indexing time), silently reducing recall. This
  was fixed by extracting the tokenizer into a single shared function used
  identically by both stages.
- **Balancing chunk size against retrieval precision**: larger chunks improve
  recall (more context per chunk) but risk exceeding the moulinette's
  `max_context_length` and diluting relevance; `--max_chunk_size` was kept
  configurable to let this trade-off be tuned per dataset.
- **Batch robustness**: a single failing question (empty query, no match found)
  used to raise an exception that aborted the entire `search_dataset` run. The
  per-question retrieval call is now isolated so one bad question degrades
  gracefully instead of losing the whole batch.

## Example Usage

```bash
$ uv run python -m src search "How to configure the OpenAI server?" --k 5
data/raw/vllm-0.10.1/docs/serving/openai_compatible_server.md [9867:10100]
data/raw/vllm-0.10.1/vllm/entrypoints/openai/api_server.py [267:400]
...

$ uv run python -m src answer "How to configure the OpenAI server?" --k 5
{
  "question_id": "...",
  "question": "How to configure the OpenAI server?",
  "retrieved_sources": [...],
  "answer": "To configure the OpenAI compatible server in vLLM..."
}
```

## Resources

- [vLLM documentation](https://docs.vllm.ai/)
- [BM25 — Okapi BM25 ranking function](https://en.wikipedia.org/wiki/Okapi_BM25)
- [rank_bm25 library](https://github.com/dorianbrown/rank_bm25)
- [LangChain text splitters](https://python.langchain.com/docs/how_to/recursive_text_splitter/)
- [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [Python Fire documentation](https://github.com/google/python-fire)

### AI usage

AI assistance was used during this project for:
- Reviewing the implementation against the subject's requirements and identifying
  gaps (missing CLI command, README structure, edge-case handling).
- Diagnosing and fixing a bugs
- Explaining documentation
- Writing documentation

All AI-assisted changes were reviewed, understood, and adapted manually before
being integrated into the project.
