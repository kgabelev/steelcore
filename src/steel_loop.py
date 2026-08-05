#!/usr/bin/env python3
"""
Generate a trap-flamenco verse, critique it, then generate an improved version.

Requires: pip install anthropic
Requires: ANTHROPIC_API_KEY set in the environment (or `ant auth login`).

Usage:
    python3 steel_loop.py
"""

import anthropic

MODEL = "claude-sonnet-5"
MAX_TOKENS = 800

client = anthropic.Anthropic()


def _extract_text(response: anthropic.types.Message) -> str:
    for block in response.content:
        if block.type == "text":
            return block.text.strip()
    return ""


def generate_verse() -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": (
                "Write a short trap-flamenco style verse, 8-12 lines. "
                "Blend flamenco imagery, cante, and rhythm with trap cadence "
                "and modern slang. Return only the verse, no commentary or "
                "preamble."
            ),
        }],
    )
    return _extract_text(response)


def critique_verse(verse: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": (
                "Critique the following trap-flamenco verse. Address flow, "
                "rhythm, and originality as three distinct points. Be "
                "concise and specific.\n\n"
                f"{verse}"
            ),
        }],
    )
    return _extract_text(response)


def improve_verse(verse: str, critique: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": (
                "Rewrite the verse below to address the critique. Keep it "
                "8-12 lines and in the same trap-flamenco style. Return "
                "only the improved verse, no commentary.\n\n"
                f"Original verse:\n{verse}\n\nCritique:\n{critique}"
            ),
        }],
    )
    return _extract_text(response)


def main() -> None:
    verse = generate_verse()
    critique = critique_verse(verse)
    improved = improve_verse(verse, critique)

    print("=" * 40)
    print("1. ORIGINAL")
    print("=" * 40)
    print(verse)
    print()

    print("=" * 40)
    print("2. CRITIQUE")
    print("=" * 40)
    print(critique)
    print()

    print("=" * 40)
    print("3. IMPROVED")
    print("=" * 40)
    print(improved)


if __name__ == "__main__":
    main()
