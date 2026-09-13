from typing import List, Dict, Any


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> List[str]:
    """Splits text into chunks by character count with overlap, attempting to split at sentence/paragraph boundaries."""
    if not text or not text.strip():
        return []

    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current_chunk = ""

    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue

        if len(current_chunk) + len(p_clean) + 2 <= chunk_size:
            current_chunk = f"{current_chunk}\n\n{p_clean}" if current_chunk else p_clean
        else:
            if current_chunk:
                chunks.append(current_chunk)

            if len(p_clean) > chunk_size:
                # Splitting large paragraphs into sliding window chunks
                words = p_clean.split()
                sub_chunk = ""
                for w in words:
                    if len(sub_chunk) + len(w) + 1 <= chunk_size:
                        sub_chunk = f"{sub_chunk} {w}" if sub_chunk else w
                    else:
                        chunks.append(sub_chunk)
                        # Carry overlap
                        overlap_words = sub_chunk.split()[-20:] if sub_chunk else []
                        sub_chunk = f"{' '.join(overlap_words)} {w}".strip()
                if sub_chunk:
                    current_chunk = sub_chunk
                else:
                    current_chunk = ""
            else:
                current_chunk = p_clean

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
