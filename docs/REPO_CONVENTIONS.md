# Repository Conventions

<details>
<summary>🇪🇸 Español — abrir</summary>

## Estructura
| Zona | Función |
|---|---|
| src/ | código vivo del runtime |
| tests/ | verificación automatizada |
| experiments/ | protocolos ejecutables |
| docs/ | documentación técnica y protocolos |
| research/ | evidencia histórica y ledger |
| .github/workflows/ | CI activo |

## Regla de una fuente
Un protocolo debe tener una ruta trazable: docs → experiments → tests → workflow → artifact.
No crear copias de la misma fuente solo para cambiar idioma.

## Nombres
- Protocolos: identificador canónico (Vxx, C0.x, I0–I10, Lattice-x).
- Código: snake_case.
- Tests: test_<subject>.py.
- Workflows: <subject>.yml.
- Documentos de protocolo: identificador + descripción estable.

## Limpieza
No borrar archivos únicamente porque sean viejos.
Borrar cuando sean duplicados sin función actual, workflows one-shot ya materializados, scripts que mutan main automáticamente sin necesidad actual o archivos generados/temporales.
Mover/archivar antes que eliminar cuando el archivo tenga valor histórico.

## Idioma
La versión humana usa: 🇪🇸 Español — abrir / 🇺🇸 English — open.
La parte experimental cruda puede conservar un idioma único para proteger reproducibilidad, siempre que la navegación y el protocolo estén disponibles en ambos idiomas.

## Evidencia
Nunca ocultar ni reescribir resultados nulos, endpoints que no separaron, cambios de protocolo, correcciones previas a validación o artifacts de ejecuciones.

</details>

<details>
<summary>🇺🇸 English — open</summary>

## Structure
| Area | Function |
|---|---|
| src/ | live runtime code |
| tests/ | automated verification |
| experiments/ | executable protocols |
| docs/ | technical documentation and protocols |
| research/ | historical evidence and ledger |
| .github/workflows/ | active CI |

## Single-source rule
A protocol should have one traceable route: docs → experiments → tests → workflow → artifact.
Do not create duplicate source files merely to change language.

## Naming
- Protocols: canonical identifiers (Vxx, C0.x, I0–I10, Lattice-x).
- Code: snake_case.
- Tests: test_<subject>.py.
- Workflows: <subject>.yml.
- Protocol documents: identifier + stable description.

## Cleanup
Do not delete files just because they are old.
Delete when they are duplicates with no active function, one-shot materialization workflows already used, scripts that automatically mutate main without a current need, or generated/temporary files.
Archive rather than delete when historical value matters.

## Language
Human-facing documentation uses: 🇪🇸 Español — abrir / 🇺🇸 English — open.
Raw experimental artifacts may remain in one canonical language to protect reproducibility when protocol/navigation exist in both languages.

## Evidence
Never hide or rewrite null results, endpoints that failed to separate, protocol changes, corrections made before validation, or execution artifacts.

</details>

See also docs/LANGUAGE.md and AGENTS.md.