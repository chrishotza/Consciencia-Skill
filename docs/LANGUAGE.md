# Idioma / Language

Skill-Conscious usa el mismo patrón de selección lingüística en su documentación pública:

- 🇪🇸 **Español** — versión principal para usuarios hispanohablantes.
- 🇺🇸 **English** — traducción completa dentro de un bloque desplegable cuando el documento también debe conservar una versión española, o viceversa.

## Regla

Los nombres de código, módulos, APIs, variables, protocolos, métricas, hashes, JSON, YAML y comandos se conservan literalmente. Solo se traducen las capas destinadas a lectura humana.

Los resultados científicos no se modifican para hacerlos sonar mejor en otro idioma. Las cifras, condiciones, controles, p-values, límites y resultados nulos deben permanecer idénticos.

## Cobertura

La capa pública y operativa debe ser bilingüe:

- README y navegación;
- instalación y uso;
- método y alcance científico;
- contribución;
- Skill para agentes;
- arquitectura e infraestructura;
- índice y fundamentos;
- resúmenes de investigación.

Los artefactos experimentales crudos, tests, fixtures y archivos de datos mantienen sus identificadores canónicos para preservar reproducibilidad. Sus entradas de navegación deben poder entenderse en ambos idiomas.

## Patrón de selección

Usar el mismo estilo que el README:

<details>
<summary>🇪🇸 Español — abrir</summary>

Contenido en español.

</details>

<details>
<summary>🇺🇸 English — open</summary>

English content.

</details>

Este patrón evita mantener dos rutas de archivo para el mismo documento y hace que los enlaces internos sigan siendo estables.


<a id="espanol"></a>

# Idioma / Language

Skill-Conscious usa un selector único en **todos los archivos Markdown legibles por humanos**, incluidos documentos activos, protocolos históricos, evidencia y fundamentos.

- 🇪🇸 **Español — abrir**
- 🇺🇸 **English — open**

## Regla de enlaces

Toda navegación que ofrezca una elección de idioma debe apuntar al anclaje correspondiente del mismo Markdown:

- Español → #espanol
- English → #english

El README nunca debe llevar desde su sección española a una sección inglesa del documento destino, ni viceversa.

## Regla de traducción

Los nombres de código, módulos, APIs, variables, protocolos, métricas, hashes, JSON, YAML y comandos se conservan literalmente.

Las capas destinadas a lectura humana se traducen completamente. No se reemplaza una traducción por un resumen cuando el documento contiene información experimental, histórica o metodológica.

Los números, condiciones, controles, p-values, límites, seeds y resultados nulos deben permanecer idénticos.

## Código, datos y artifacts

Los archivos Python, JSON, YAML, fixtures, bases SQLite y artifacts generados no se traducen.

Sus identificadores sí deben conservarse literalmente en ambos idiomas.

## Patrón

Cada Markdown bilingüe usa:

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

Contenido completo en español.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

Full English content.

</details>

La traducción debe conservar la organización y el nivel de detalle de la fuente.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Language

Skill-Conscious uses one language-selection convention across **all human-readable Markdown files**, including active documents, historical protocols, evidence, and foundations.

- 🇪🇸 **Español — abrir**
- 🇺🇸 **English — open**

## Link rule

Any navigation that offers a language choice must target the corresponding anchor in the same Markdown:

- Spanish → #espanol
- English → #english

The README must never send a user from its Spanish section to an English section of the target document, or vice versa.

## Translation rule

Code names, modules, APIs, variables, protocols, metrics, hashes, JSON, YAML, and commands remain literal.

Human-facing layers are translated completely. A translation must not be replaced by a summary when the document contains experimental, historical, or methodological information.

Numbers, conditions, controls, p-values, limits, seeds, and null results remain identical.

## Code, data, and artifacts

Python, JSON, YAML, fixtures, SQLite databases, and generated artifacts are not translated.

Their identifiers remain literal in both languages.

## Pattern

Every bilingual Markdown file uses:

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

Contenido completo en español.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

Full English content.

</details>

The translation must preserve the source document's organization and level of detail.

</details>