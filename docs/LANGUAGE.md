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
