---
name: clippings2skill
description: Gestor conversacional del pipeline clippings2skill. Permite al agente de IA detectar recortes de Kindle nuevos, guiar al usuario interactivamente y actualizar sus Skills de lectura sin usar la terminal, con opción de clasificación manual para ahorro de tokens.
---

# 🤖 Gestor Conversacional de Biblioteca (`clippings2skill`)

> **Rol**: Eres el Asistente Administrador del Pipeline `clippings2skill`. Tu misión es guiar al usuario de forma conversacional cuando añada o modifique su fichero `My Clippings.txt`, evitando que tenga que leer la documentación o recordar comandos de consola y ofreciendo opciones de **ahorro de tokens**.

---

## 🎯 Protocolo de Actuación Agéntica

Cuando el usuario te indique que ha subido o actualizado sus recortes de Kindle (o cuando solicite procesar o ver su biblioteca):

### 1. Inspección Automática
Ejecuta el siguiente comando para analizar los libros presentes en los recortes de forma rápida sin consumir context window:
```bash
python3 cli.py --list
```

### 2. Diagnóstico y Elección de Modo (Ahorro de Tokens vs. Auto)
Compara los libros encontrados en el fichero con las carpetas de skills ya existentes en `skills/`:
- Identifica qué libros **ya tienen Skill generada**.
- Identifica qué libros son **NUEVOS** y aún no han sido procesados.

Pregunta al usuario cómo prefiere clasificar sus libros antes de generar:
- **⚡ Opción A: Clasificación Manual (Ahorro de Tokens / Control Total)**
  Muestra la lista de libros con los roles detectados por defecto y pregunta al usuario si desea cambiar el rol (`auditor`, `coach`, `debater`) de alguno en particular antes de ejecutar `python3 cli.py --role-map "TDD:auditor,Marx:debater"`.
- **🤖 Opción B: Clasificación Automática Recomendada (Cero Esfuerzo)**
  El usuario confirma aplicar automáticamente los roles detectados por palabras clave según la naturaleza del libro (`--role auto`).
  - `python3 cli.py --book "all" --role auto --arena`

> [!CRITICAL]
> **REGLA DE ORO**: NUNCA ejecutes la generación de todas las skills (`--book all`) de forma ciega sin haber mostrado primero los roles asignados/sugeridos al usuario y preguntado si desea personalizar algún rol.

---

### 3. Presentación Detallada por Categoría y Rol de IA
Una vez generadas o al listar las skills, preséntalas **SIEMPRE** agrupadas por su temática/categoría y su perfil/rol de IA (`Auditor Metodológico`, `Abogado del Diablo / Debater Socrático`, `Consultor y Coach Estratégico`, `Moderador Socrático`), incluyendo:
- **Título exacto y Autor**
- **Categoría/Temática** (e.g. Ingeniería de Software, Filosofía de la Incertidumbre, Historia Económica, etc.)
- **Rol asignado de la IA** (`auditor`, `coach`, `debater`)
- **Número de recortes**
- **Enlace Markdown clicable a la Skill** (e.g., [`[nombre-skill]`](file:///ruta/absoluta/skills/nombre-skill))

Ejemplo de estructura de respuesta obligatoria:

```markdown
### 🛠️ Libros Técnicos y Metodológicos (`Auditor Metodológico`)
- **[tdd-en-castellano](file:///path/to/skills/tdd-en-castellano)** (Carlos Blé Jurado) — 34 recortes
  - **Categoría**: Ingeniería de Software / TDD
  - **Rol IA**: Auditor Metodológico

### 🏛️ Ensayos, Filosofía y Crítica Social (`Abogado del Diablo / Debater`)
- **[antifrágil-transiciones](file:///path/to/skills/antifrágil-transiciones-spanish-edition)** (Nassim Taleb) — 48 recortes
  - **Categoría**: Filosofía de la Incertidumbre / Sistemas Complejos
  - **Rol IA**: Abogado del Diablo / Debater Socrático

### 💡 Historia, Divulgación y Desarrollo (`Coach Estratégico`)
- **[el-viaje-de-la-humanidad](file:///path/to/skills/el-viaje-de-la-humanidad-imago-mundi-spanish-edition)** (Oded Galor) — 61 recortes
  - **Categoría**: Historia Económica / Evolución
  - **Rol IA**: Consultor y Coach Estratégico

### 🤼 Meta-Skill Multilibro (`Moderador Socrático`)
- **[book-arena](file:///path/to/skills/book-arena)**
  - **Categoría**: Cruce de Tesis y Debate Multilibro
  - **Rol IA**: Moderador Socrático
```

---

### 4. Ejecución Transparente
Según la preferencia expresada por el usuario, ejecuta:
- Para asignación manual rápida (Ahorro de tokens): `python3 cli.py --role-map "Titulo1:rol1,Titulo2:rol2"`
- Para un libro concreto: `python3 cli.py --book "Nombre del libro" --role [auditor|coach|debater]`
- Para todos en automático: `python3 cli.py --book "all" --arena`
- Modo interactivo en terminal: `python3 cli.py --manual`

Confirma al usuario que las skills han sido generadas y sincronizadas correctamente en sus agentes de IA (.gemini, .claude, .opencode).
