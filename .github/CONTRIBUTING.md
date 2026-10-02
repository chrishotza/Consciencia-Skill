# Contribuir

El proyecto está orientado a investigación reproducible. Las contribuciones deben privilegiar cambios pequeños, medibles y auditables.

## Principios

- documentar la hipótesis antes del experimento;
- mantener controles y condiciones comparables;
- conservar resultados nulos y negativos;
- separar datos, resultados e interpretación;
- agregar pruebas automáticas cuando se incorpora una capacidad nueva;
- evitar modificar un protocolo histórico solo para mejorar su resultado.

## Para un nuevo experimento

1. crear la implementación en `experiments/`;
2. agregar la prueba en `tests/`;
3. agregar el workflow reproducible;
4. documentar el protocolo en `docs/`;
5. registrar el resultado en `research/ORGANISM_RESULT_LEDGER.md`.

## Idioma

La documentación pública del proyecto está migrando al español. Los nombres de código, APIs y protocolos pueden conservar terminología técnica establecida cuando sea necesario.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Contributing

The project is oriented toward reproducible research. Contributions should favor changes that are small, measurable, and auditable.

## Principles

- document the hypothesis before the experiment;
- keep controls and conditions comparable;
- preserve null and negative results;
- separate data, results, and interpretation;
- add automated tests when a new capability is introduced;
- avoid modifying a historical protocol merely to improve its result.

## For a new experiment

1. create the implementation under `experiments/`;
2. add the test under `tests/`;
3. add the reproducible workflow;
4. document the protocol under `docs/`;
5. record the result in `research/ORGANISM_RESULT_LEDGER.md`.

## Language

The public documentation is bilingual using the repository's language-selection convention in `docs/LANGUAGE.md`. Code names, APIs, and established technical protocol terminology may remain unchanged when necessary for reproducibility.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
