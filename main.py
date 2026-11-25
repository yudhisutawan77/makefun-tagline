"""make.fun tagline entry.

Writes a single original tagline for make.fun to the output path the
grader expects (``/output/entry.txt`` per RULES.txt), honouring an
explicit output location when one is provided through the environment.
"""

import os

TAGLINE = "AI agents enter open bounties, ship their best code, and win USDC in the open."


def resolve_output_path() -> str:
    """Return the file path the tagline must be written to.

    RULES.txt names ``/output/entry.txt``. An environment variable, when
    set, overrides it; a value that names a directory gets
    ``entry.txt`` appended inside it. MAKEFUN_OUTPUT_DIR is the
    directory the kit harness exports, so it is honoured right after
    an explicit ENTRY_OUT. Priority is ENTRY_OUT first, then
    MAKEFUN_OUTPUT_DIR, then ENTRY_OUT_DIR / OUTPUT_DIR / OUTPUT_PATH,
    and finally the default /output/entry.txt.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        return entry_out if not os.path.isdir(entry_out) else os.path.join(entry_out, "entry.txt")
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        # MAKEFUN_OUTPUT_DIR always names a directory, even when it
        # does not exist yet (makedirs in main() creates it).
        return os.path.join(makefun_dir, "entry.txt")
    for name in ("ENTRY_OUT_DIR", "OUTPUT_DIR", "OUTPUT_PATH"):
        value = os.environ.get(name)
        if value:
            return value if not os.path.isdir(value) else os.path.join(value, "entry.txt")
    return "/output/entry.txt"


def main() -> None:
    """Validate the tagline and write it to the resolved output path."""
    text = TAGLINE.strip()
    if not 1 <= len(text) <= 100:
        raise SystemExit(f"tagline must be 1-100 characters, got {len(text)}")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


if __name__ == "__main__":
    main()
