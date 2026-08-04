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
from clippings2skill.generator import (
    generate_skill_for_book,
    generate_arena_skill,
    detect_role_for_book,
    ROLE_PROMPTS,
)
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
        default=None,
        help="Rol asignado a la Skill generada: auditor, coach, debater, auto (por defecto: auto - detección inteligente)",
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
        "--manual",
        "-m",
        action="store_true",
        help="Modo manual interactivo: Selecciona manualmente el rol (auditor, coach, debater) para cada libro para ahorrar tokens",
    )
    parser.add_argument(
        "--role-map",
        help="Mapa manual de roles en formato 'Titulo1:auditor,Titulo2:debater' para asignación directa sin interacción",
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
        print("\n📚 Libros encontrados en el fichero (Clasificados por Rol y Temática):")
        print("=" * 70)
        for i, b in enumerate(books_summary, 1):
            b_clips = [c for c in cleaned_clips if c["book_title"] == b["title"]]
            role_key = detect_role_for_book(b["title"], b_clips)
            role_title = ROLE_PROMPTS.get(role_key, ROLE_PROMPTS["coach"])["title"]
            print(f"{i:2d}. {b['title']} (Autor: {b['author']}) — {b['count']} recortes")
            print(f"    └─ Rol sugerido de IA: [{role_title}] ({role_key})")
        print("=" * 70)
        print("\nPara generar la skill de un libro ejecuta:")
        print('  python3 cli.py --book "Nombre del Libro" --role [auditor|coach|debater]')
        print("Para generar todas las skills interactivamente:")
        print("  python3 cli.py --book all --manual")
        print("Para generar la Arena de Debate entre todos los libros:")
        print("  python3 cli.py --arena")
        return

    if args.arena:
        print("\n🤼 Generando Meta-Skill de Arena de Debate Multilibro...")
        arena_dir = generate_arena_skill(cleaned_clips, output_dir=args.output_dir)
        print(f"🎉 Arena de Debate generada con éxito en: {arena_dir}")

    # Determinar libros a procesar
    books_to_process = []
    if args.book:
        if args.book.lower() == "all":
            books_to_process = books_summary
        else:
            matches = [b for b in books_summary if args.book.lower() in b["title"].lower()]
            if not matches:
                print(f"❌ No se encontró ningún libro que coincida con '{args.book}'")
                return
            books_to_process = matches

    # Parsear mapa de roles si se proporcionó
    role_map_dict = {}
    if args.role_map:
        for pair in args.role_map.split(","):
            if ":" in pair:
                k, v = pair.split(":", 1)
                role_map_dict[k.strip().lower()] = v.strip().lower()

    # Determinar si se debe lanzar el prompt manual por libro
    is_interactive_terminal = sys.stdin.isatty()
    should_do_manual_prompt = False

    if args.manual:
        should_do_manual_prompt = True
    elif books_to_process and args.role is None and not args.role_map and is_interactive_terminal:
        try:
            choice = input("\n❓ ¿Deseas seleccionar el rol manualmente para cada libro uno a uno? [s/N]: ").strip().lower()
            if choice in ["s", "si", "sí", "y", "yes"]:
                should_do_manual_prompt = True
        except (EOFError, KeyboardInterrupt):
            pass

    if books_to_process or (args.manual and not books_to_process):
        targets = books_to_process if books_to_process else books_summary

        if should_do_manual_prompt:
            print("\n🎛️ Modo Clasificación Manual por Libro:")
            print("Asigna un rol a cada libro: [1] auditor | [2] coach | [3] debater | [4] auto (por defecto) | [s] omitir\n")
            for b in targets:
                b_title = b["title"]
                b_clips = [c for c in cleaned_clips if c["book_title"] == b_title]
                auto_role = detect_role_for_book(b_title, b_clips)
                auto_role_title = ROLE_PROMPTS.get(auto_role, ROLE_PROMPTS["coach"])["title"]

                matched_role = None
                for rk, rv in role_map_dict.items():
                    if rk in b_title.lower():
                        matched_role = rv
                        break

                if matched_role:
                    role_choice = matched_role
                    print(f"📖 '{b_title}' -> Aplicando mapa de rol: [{role_choice}]")
                else:
                    try:
                        prompt_msg = f"📖 '{b_title}' (Sugerido: {auto_role_title} [{auto_role}]) -> Rol [1/2/3/4/s] (Enter = {auto_role}): "
                        choice = input(prompt_msg).strip().lower()
                    except (EOFError, KeyboardInterrupt):
                        print("\nOperación cancelada.")
                        break

                    if choice in ["s", "skip", "omitir"]:
                        print(f"  ⏭️ Omitido: {b_title}")
                        continue

                    role_choice = auto_role
                    if choice in ["1", "auditor"]:
                        role_choice = "auditor"
                    elif choice in ["2", "coach"]:
                        role_choice = "coach"
                    elif choice in ["3", "debater"]:
                        role_choice = "debater"
                    elif choice in ["4", "auto"]:
                        role_choice = "auto"

                skill_dir = generate_skill_for_book(
                    b_title, b_clips, role=role_choice, output_dir=args.output_dir
                )
                print(f"  🎉 Skill generada [{role_choice}] en: {skill_dir}")
        else:
            default_role = args.role if args.role else "auto"
            print(f"\n🔨 Generando Skills de IA...")
            for b in targets:
                b_title = b["title"]
                assigned_role = default_role
                for rk, rv in role_map_dict.items():
                    if rk in b_title.lower():
                        assigned_role = rv
                        break

                b_clips = [c for c in cleaned_clips if c["book_title"] == b_title]
                skill_dir = generate_skill_for_book(
                    b_title, b_clips, role=assigned_role, output_dir=args.output_dir
                )
                print(f"🎉 Skill generada [{assigned_role}] en: {skill_dir}")

    if not args.book and not args.arena and not args.manual and not args.role_map and not should_do_manual_prompt:
        print("\n⚠️ Especifica un libro con --book \"Título\", usa --book all para procesar todos, usa --manual (-m) para elegir roles interactivamente, usa --role-map \"Libro:rol\", usa --arena para la Arena de Debate, o usa --list para listar los libros.")
        return

    if not args.no_sync:
        print("\n🔄 Sincronizando con Agentes Multi-LLM (.gemini, .claude, .opencode)...")
        sync_logs = sync_skills()
        for log in sync_logs:
            print(f"  {log}")
        print("✨ Sincronización completada.")


if __name__ == "__main__":
    main()
