"""
generator.py
============
Generador de artefactos de Skill para IA (SKILL.md, dataset.json, knowledge.md),
con soporte para múltiples roles (Auditor, Coach, Debater), asignación automática
inteligente por naturaleza del libro, Arena de Debate y la Regla de Juicio Crítico Humano.
"""

import os
import json
import re
from typing import List, Dict, Any


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "book-skill"


ROLE_PROMPTS = {
    "auditor": {
        "title": "Auditor Metodológico y Diagnóstico",
        "description": "Evalúa y audita proyectos, decisiones o código verificando el cumplimiento estricto de las reglas del libro.",
        "behavior": """- Actúa como un auditor metódico e implacable.
- Compara los planteamientos del usuario contra las directrices y reglas del libro.
- Si detectas prácticas contrarias a la metodología del autor, señálalas con las evidencias exactas del dataset."""
    },
    "coach": {
        "title": "Consultor y Coach Estratégico",
        "description": "Ayuda a aplicar los principios abstractos y la filosofía del libro a situaciones reales de trabajo.",
        "behavior": """- Actúa como un mentor reflexivo y orientado a la acción.
- Guía al usuario haciendo preguntas para aplicar los conceptos clave del libro a sus problemas diarios.
- Conecta las tesis del autor con las decisiones del proyecto del usuario."""
    },
    "debater": {
        "title": "Oponente Socrático y Abogado del Diablo",
        "description": "Desafía las asunciones del usuario poniendo a prueba la solidez de sus hipótesis frente al libro.",
        "behavior": """- Actúa como un oponente socrático y riguroso.
- Lleva la contraria de forma constructiva usando pasajes del libro para que el usuario defienda sus posturas.
- Pon a prueba las asunciones no cuestionadas del usuario."""
    }
}

CRITICAL_JUDGMENT_RULE = """
---

## 🛡️ Principio Innegociable: Juicio Crítico Humano no Delegable

> [!CAUTION]
> **REGLA DE ORO**: Como IA, tu objetivo es enriquecer y desafiar el pensamiento del usuario, NUNCA sustituirlo.
> Si detectas que el usuario intenta delegar su criterio a ciegas o muestra falta de comprensión de las bases del libro, DEBES responder activamente:
> 
> *"⚠️ Un humano nunca debe dimitir de su juicio crítico. Para tomar una decisión con criterio sobre este asunto, es fundamental que domines las siguientes bases extraídas de tus lecturas que parecen no estar asumidas en tu planteamiento: [Base 1, Base 2]..."*
"""


def detect_role_for_book(book_title: str, clips: List[Dict[str, Any]]) -> str:
    title_lower = book_title.lower()

    # Technical / Methodological / Software Engineering -> Auditor
    auditor_keywords = [
        "tdd", "ddd", "agile", "growth", "impact", "code", "clean",
        "refactoring", "domain-driven", "architecture", "design",
        "desarrollo", "software", "programación", "métricas"
    ]
    for kw in auditor_keywords:
        if kw in title_lower:
            return "auditor"

    # Philosophical / Political / Critical / Essay -> Debater
    debater_keywords = [
        "marx", "antifrágil", "antifragil", "taleb", "pensamiento crítico",
        "filosofía", "política", "no seas tú mismo", "applebaum", "social",
        "capitalismo", "ideología", "ensayo"
    ]
    for kw in debater_keywords:
        if kw in title_lower:
            return "debater"

    # Default for reflective / history / personal development -> Coach
    return "coach"


def generate_skill_for_book(
    book_title: str,
    clips: List[Dict[str, Any]],
    role: str = "auto",
    output_dir: str = "skills"
) -> str:
    if not clips:
        raise ValueError(f"No hay recortes para el libro '{book_title}'")

    role_key = role.lower()
    if role_key == "auto":
        role_key = detect_role_for_book(book_title, clips)

    if role_key not in ROLE_PROMPTS:
        role_key = "coach"

    role_info = ROLE_PROMPTS[role_key]
    author = clips[0]["author"]
    slug = slugify(book_title)
    skill_dir = os.path.join(output_dir, slug)
    os.makedirs(skill_dir, exist_ok=True)

    # 1. dataset.json
    dataset_path = os.path.join(skill_dir, "dataset.json")
    dataset_data = {
        "book_title": book_title,
        "author": author,
        "role_type": role_key,
        "total_clips": len(clips),
        "clips": [
            {
                "id": i + 1,
                "page": c["page"],
                "meta": c["meta"],
                "content": c["content"]
            }
            for i, c in enumerate(clips)
        ]
    }
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset_data, f, ensure_ascii=False, indent=2)

    # 2. knowledge.md
    knowledge_path = os.path.join(skill_dir, "knowledge.md")
    with open(knowledge_path, "w", encoding="utf-8") as f:
        f.write(f"# 📚 Evidencias de Lectura: {book_title}\n\n")
        f.write(f"**Autor:** {author}\n")
        f.write(f"**Rol asignado:** {role_info['title']} ({role_key})\n")
        f.write(f"**Total de recortes:** {len(clips)}\n\n")
        f.write("---\n\n")
        for i, c in enumerate(clips, 1):
            f.write(f"### Recorte #{i} (Página/Posición: {c['page']})\n")
            f.write(f"> {c['content']}\n\n")
            f.write(f"*Metadatos: {c['meta']}*\n\n---\n\n")

    # 3. SKILL.md
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(f"""---
name: {slug}
description: Skill de {role_info['title']} basada en '{book_title}' de {author}.
---

# 📖 Asistente Experto: {book_title} ({role_info['title']})

> **Rol**: Eres un {role_info['title']} respaldado por los recortes y evidencias del libro **{book_title}** ({author}).
> {role_info['description']}

---

## 🎯 Directrices de Comportamiento

{role_info['behavior']}

---

## 📁 Base de Conocimiento

- **Dataset en JSON**: `dataset.json`
- **Guía de Evidencias**: `knowledge.md`
{CRITICAL_JUDGMENT_RULE}
""")

    return skill_dir


def generate_arena_skill(
    all_clips: List[Dict[str, Any]],
    output_dir: str = "skills"
) -> str:
    if not all_clips:
        raise ValueError("No hay recortes para generar la Arena de Debate.")

    slug = "book-arena"
    skill_dir = os.path.join(output_dir, slug)
    os.makedirs(skill_dir, exist_ok=True)

    books = {}
    for c in all_clips:
        bt = c["book_title"]
        if bt not in books:
            books[bt] = {"author": c["author"], "clips": []}
        books[bt]["clips"].append(c)

    dataset_path = os.path.join(skill_dir, "dataset.json")
    dataset_data = {
        "arena_title": "Arena de Debate Multilibro",
        "total_books": len(books),
        "books": [
            {
                "title": bt,
                "author": data["author"],
                "clips_count": len(data["clips"]),
                "clips": data["clips"]
            }
            for bt, data in books.items()
        ]
    }
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset_data, f, ensure_ascii=False, indent=2)

    skill_path = os.path.join(skill_dir, "SKILL.md")
    books_summary = "\n".join([f"- **{bt}** ({data['author']}): {len(data['clips'])} recortes" for bt, data in books.items()])

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(f"""---
name: book-arena
description: Skill de Arena de Debate Socrático y Cruce de Tesis entre múltiples libros.
---

# 🤼 Arena de Debate Socrático entre Autores

> **Rol**: Eres un Moderador y Facilitador Socrático que orquesta debates cruzados entre las tesis de los diferentes libros leídos por el usuario.

---

## 📚 Libros en la Arena

{books_summary}

---

## 🎯 Modos de Funcionamiento en la Arena

1. **🥊 Debate entre Autores**: Haz que las tesis de dos o más libros contrasten sobre el problema que te plantee el usuario.
2. **🔀 Cruce de Metodologías**: Analiza cómo aplicar los principios del Libro A para resolver las limitaciones del Libro B.
3. **🧪 Examen de Casos Reales**: Pide al usuario su caso práctico y somételo a la crítica cruzada de los autores.
{CRITICAL_JUDGMENT_RULE}
""")

    return skill_dir
