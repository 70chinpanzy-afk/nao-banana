from __future__ import annotations

import pathlib
import py_compile


ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_file(path: str) -> None:
    target = ROOT / path
    if not target.exists():
        raise FileNotFoundError(f"Required file is missing: {path}")


def require_text(path: str, expected: str) -> None:
    target = ROOT / path
    content = target.read_text(encoding="utf-8")
    if expected not in content:
        raise AssertionError(f"{path} does not contain expected text: {expected}")


def main() -> None:
    py_compile.compile(str(ROOT / "app.py"), doraise=True)

    for path in [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    ]:
        require_file(path)

    require_text("README.md", "Nano Banana Pro")
    require_text("README.md", "Privacy and Security")
    require_text("SECURITY.md", "API key")
    require_text("LICENSE", "MIT License")


if __name__ == "__main__":
    main()
