# 📚 clippings2skill

> **Transforma recortes y subrayados de Kindle (`My Clippings.txt`) en Skills ejecutables de IA Multi-LLM para Google Antigravity, Claude Code y OpenCode.**

---

## 🎯 ¿Qué hace `clippings2skill`?

Este repositorio procesa las notas y pasajes destacados exportados desde tu e-reader Kindle o lector de eBooks, deduplica resaltados parciales y genera automáticamente una **Skill estructurada de IA Agéntica**.

La Skill resultante permite a cualquier modelo de lenguaje (LLM) actuar como un **consultor, auditor o debatiente socrático sobre las temáticas de tus libros**, respaldado por evidencias y citas extraídas de tus lecturas.

---

## ⚖️ Descargo de Responsabilidad Legal (Disclaimer)

> [!WARNING]
> **`clippings2skill` es una herramienta técnica local para uso estrictamente personal.**
> 
> * **Sin Contenido Protegido**: Este repositorio no incluye ni distribuye textos o libros protegidos por derechos de autor (*copyright*).
> * **Uso Personal**: Las Skills generadas a partir de tus recortes son únicamente para tu estudio personal y uso privado dentro de tus propios agentes de IA.
> * **Privacidad por Diseño**: Por defecto, `.gitignore` ignora todas las skills generadas (`skills/*`) para evitar que subas accidentalmente a GitHub resúmenes de libros con derechos de autor. Consulta [`DISCLAIMER.md`](DISCLAIMER.md) para más detalles.

---

## 🌟 Características Destacadas

* **🤖 Meta-Skill Interactivas "Cero Terminal" (`skills/clippings2skill`)**:
  - Simplemente arrastra tu `My Clippings.txt` y pídele a tu Agente de IA: *"Actualiza mi biblioteca de recortes"*. El agente detectará nuevos libros y gestionará la generación conversacionalmente.
* **🎭 Selección de Rol por Libro (`--role auditor|coach|debater`)**:
  - `auditor`: Evalúa y audita proyectos/código con un checklist de reglas fijas del libro.
  - `coach`: Mentor estratégico para aplicar principios abstractos a situaciones reales.
  - `debater`: Oponente socrático y abogado del diablo que cuestiona tus asunciones.
* **🤼 Arena de Debate Multilibro (`--arena`)**:
  - Genera la Meta-Skill `book-arena` que permite cruzar tesis y hacer debatir a diferentes autores entre sí sobre tus casos reales.
* **🛡️ Principio Innegociable de Juicio Crítico Humano**:
  - Todas las Skills generadas incluyen una regla de oro en su prompt: **La IA jamás debe sustituir el juicio crítico del usuario**.
* **🤖 Sincronización Multi-LLM Automática**:
  - Conecta automáticamente tus skills con **Google Antigravity** (`.gemini/skills/`), **Claude Code** (`.claude/skills/`) y **OpenCode** (`.opencode/skills/`).

---

## 📂 ¿Cómo Usar o Exportar las Skills Generadas?

Cuando generas las skills de tus libros leídos:

1. **Uso Local Automático**: El comando `cli.py` (o la meta-skill interactiva) sincroniza tus skills mediante symlinks a tus carpetas locales `.gemini/skills/`, `.claude/skills/` y `.opencode/skills/`. Tu agente de IA podrá utilizarlas de inmediato sin hacer nada más.
2. **Exportar a otros Proyectos o Equipos**: Si deseas usar la skill de un libro en otro lugar, simplemente copia la carpeta `skills/<book-slug>/` a la carpeta de skills de tu otro proyecto o a tu directorio global de usuario (ej. `~/.gemini/skills/` o `~/.claude/skills/`).

---

## 🚀 Uso en Consola

```bash
# Listar los libros en tus recortes
python3 cli.py --list

# Generar la Skill de un libro con un rol específico
python3 cli.py --book "The Lean Startup" --role coach

# Generar la Arena de Debate entre todos los libros
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
