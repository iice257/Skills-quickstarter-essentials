"""Post text helpers for the MCP layer."""

from __future__ import annotations

import re
import unicodedata
import urllib.parse
from dataclasses import dataclass


MAX_WEIGHTED_LENGTH = 280
TCO_URL_LENGTH = 23
COMPOSER_URL = "https://twitter.com/intent/tweet"
URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)


@dataclass(frozen=True)
class ValidationResult:
    text: str
    url: str | None
    weighted_length: int
    max_length: int = MAX_WEIGHTED_LENGTH

    @property
    def valid(self) -> bool:
        return self.weighted_length <= self.max_length

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "url": self.url,
            "weighted_length": self.weighted_length,
            "max_length": self.max_length,
            "valid": self.valid,
        }


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.lstrip("\ufeff")
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    return "\n".join(lines).strip()


def validate_url(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be fully qualified with http:// or https://")
    return url


def _is_cjk(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x2E80 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x20000 <= codepoint <= 0x2FA1F
    )


def _is_emoji_or_symbol(char: str) -> bool:
    codepoint = ord(char)
    return 0x1F000 <= codepoint <= 0x1FAFF or 0x2600 <= codepoint <= 0x27BF


def char_weight(char: str) -> int:
    if char in {"\u200d", "\ufe0e", "\ufe0f"}:
        return 0
    if char == "\n" or char == "\t":
        return 1
    codepoint = ord(char)
    if codepoint <= 0x024F:
        return 1
    if 0x2000 <= codepoint <= 0x206F:
        return 1
    if _is_cjk(char) or _is_emoji_or_symbol(char):
        return 2
    if unicodedata.category(char).startswith("M"):
        return 0
    return 2


def weighted_length(text: str) -> int:
    text = normalize_text(text)
    total = 0
    cursor = 0
    for match in URL_RE.finditer(text):
        for char in text[cursor : match.start()]:
            total += char_weight(char)
        total += TCO_URL_LENGTH
        cursor = match.end()
    for char in text[cursor:]:
        total += char_weight(char)
    return total


def countable_text(text: str, url: str | None = None) -> str:
    text = normalize_text(text)
    url = validate_url(url)
    if not url:
        return text
    if not text:
        return url
    return f"{text} {url}"


def validate_post(text: str, url: str | None = None) -> ValidationResult:
    url = validate_url(url)
    normalized = normalize_text(text)
    return ValidationResult(
        text=normalized,
        url=url,
        weighted_length=weighted_length(countable_text(normalized, url)),
    )


def build_intent_url(text: str, url: str | None = None) -> str:
    url = validate_url(url)
    result = validate_post(text, url)
    params = {"text": result.text}
    if url:
        params["url"] = url
    return f"{COMPOSER_URL}?{urllib.parse.urlencode(params)}"


def split_long_token(token: str, limit: int) -> list[str]:
    pieces: list[str] = []
    current = ""
    for char in token:
        candidate = current + char
        if current and weighted_length(candidate) > limit:
            pieces.append(current)
            current = char
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def _append_piece(chunks: list[str], current: str, piece: str, separator: str, limit: int) -> str:
    candidate = piece if not current else f"{current}{separator}{piece}"
    if weighted_length(candidate) <= limit:
        return candidate
    if current:
        chunks.append(current)
        current = ""
    if weighted_length(piece) <= limit:
        return piece
    split_pieces = split_long_token(piece, limit)
    chunks.extend(split_pieces[:-1])
    return split_pieces[-1]


def wrap_weighted(text: str, limit: int) -> list[str]:
    text = normalize_text(text)
    if not text:
        return []
    chunks: list[str] = []
    current = ""
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    for paragraph_index, paragraph in enumerate(paragraphs):
        if paragraph_index and current:
            candidate = f"{current}\n\n"
            if weighted_length(candidate) <= limit:
                current = candidate
            else:
                chunks.append(current)
                current = ""
        for word in paragraph.split():
            separator = "" if not current or current.endswith("\n\n") else " "
            current = _append_piece(chunks, current, word, separator, limit)
    if current:
        chunks.append(current)
    return chunks


def make_thread(text: str, url: str | None = None) -> list[str]:
    validate_url(url)
    target = 250
    while target >= 140:
        chunks = wrap_weighted(text, target)
        if not chunks:
            return []
        numbered = [f"{index}/{len(chunks)} {chunk}" for index, chunk in enumerate(chunks, 1)]
        if all(validate_post(chunk, url if index == len(numbered) else None).valid for index, chunk in enumerate(numbered, 1)):
            return numbered
        target -= 10
    raise ValueError("Could not split this text into valid post-sized chunks")
