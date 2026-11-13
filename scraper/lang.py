"""English-only filter for memory folders.

Each memory file (frontmatter and fenced code removed) is classified with lingua;
a folder is English if >= MIN_EN_FRAC of its files are detected as English.
"""

import re

from lingua import Language, LanguageDetectorBuilder

MIN_EN_FRAC = 0.8
_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()


def _prose(text: str) -> str:
    text = re.sub(r"\A---\s*\n.*?\n---", "", text, flags=re.S)  # frontmatter
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # code blocks
    return re.sub(r"`[^`]*`", "", text)  # inline code


def file_language(text: str):
    lang = _detector.detect_language_of(_prose(text))
    return lang.name.lower() if lang else None


def english_fraction(files: dict) -> float:
    """files: {path: text}; MEMORY.md index excluded."""
    langs = [file_language(t) for p, t in files.items() if not p.endswith("MEMORY.md")]
    return sum(l == "english" for l in langs) / len(langs) if langs else 0.0
