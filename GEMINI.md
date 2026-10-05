# Coding & Style Guidelines (PEP 8 & PEP 257)

This project strictly adheres to the official Python Style Guide (PEP 8) and Docstring Conventions (PEP 257). All code, comments, docstrings, and tests written or modified in this repository must comply with the rules below.

---

## 1. Line Length Restrictions

- **Code statements**: Strictly maximum **79 characters**.
- **Flowing comments and docstrings**: Strictly maximum **72 characters**.
- Wrap long lines using Python's implied line continuation inside parentheses, brackets, and braces rather than backslashes whenever possible.

---

## 2. Comments & Documentation

### Comment Conventions
- **Complete Sentences**: Every comment must be a complete, grammatically correct sentence starting with a capital letter and ending with appropriate punctuation (period, etc.).
- **Block Comments**:
  - Must apply to code following them and be indented to the same level as that code.
  - Each line must start with a `# ` (hash followed by a single space).
  - Paragraphs inside block comments should be separated by a line containing a single `#`.
- **Inline Comments**:
  - Use sparingly and only when non-obvious rationale is required. Never state the obvious.
  - Must be separated from the code by at least **two spaces**: `x = x + 1  # Compensate for border offset.`
- **Documentation Integrity**: Preserve existing comments and docstrings unless explicitly requested to update or refactor them.

### Docstring Conventions (PEP 257)
- **Coverage**: Every public module, class, method, function, and public `@property` must have a docstring.
- **One-line Docstrings**: Closing `"""` must be on the same line as the opening `"""`. Example:
  ```python
  """Return a copy of the simulation state vector."""
  ```
- **Multi-line Docstrings**:
  - Summary line on the first line (or right after opening `"""`).
  - Blank line after summary.
  - Detailed description wrapped at $\le 72$ characters.
  - Closing `"""` placed on a line by itself.
- **Internal / Non-public Methods**:
  - Methods prefixed with `_` must include an explanatory comment directly following the `def` statement describing their internal behavior.

---

## 3. Formatting, Spacing & Naming

- **Indentation**: 4 spaces per indentation level. Never use tabs.
- **Blank Lines**:
  - 2 blank lines surrounding top-level function and class definitions.
  - 1 blank line surrounding method definitions inside a class.
- **Imports**:
  - Grouped into:
    1. Standard library imports
    2. Related third-party imports
    3. Local application/library imports
  - Blank line between each group. Never use wildcard imports (`from module import *`).
- **Naming Conventions**:
  - Classes: `PascalCase` (e.g., `BiologicalModel`, `ParameterPanel`).
  - Functions & methods: `snake_case` (e.g., `simulate_model`, `rhs`).
  - Constants: `UPPER_CASE_WITH_UNDERSCORES` (e.g., `LIGHT_STYLESHEET`).
  - Non-public attributes/methods: Leading single underscore (e.g., `_buttons`, `_on_resize_debounced`).

---

## 4. Verification Workflow

Before completing any coding task or pull request:
1. **Linter Check**: Run `./.venv/bin/flake8 .` — must report `0` errors or warnings.
2. **Comment & Docstring Audit**: Ensure no comment or docstring line exceeds 72 characters and no public object lacks documentation.
3. **Test Suite**: Run `./.venv/bin/python tests/run_tests.py` — all unit and GUI tests must pass.
