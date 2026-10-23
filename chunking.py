import re


def chunk_text(text: str, target_words: int = 250, min_words: int = 200) -> list[str]:
    """Split at sentence boundaries, with a word-boundary fallback for long sentences."""
    if target_words <= 0 or min_words <= 0 or min_words > target_words:
        raise ValueError("Chunk sizes must satisfy 0 < min_words <= target_words")
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    units = []
    for sentence in sentences:
        words = sentence.split()
        while len(words) > target_words:
            units.append(" ".join(words[:target_words]))
            words = words[target_words:]
        if words:
            units.append(" ".join(words))

    chunks, current = [], []
    for unit in units:
        words = unit.split()
        if current and len(current) + len(words) > target_words:
            chunks.append(" ".join(current))
            current = []
        current.extend(words)
    if current:
        if chunks and len(current) < min_words and len(chunks[-1].split()) + len(current) <= target_words:
            chunks[-1] += " " + " ".join(current)
        else:
            chunks.append(" ".join(current))
    return chunks
