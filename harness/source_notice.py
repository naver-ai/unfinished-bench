# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""The copyright notice at the top of the repository's source files, and its removal from the copies that go into task
folders and containers. Copies keep the exact bytes the benchmark was measured with, so the agent's environment does
not change and nothing in it names the benchmark."""
import shutil

NOTICE = ("# Unfinished-Bench", "# Copyright (c) 2026-present NAVER Corp.", "# Apache-2.0")
DERIVED = ("# Derived from hermes-agent 0.19.0 (https://github.com/NousResearch/hermes-agent)",
           "# Copyright (c) 2025 Nous Research. MIT License, see harness/hermes_patches/LICENSE.",
           "# Modified for Unfinished-Bench: changes are marked \"# PATCH\" and listed in harness/hermes_patches/README.md.")


def strip_notice(text):
    """Remove the notice lines: ours, or the one on the modified hermes-agent files (right after a shebang line, if any)."""
    lines = text.split("\n")
    i = 1 if lines and lines[0].startswith("#!") else 0
    for block in (NOTICE, DERIVED):
        if tuple(lines[i:i + len(block)]) == block:
            del lines[i:i + len(block)]
            break
    return "\n".join(lines)


def copy_without_notice(src, dst):
    """shutil.copy for source files: same permission bits, notice removed."""
    with open(src, encoding="utf-8", newline="") as f:
        text = f.read()
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(strip_notice(text))
    shutil.copymode(src, dst)
    return dst
