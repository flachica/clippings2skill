"""
parser.py
=========
Parseador de ficheros My Clippings.txt de Kindle.
"""

import os
import re
import sys
from typing import List, Dict, Any


def read_file_with_fallback_encoding(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc, errors="ignore") as f:
                return f.read()
        except Exception:
            continue

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_page_number(meta_str: str) -> int:
    m = re.search(r"página\s+(\d+)|page\s+(\d+)", meta_str, re.IGNORECASE)
    if m:
        return int(m.group(1) or m.group(2))
    m_loc = re.search(r"Posición\s+(\d+)|Location\s+(\d+)", meta_str, re.IGNORECASE)
    if m_loc:
        return int(m_loc.group(1) or m_loc.group(2))
    return 0


def parse_title_author(header_str: str) -> Dict[str, str]:
    header_str = header_str.strip()
    m = re.match(r"^(.*?)\s*\(([^()]+)\)$", header_str)
    if m:
        return {"title": m.group(1).strip(), "author": m.group(2).strip()}
    return {"title": header_str, "author": "Desconocido"}


def parse_clippings_file(filepath: str) -> List[Dict[str, Any]]:
    text = read_file_with_fallback_encoding(filepath)
    raw_entries = text.split("==========\n")
    clips = []

    for entry in raw_entries:
        lines = [line.strip() for line in entry.strip().split("\n") if line.strip()]
        if len(lines) >= 3:
            header = lines[0]
            meta = lines[1]
            content = "\n".join(lines[2:])

            if "<Has llegado al límite de recortes" in content or "<You have reached the clipping limit" in content:
                continue

            parsed_header = parse_title_author(header)
            page = extract_page_number(meta)

            clips.append({
                "book_title": parsed_header["title"],
                "author": parsed_header["author"],
                "raw_header": header,
                "meta": meta,
                "page": page,
                "content": content
            })

    return clips


def get_books_summary(clips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    books = {}
    for clip in clips:
        key = clip["book_title"]
        if key not in books:
            books[key] = {
                "title": clip["book_title"],
                "author": clip["author"],
                "count": 0
            }
        books[key]["count"] += 1

    return sorted(books.values(), key=lambda x: x["count"], reverse=True)
