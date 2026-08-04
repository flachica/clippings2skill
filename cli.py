#!/usr/bin/env python3
"""
cli.py — CLI principal de clippings2skill
========================================
Convierte recortes de Kindle (My Clippings.txt) en Skills ejecutables para IA.

Uso:
  python3 cli.py --list
  python3 cli.py --book "The Lean Startup" --role coach
  python3 cli.py --arena
"""

import os
import sys
import argparse
from clippings2skill.parser import parse_clippings_file, get_books_summary
from clippings2skill.deduplicator import deduplicate_clips
from clippings2skill.generator import generate_skill_for_book, generate_arena_skill
from clippings2skill.syncer import sync_skills


def main():
    parser = argparse.ArgumentParser(
        description="clippings2skill — Kindle My Clippings to Multi-LLM Agent Skills Generator"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="My Clippings.txt",
        help="Ruta al fichero de recortes (por defecto: My Clippings.txt, fallback a tests/sample_clippings.txt si no existe)",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="Listar todos los libros encontrados en el fichero de recortes",
    )
    parser.add_argument(
        "--book",
        "-b",
        help="Título exacto del libro o parte del título para generar su Skill (usa 'all' para todos)",
    )
    parser.add_argument(
        "--role",
        "-r",
        choices=["auditor", "coach", "debater", "auto"],
        default="coach",
        help="Rol asignado a la Skill generada: auditor, coach, debater (por defecto: coach)",
    )
    parser.add_argument(
        "--arena",
        "-a",
        action="store_true",
        help="Generar la Meta-Skill 'book-arena' para debate cruzado socrático entre todos los libros leídos",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="skills",
        help="Directorio donde guardar las skills generadas (por defecto: skills/)",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Desactivar la sincronización automática con carpetas de agentes (.gemini, .claude, .opencode)",
    )

    args = parser.parse_args()

    input_file = args.input
    if not os.path.exists(input_file):
        fallback_path = os.path.join("tests", "sample_clippings.txt")
        if input_file == "My Clippings.txt" and os.path.exists(fallback_path):
            print(f"ℹ️ 'My Clippings.txt' no encontrado. Usando '{fallback_path}' de muestra.")
            input_file = fallback_path
        else:
            print(f"❌ Error: El archivo '{input_file}' no existe.", file=sys.stderr)
            sys.exit(1)

    print(f"📖 Parseando recortes desde: {input_file}...")
    raw_clips = parse_clippings_file(input_file)
    print(f"🔹 Recortes totales encontrados: {len(raw_clips)}")

    cleaned_clips = deduplicate_clips(raw_clips)
    print(f"✨ Recortes después de deduplicar: {len(cleaned_clips)}")

    books_summary = get_books_summary(cleaned_clips)

    if args.list:
        print("\n📚 Libros encontrados en el fichero:")
        print("=" * 60)
        for i, b in enumerate(books_summary, 1):
            print(f"{i:2d}. {b['title']} (Autor: {b['author']}) — {b['count']} recortes")
        print("=" * 60)
        print("\nPara generar la skill de un libro ejecuta:")
        print('  python3 cli.py --book "Nombre del Libro" --role [auditor|coach|debater]')
        print("Para generar la Arena de Debate entre todos los libros:")
        print("  python3 cli.py --arena")
        return

    if args.arena:
        print("\n🤼 Generando Meta-Skill de Arena de Debate Multilibro...")
        arena_dir = generate_arena_skill(cleaned_clips, output_dir=args.output_dir)
        print(f"🎉 Arena de Debate generada con éxito en: {arena_dir}")

    if args.book:
        target_title = args.book
        books_to_process = []
        if target_title.lower() == "all":
            books_to_process = [b["title"] for b in books_summary]
        else:
            matches = [b for b in books_summary if target_title.lower() in b["title"].lower()]
            if not matches:
                print(f"❌ No se encontró ningún libro que coincida con '{target_title}'")
                return
            books_to_process = [matches[0]["title"]]

        print(f"\n🔨 Generando Skills de IA con rol [{args.role}]...")
        for b_title in books_to_process:
            book_clips = [c for c in cleaned_clips if c["book_title"] == b_title]
            skill_dir = generate_skill_for_book(
                b_title, book_clips, role=args.role, output_dir=args.output_dir
            )
            print(f"🎉 Skill generada con éxito en: {skill_dir}")

    if not args.book and not args.arena:
        print("\n⚠️ Especifica un libro con --book \"Título\", usa --arena para la Arena de Debate, o usa --list para listar los libros.")
        return

    if not args.no_sync:
        print("\n🔄 Sincronizando con Agentes Multi-LLM (.gemini, .claude, .opencode)...")
        sync_logs = sync_skills()
        for log in sync_logs:
            print(f"  {log}")
        print("✨ Sincronización completada.")


if __name__ == "__main__":
    main()
