"""
deduplicator.py
===============
Algoritmo de deduplicación y filtrado inteligente de recortes Kindle.
"""

from typing import List, Dict, Any


def deduplicate_clips(clips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Group by book
    clips.sort(key=lambda x: (x["book_title"], x["page"]))

    filtered = []
    # 1. Filter out clips whose content is a substring of another clip in the same book
    for i, c1 in enumerate(clips):
        is_sub = False
        for j, c2 in enumerate(clips):
            if (
                i != j
                and c1["book_title"] == c2["book_title"]
                and c1["content"] in c2["content"]
                and len(c1["content"]) < len(c2["content"])
            ):
                is_sub = True
                break
        if not is_sub:
            filtered.append(c1)

    # 2. Filter exact duplicate key (book_title, page, content)
    unique_clips = []
    seen = set()
    for c in filtered:
        key = (c["book_title"], c["page"], c["content"].strip())
        if key not in seen:
            seen.add(key)
            unique_clips.append(c)

    return unique_clips
