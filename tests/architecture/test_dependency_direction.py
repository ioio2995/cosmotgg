"""Architecture invariant: `core` and `tests/core` must never depend on `models`.

Scope and limits of this check
-------------------------------
This test performs a static AST scan of import statements found in
`src/cosmotgg/core/**/*.py` and `tests/core/**/*.py`. It detects, at
minimum:

- `import cosmotgg.models` / `import cosmotgg.models.sub...`;
- `from cosmotgg.models import ...` / `from cosmotgg.models.sub import ...`;
- `from cosmotgg import models`;
- statically detectable relative imports manifestly directed at a
  `models` package/module (e.g. `from . import models`,
  `from .models import ...`, `from ..models import ...`).

It does NOT claim to detect every possible dynamic import mechanism
(`importlib.import_module(...)`, `__import__(...)`, string-based module
loading, or any other non-static indirection). It is a structural
guardrail against statically detectable violations of the
`core -X-> models` dependency direction, not a complete proof of absence
of any dependency.
"""

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = REPO_ROOT / "src" / "cosmotgg" / "core"
TESTS_CORE_DIR = REPO_ROOT / "tests" / "core"


def _iter_python_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.rglob("*.py"))


def _is_forbidden_models_import(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(
            alias.name == "cosmotgg.models" or alias.name.startswith("cosmotgg.models.")
            for alias in node.names
        )

    if isinstance(node, ast.ImportFrom):
        module = node.module or ""

        if node.level == 0:
            if module == "cosmotgg.models" or module.startswith("cosmotgg.models."):
                return True
            if module == "cosmotgg":
                return any(alias.name == "models" for alias in node.names)
            return False

        # Relative import (node.level >= 1): flag statically detectable
        # imports manifestly directed at a `models` package/module.
        if module == "models" or module.startswith("models."):
            return True
        if module == "":
            return any(alias.name == "models" for alias in node.names)
        return False

    return False


def _find_violations(path: Path) -> list[tuple[Path, int]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    return [
        (path, node.lineno)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom)) and _is_forbidden_models_import(node)
    ]


@pytest.mark.parametrize(
    "directory", [CORE_DIR, TESTS_CORE_DIR], ids=["core", "tests_core"]
)
def test_no_static_import_of_models(directory: Path):
    violations: list[tuple[Path, int]] = []
    for path in _iter_python_files(directory):
        violations.extend(_find_violations(path))

    assert not violations, (
        "Statically detectable import(s) of cosmotgg.models found where "
        f"forbidden: {violations}"
    )
