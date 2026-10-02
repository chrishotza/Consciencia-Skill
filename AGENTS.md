# Skill-Conscious — Agent Instructions

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Regla principal

Tratá este repositorio como un laboratorio de software e investigación reproducible, no como un único prompt.

### Ruta de lectura
1. AI_INDEX.md
2. AI_MAP.json
3. research/ORGANISM_RESULT_LEDGER.md
4. protocolo exacto en docs/
5. experimento correspondiente en experiments/
6. test correspondiente en tests/
7. workflow solo cuando CI sea relevante

No recorras recursivamente todo el repositorio.

## Tres clases de contenido

**Activo** — arquitectura, protocolos y workflows que siguen en desarrollo.
**Histórico** — V47–V80, C0.x y experimentos anteriores conservados para reproducibilidad.
**Archivado** — scripts o workflows de migración/materialización de una sola ocasión que ya no participan del CI activo. Su procedencia debe quedar documentada, pero no necesitan ejecutarse.

## Regla de idioma
La documentación orientada a humanos usa:
- 🇪🇸 Español — abrir
- 🇺🇸 English — open

Los identificadores de código, nombres de módulos, APIs, hashes, métricas, seeds, nombres de protocolos y artefactos no se traducen.

## Regla científica
Separá siempre: fuente teórica; implementación; medición; resultado; interpretación; hipótesis.
Los resultados nulos permanecen nulos. No se modifica un protocolo histórico para mejorar su resultado.

## Regla de cambios
Cuando modifiques una capacidad: cambia primero la implementación mínima; agrega o ajusta el test; actualiza el experimento; actualiza el protocolo; actualiza el workflow solo si hace falta; actualiza el índice y el ledger cuando corresponda.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Main rule
Treat this repository as a reproducible software and research laboratory, not as a single prompt.

### Reading route
1. AI_INDEX.md
2. AI_MAP.json
3. research/ORGANISM_RESULT_LEDGER.md
4. exact protocol in docs/
5. matching experiment in experiments/
6. matching test in tests/
7. workflow only when CI behavior matters

Do not recursively crawl the entire repository.

## Three content classes
**Active** — architecture, protocols, and workflows still under development.
**Historical** — V47–V80, C0.x, and earlier experiments preserved for reproducibility.
**Archived** — one-shot migration/materialization scripts or workflows that no longer participate in active CI. Their provenance should remain documented, but they do not need to execute.

## Language rule
Human-facing documentation uses:
- 🇪🇸 Español — abrir
- 🇺🇸 English — open

Code identifiers, module names, APIs, hashes, metrics, seeds, protocol IDs, and artifact names are not translated.

## Scientific rule
Always separate: theoretical source; implementation; measurement; result; interpretation; hypothesis.
Null results remain null. Do not modify historical protocols to improve their result.

## Change rule
When modifying a capability: change the smallest relevant implementation; add or update the test; update the experiment; update the protocol; update CI only when necessary; update indexes and the ledger when applicable.

</details>

See also docs/LANGUAGE.md and docs/REPO_CONVENTIONS.md.