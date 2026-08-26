"""Architecture invariant: SCIENTIFIC_METADATA on every public core module.

Verifies (per `docs/governance/software-architecture-governance.md` §5)
that every public module of `cosmotgg.core` exposes a `SCIENTIFIC_METADATA`
mapping conforming to the closed status taxonomy, with the fields required
by each status, and that `normative_reference` (when required) points to an
existing file and, when it carries an anchor, to a heading that actually
exists in that Markdown document.

This test verifies the *declarative structure* of `SCIENTIFIC_METADATA`. It
makes no claim about the scientific truth of a module's classification.

No `project-defined` module currently exists in `core`. The validation
branch for `project-defined` is nonetheless implemented and exercised below
against synthetic metadata, to protect the future evolution of `core`.
"""

import importlib
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = REPO_ROOT / "src" / "cosmotgg" / "core"

ALLOWED_STATUS = {"established", "project-defined"}


def _iter_core_module_names() -> list[str]:
    names = []
    for path in sorted(CORE_DIR.rglob("*.py")):
        relative = path.relative_to(REPO_ROOT / "src")
        parts = relative.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        names.append(".".join(parts))
    return names


def _slugify_heading(text: str) -> str:
    """Minimal, deterministic ASCII heading slug (lowercase, hyphenated).

    Scope: this resolver only supports plain ASCII Markdown ATX headings
    (`# ...`). It does not claim to reproduce every edge case of a
    particular Markdown renderer's anchor algorithm (e.g. accented
    characters, duplicate-heading disambiguation suffixes).
    """
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug


def _markdown_headings(markdown_path: Path) -> set[str]:
    headings = set()
    for line in markdown_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.*)$", line.strip())
        if match:
            headings.add(_slugify_heading(match.group(1)))
    return headings


def _validate_metadata(module_name: str, metadata) -> None:
    assert isinstance(metadata, dict), f"{module_name}: SCIENTIFIC_METADATA must be a dict"
    assert set(metadata.keys()) == {"status", "origin_model", "normative_reference"}, (
        f"{module_name}: SCIENTIFIC_METADATA has unexpected keys: {sorted(metadata.keys())}"
    )

    status = metadata["status"]
    assert status in ALLOWED_STATUS, f"{module_name}: invalid status {status!r}"

    origin_model = metadata["origin_model"]
    normative_reference = metadata["normative_reference"]

    if status == "established":
        assert origin_model is None, f"{module_name}: origin_model must be None for established"
        assert normative_reference is None, (
            f"{module_name}: normative_reference must be None for established"
        )
        return

    # status == "project-defined"
    assert origin_model, f"{module_name}: origin_model must be non-empty for project-defined"
    assert normative_reference, (
        f"{module_name}: normative_reference must be non-empty for project-defined"
    )

    reference_path_str, _, anchor = normative_reference.partition("#")
    resolved_path = REPO_ROOT / reference_path_str
    assert resolved_path.exists(), (
        f"{module_name}: normative_reference file does not exist: {reference_path_str}"
    )

    if anchor:
        headings = _markdown_headings(resolved_path)
        assert anchor in headings, (
            f"{module_name}: anchor #{anchor} not found in {reference_path_str}"
        )


@pytest.mark.parametrize("module_name", _iter_core_module_names())
def test_core_module_has_valid_scientific_metadata(module_name: str):
    module = importlib.import_module(module_name)
    assert hasattr(module, "SCIENTIFIC_METADATA"), (
        f"{module_name} must expose SCIENTIFIC_METADATA"
    )
    _validate_metadata(module_name, module.SCIENTIFIC_METADATA)


def test_invalid_status_is_rejected():
    with pytest.raises(AssertionError):
        _validate_metadata(
            "synthetic.module",
            {"status": "unknown-status", "origin_model": None, "normative_reference": None},
        )


def test_project_defined_requires_origin_model_and_reference():
    with pytest.raises(AssertionError):
        _validate_metadata(
            "synthetic.module",
            {
                "status": "project-defined",
                "origin_model": None,
                "normative_reference": "docs/governance/software-architecture-governance.md",
            },
        )


def test_project_defined_rejects_missing_reference_file():
    with pytest.raises(AssertionError):
        _validate_metadata(
            "synthetic.module",
            {
                "status": "project-defined",
                "origin_model": "modelXX",
                "normative_reference": "docs/does/not/exist.md#anchor",
            },
        )


def test_project_defined_accepts_existing_reference_without_anchor():
    _validate_metadata(
        "synthetic.module",
        {
            "status": "project-defined",
            "origin_model": "modelXX",
            "normative_reference": "docs/governance/software-architecture-governance.md",
        },
    )


def test_project_defined_accepts_reference_with_matching_anchor(tmp_path):
    doc = tmp_path / "spec.md"
    doc.write_text("# Title\n\n## Some Established Reference\n", encoding="utf-8")

    _validate_metadata(
        "synthetic.module",
        {
            "status": "project-defined",
            "origin_model": "modelXX",
            "normative_reference": f"{doc}#some-established-reference",
        },
    )


def test_project_defined_rejects_reference_with_mismatched_anchor(tmp_path):
    doc = tmp_path / "spec.md"
    doc.write_text("# Title\n\n## Some Established Reference\n", encoding="utf-8")

    with pytest.raises(AssertionError):
        _validate_metadata(
            "synthetic.module",
            {
                "status": "project-defined",
                "origin_model": "modelXX",
                "normative_reference": f"{doc}#missing-anchor",
            },
        )
