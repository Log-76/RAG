# ============================================================
#  VARIABLES
# ============================================================

USER         ?= $(shell whoami)
VENV         := /tmp/$(USER)_venv
UV_CACHE_DIR := /tmp/$(USER)_uv_cache
PYTHON_VENV  := $(VENV)/bin/python
UV           := UV_CACHE_DIR=$(UV_CACHE_DIR) $(VENV)/bin/uv
LLM	 := llm_sdk
PYTHON   := $(UV) run python

PYTEST   := $(UV) run pytest
TESTDIR	 := tests

MYPY     := $(UV) run mypy
FLAKE8   := $(UV) run flake8
EXCLUDE	 := --extend-exclude=$(VENV),$(TESTDIR),$(LLM),moulinette

FUNC_DEF ?= data/input/functions_definition.json
INPUT_F	 ?= data/input/function_calling_tests.json
OUTPUT_F ?= data/output/function_calls.json

ALT	?= HuggingFaceTB/SmolLM-135M-Instruct
HF_OFF	:= HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1

# ------------------------------------------------------------
#  Ansi colors
# ------------------------------------------------------------

RESET	:= \033[0m
GRAY	:= \033[1;90m
RED	:= \033[1;91m
GREEN	:= \033[1;92m
YELLOW	:= \033[1;93m
BLUE	:= \033[1;94m
MAGENTA	:= \033[1;95m
CYAN	:= \033[1;96m
WHITE	:= \033[1;97m

# ------------------------------------------------------------
#  Additional commands
# ------------------------------------------------------------

ECHO	:= echo
FIND	:= /bin/find
IGNORE	:= 2>/dev/null || true
MV	:= /bin/mv
RM	:= /bin/rm -rf

# ============================================================
#  RULES
# ============================================================

.PHONY: install run debug clean lint lint-strict \
       	help test campus-init clean-venv visual run-alt

# ------------------------------------------------------------
#  Default target
# ------------------------------------------------------------

help:
	@$(ECHO) ""
	@$(ECHO) " $(BLUE)MANDATORY RULES$(RESET)"
	@$(ECHO) ""
	@$(ECHO) "     $(BLUE)install$(RESET)      Install dependencies in venv"
	@$(ECHO) "     $(BLUE)run$(RESET)          Run the pipeline with preset values"
	@$(ECHO) "     $(BLUE)debug$(RESET)        Run the main script with pdb"
	@$(ECHO) "     $(BLUE)clean$(RESET)        Remove temporary files and caches"
	@$(ECHO) "     $(BLUE)lint$(RESET)         Execute flake8 + mypy (standard flags)"
	@$(ECHO) "     $(BLUE)lint-strict$(RESET)  Execute flake8 + mypy --strict"
	@$(ECHO) ""
	@$(ECHO) " $(CYAN)BONUS RULES$(RESET)"
	@$(ECHO) ""
	@$(ECHO) "     $(CYAN)campus-init$(RESET)  Set up environment in /tmp"
	@$(ECHO) "     $(CYAN)visual$(RESET)       Run generation with live state-machine visualization"
	@$(ECHO) "     $(CYAN)test$(RESET)         Run test suite"
	@$(ECHO) "     $(CYAN)run-alt$(RESET)      Run the pipeline with another model"
	@$(ECHO) "     $(CYAN)clean-venv$(RESET)   Remove the venv"
	@$(ECHO) ""

# ------------------------------------------------------------
#  install — create a virtual environment and install deps
# ------------------------------------------------------------

install:
	@$(ECHO) "$(YELLOW)>>> Creating virtual environment in $(VENV)...$(RESET)"
	python3 -m venv $(VENV)
	@$(ECHO) "$(YELLOW)>>> Installing uv in the virtual environment...$(RESET)"
	$(PYTHON_VENV) -m pip install --upgrade pip
	$(PYTHON_VENV) -m pip install uv
	@$(ECHO) "$(YELLOW)>>> Installing dependencies from pyproject.toml...$(RESET)"
	$(UV) pip install --python $(VENV) .
	@$(ECHO) "$(CYAN)>>> Environment ready! Activate it with: source $(VENV)/bin/activate$(RESET)"

# ------------------------------------------------------------
#  run — execute the main script
# ------------------------------------------------------------

run:
	@$(ECHO) "$(YELLOW)>>> Running the function calling tool...$(RESET)"
	@$(PYTHON) -m src \
	--functions_definition $(FUNC_DEF) \
	--input $(INPUT_F) \
	--output $(OUTPUT_F)

# ------------------------------------------------------------
#  debug — launch the main script under pdb
# ------------------------------------------------------------

debug:
	@$(ECHO) "$(YELLOW)>>> Launching src module under pdb...$(RESET)"
	$(PYTHON) -m pdb src \
	--functions_definition $(FUNC_DEF) \
	--input $(INPUT_F) \
	--output $(OUTPUT_F)

# ------------------------------------------------------------
#  clean — remove byte-compiled files and tool caches
# ------------------------------------------------------------

clean:
	@$(ECHO) "$(YELLOW)>>> Removing Python bytecode caches...$(RESET)"
	@$(FIND) . -type d -name "__pycache__" -exec $(RM) {} + $(IGNORE)
	@$(FIND) . -type f -name "*.pyc" -delete $(IGNORE)
	@$(FIND) . -type f -name "*.pyo" -delete $(IGNORE)
	@$(ECHO) "$(YELLOW)>>> Removing test & linter caches...$(RESET)"
	@$(FIND) . -type d -name ".mypy_cache" -exec $(RM) {} + $(IGNORE)
	@$(FIND) . -type d -name ".ruff_cache" -exec $(RM) {} + $(IGNORE)
	@$(FIND) . -type d -name ".pytest_cache" -exec $(RM) {} + $(IGNORE)
	@$(ECHO) "$(YELLOW)>>> Removing build artifacts and package infos...$(RESET)"
	@$(FIND) . -type d -name "*.egg-info" -exec $(RM) {} + $(IGNORE)
	@$(RM) build/ dist/ .uv/
	@$(ECHO) "$(YELLOW)>>> Removing generated output files...$(RESET)"
	@$(RM) $(OUTPUT_F)
	@$(ECHO) "$(CYAN)>>> Clean complete.$(RESET)"

# ------------------------------------------------------------
#  lint — standard type-checking and style enforcement
# ------------------------------------------------------------

lint:
	@$(ECHO) "$(YELLOW)>>> Running flake8...$(RESET)"
	@$(FLAKE8) . $(EXCLUDE) $(IGNORE)
	@$(ECHO) "$(YELLOW)>>> Running mypy (standard)...$(RESET)"
	@$(MYPY) . \
	    --warn-return-any \
	    --warn-unused-ignores \
	    --ignore-missing-imports \
	    --disallow-untyped-defs \
	    --check-untyped-defs

# ------------------------------------------------------------
#  lint-strict — maximum mypy strictness (recommended)
# ------------------------------------------------------------

lint-strict:
	@$(ECHO) "$(YELLOW)>>> Running flake8...$(RESET)"
	@$(FLAKE8) . $(EXCLUDE) $(IGNORE) 
	@$(ECHO) "$(YELLOW)>>> Running mypy (strict)...$(RESET)"
	@$(MYPY) . --strict

# ------------------------------------------------------------
#  test — test the project with pytest framework 
# ------------------------------------------------------------

test:
	@$(ECHO) "$(YELLOW)>>> Running Test Suite UI...$(RESET)"
	@$(PYTHON) -m tests 

# ------------------------------------------------------------
#  campus-init — Set up environment in /tmp to bypass space constraints
# ------------------------------------------------------------

campus-init:
	@$(ECHO) "$(YELLOW)>>> Routing uv cache to /tmp...$(RESET)"
	@export UV_CACHE_DIR="/tmp/$(USER)_uv_cache"; \
	$(ECHO) "$(YELLOW)>>> Creating venv in /tmp...$(RESET)" ; \
	$(UV) venv "/tmp/$(USER)_callmemaybe_$(VENV)" ; \
	$(ECHO) "$(YELLOW)>>> Linking $(VENV)...$(RESET)" ; \
	$(RM) $(VENV) ; \
	ln -s "/tmp/$(USER)_callmemaybe_$(VENV)" $(VENV) ; \
	$(ECHO) "$(YELLOW)>>> Syncing dependencies...$(RESET)" ; \
	$(UV) sync
	@$(ECHO) "$(CYAN)>>> Campus environment ready! You can access it via: source $(VENV)/bin/activate$(RESET)"

# ------------------------------------------------------------
#  clean-venv — remove virtual environment
# ------------------------------------------------------------

clean-venv:
	@$(ECHO) "$(YELLOW)>>> Cleaning virtual environment and caches...$(RESET)"
	@$(RM) $(VENV)
	@$(RM) $(UV_CACHE_DIR)
	@$(RM) "/tmp/$(USER)_venv"
	@$(RM) .venv
	@$(ECHO) "$(CYAN)>>> Virtual environment cleanup complete.$(RESET)"

# ------------------------------------------------------------
#  visual — Visualise the generation process 
# ------------------------------------------------------------

visual:
	@$(ECHO) "$(YELLOW)>>> Running the function calling tool with generation process visuals...$(RESET)"
	@$(PYTHON) -m src \
	--functions_definition $(FUNC_DEF) \
	--input $(INPUT_F) \
	--output $(OUTPUT_F) \
	--verbose

# ------------------------------------------------------------
#  run-alt — execute the main script and clean up model weights
# ------------------------------------------------------------

run-alt:
	@$(ECHO) "$(YELLOW)>>> Running engine with model: $(ALT)...$(RESET)"
	@export HF_HOME="/tmp/$(USER)_hf_alt_cache"; \
	LLM_MODEL_NAME="$(ALT)" $(PYTHON) -m src \
	--functions_definition $(FUNC_DEF) \
	--input $(INPUT_F) \
	--output $(OUTPUT_F) \
	--verbose; \
	EXIT_STATUS=$$?; \
	$(ECHO) "$(YELLOW)>>> Cleaning up downloaded model weights from /tmp...$(RESET)"; \
	$(RM) "/tmp/$(USER)_hf_alt_cache"; \
	if [ $$EXIT_STATUS -eq 0 ]; then \
		$(ECHO) "$(CYAN)>>> Alternative model test complete and cleaned.$(RESET)"; \
	else \
		$(ECHO) "$(RED)>>> Engine crashed, but tmp was still cleaned.$(RESET)"; \
	fi; \
	exit $$EXIT_STATUS
