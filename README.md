# 📚 clippings2skill

> **Transforma recortes y subrayados de Kindle (`My Clippings.txt`) en Skills ejecutables de IA Multi-LLM para Google Antigravity, Claude Code y OpenCode.**

---

## 🎯 ¿Qué hace `clippings2skill`?

Este repositorio procesa las notas y pasajes destacados exportados desde tu e-reader Kindle o lector de eBooks, deduplica resaltados parciales y genera automáticamente una **Skill estructurada de IA Agéntica**.

La Skill resultante permite a cualquier modelo de lenguaje (LLM) actuar como un **consultor, auditor o debatiente socrático sobre las temáticas de tus libros**, respaldado por evidencias y citas extraídas de tus lecturas.

---

## 🌟 Características Destacadas

* **🎭 Selección de Rol por Libro (`--role auditor|coach|debater`)**:
  - `auditor`: Evalúa y audita proyectos/código con un checklist de reglas fijas del libro.
  - `coach`: Mentor estratégico para aplicar principios abstractos a situaciones reales.
  - `debater`: Oponente socrático y abogado del diablo que cuestiona tus asunciones.
* **🤼 Arena de Debate Multilibro (`--arena`)**:
  - Genera la Meta-Skill `book-arena` que permite cruzar tesis y hacer debatir a diferentes autores entre sí sobre tus casos reales.
* **🛡️ Principio Innegociable de Juicio Crítico Humano**:
  - Todas las Skills generadas incluyen una regla de oro en su prompt: **La IA jamás debe sustituir el juicio crítico del usuario**. Si la IA detecta falta de comprensión de las bases, advertirá activamente al usuario para que no dimita de su responsabilidad crítica.
* **🤖 Sincronización Multi-LLM**:
  - Sincroniza automáticamente las skills generadas con los entornos de **Google Antigravity** (`.gemini/skills/`), **Claude Code** (`.claude/skills/`) y **OpenCode** (`.opencode/skills/`).

---

## 🔄 Arquitectura del Pipeline

```
              [ 📖 Kindle: My Clippings.txt ]
                             │
                             ▼
                    python3 cli.py
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
[ 📖 Skill por Libro ]  [ 🤼 Arena Multilibro ]  [ 🛡️ Regla de Juicio Crítico ]
 (Auditor/Coach/Debater)  (Debate entre autores)   (No sustituir el pensamiento)
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             ▼
               [ 🤖 Sincronización Multi-LLM ]
                ├── .gemini/skills/   (Google Antigravity)
                ├── .claude/skills/   (Claude Code)
                └── .opencode/skills/ (OpenCode)
```

---

## 🚀 Uso Rápido

### 1. Listar los libros en tus recortes

```bash
python3 cli.py --list
```

### 2. Generar la Skill de un libro con un rol específico

```bash
# Rol de Mentor Estratégico (por defecto)
python3 cli.py --book "The Lean Startup" --role coach

# Rol de Auditor Implacable
python3 cli.py --book "Impact-Driven Growth" --role auditor

# Rol de Abogado del Diablo / Oponente Socrático
python3 cli.py --book "Zero to One" --role debater
```

### 3. Generar la Arena de Debate entre todos los libros

```bash
python3 cli.py --arena
```

---

## 🧪 Pruebas Automatizadas

```bash
python3 -m unittest discover tests
```

---

## 📜 Licencia

Este proyecto está bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.
Consulta el archivo [`LICENSE`](LICENSE) para más detalles.
