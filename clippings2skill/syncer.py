"""
syncer.py
=========
Gestor de sincronización Multi-LLM Agent (.gemini/skills, .claude/skills, .opencode/skills).
"""

import os
import sys
import shutil
import pathlib
from typing import List

TARGET_DIRS = [".gemini/skills", ".claude/skills", ".opencode/skills"]
SOURCE_DIR = "skills"


def sync_skills(repo_root: str = ".") -> List[str]:
    root_path = pathlib.Path(repo_root).resolve()
    source_path = root_path / SOURCE_DIR

    if not source_path.exists():
        return [f"⚠️ Advertencia: La carpeta '{SOURCE_DIR}' no existe aún. Nada que sincronizar."]

    skill_folders = [d for d in source_path.iterdir() if d.is_dir()]
    logs = []

    for target_rel in TARGET_DIRS:
        target_base = root_path / target_rel
        target_base.mkdir(parents=True, exist_ok=True)

        for skill_dir in skill_folders:
            skill_name = skill_dir.name
            target_link = target_base / skill_name
            rel_source = os.path.relpath(skill_dir, target_base)

            if target_link.is_symlink():
                current_target = os.readlink(target_link)
                if current_target == rel_source:
                    logs.append(f"✅ [OK Symlink] {target_rel}/{skill_name} -> {rel_source}")
                    continue
                else:
                    target_link.unlink()
            elif target_link.exists():
                if target_link.is_dir():
                    shutil.rmtree(target_link)
                else:
                    target_link.unlink()

            try:
                os.symlink(rel_source, target_link, target_is_directory=True)
                logs.append(f"🔗 [Creado Symlink] {target_rel}/{skill_name} -> {rel_source}")
            except (OSError, NotImplementedError):
                shutil.copytree(skill_dir, target_link)
                logs.append(f"📋 [Copia Fallback Windows] {target_rel}/{skill_name} <- {skill_dir}")

    return logs
