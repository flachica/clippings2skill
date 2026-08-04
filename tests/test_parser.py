"""
test_parser.py
==============
Pruebas unitarias completas con unittest estándar.
"""

import os
import unittest
import tempfile
import shutil
from clippings2skill.parser import parse_clippings_file, get_books_summary
from clippings2skill.deduplicator import deduplicate_clips
from clippings2skill.generator import (
    generate_skill_for_book,
    generate_arena_skill,
    slugify,
    CRITICAL_JUDGMENT_RULE,
)


class TestClippings2Skill(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_slugify(self):
        self.assertEqual(slugify("The Lean Startup"), "the-lean-startup")
        self.assertEqual(
            slugify("Impact-Driven Growth (Carlos Iglesias)"),
            "impact-driven-growth-carlos-iglesias",
        )

    def test_parse_and_deduplicate(self):
        sample_path = os.path.join(self.temp_dir, "test_clippings.txt")
        sample_content = """Book A (Author A)
- Tu subrayado en la página 10 | Posición 100 | Añadido el lunes

Hola mundo
==========
Book A (Author A)
- Tu subrayado en la página 10 | Posición 102 | Añadido el lunes

Hola mundo maravilloso
==========
Book B (Author B)
- Tu subrayado en la página 5 | Posición 50 | Añadido el martes

Segundo libro
==========
"""
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        clips = parse_clippings_file(sample_path)
        self.assertEqual(len(clips), 3)

        unique = deduplicate_clips(clips)
        self.assertEqual(len(unique), 2)

        books = get_books_summary(unique)
        self.assertEqual(len(books), 2)

    def test_generate_skill_roles_and_critical_rule(self):
        clips = [
            {
                "book_title": "Test Book",
                "author": "Test Author",
                "page": 1,
                "meta": "Page 1",
                "content": "Sample quote content",
            }
        ]

        for role in ["auditor", "coach", "debater"]:
            output_dir = os.path.join(self.temp_dir, f"skills_{role}")
            skill_dir = generate_skill_for_book(
                "Test Book", clips, role=role, output_dir=output_dir
            )

            skill_md_path = os.path.join(skill_dir, "SKILL.md")
            self.assertTrue(os.path.exists(skill_md_path))
            self.assertTrue(os.path.exists(os.path.join(skill_dir, "dataset.json")))

            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check critical judgment rule
                self.assertIn("Juicio Crítico Humano", content)
                self.assertIn("Un humano nunca debe dimitir de su juicio crítico", content)

    def test_generate_arena(self):
        clips = [
            {
                "book_title": "Book 1",
                "author": "Author 1",
                "page": 10,
                "meta": "Page 10",
                "content": "Quote 1",
            },
            {
                "book_title": "Book 2",
                "author": "Author 2",
                "page": 20,
                "meta": "Page 20",
                "content": "Quote 2",
            },
        ]

        output_dir = os.path.join(self.temp_dir, "skills_arena")
        arena_dir = generate_arena_skill(clips, output_dir=output_dir)

        skill_md_path = os.path.join(arena_dir, "SKILL.md")
        self.assertTrue(os.path.exists(skill_md_path))
        self.assertTrue(os.path.exists(os.path.join(arena_dir, "dataset.json")))

        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Arena de Debate Socrático", content)
            self.assertIn("Juicio Crítico Humano", content)


if __name__ == "__main__":
    unittest.main()
