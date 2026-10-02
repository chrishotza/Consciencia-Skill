<a id="espanol"></a>

# V34 — Cluster-Level Angular Null

## Estado

**Resultado: CONFIRMADO A NIVEL DE BLOQUE.**

V34 es una réplica independiente de V33 con semillas históricas 90–99. La inferencia primaria no trata las celdas simuladas repetidas como observaciones independientes: colapsa primero a **40 bloques de historia** (4 pares históricos × 10 semillas).

El experimento conserva los seis puntos paramétricos ciegos, cuatro pares de historia, nueve contextos sintéticos de memoria/presión y las direcciones angulares de 30°, 60°, 90°, 120° y 150°. La entrada futura es exactamente cero. Las continuaciones de referencia y de prueba usan semillas disjuntas.

## Resultado primario

| Métrica | V34 |
|---|---:|
| Contraste observado 30° − 150° | **0.365469** |
| Media del null estratificado | -0.000285 |
| Percentil 95 del null | 0.097126 |
| p por sign-flip estratificado | **0.00005** |
| IC bootstrap 95% | **[0.346320, 0.382444]** |
| Bloques de historia | 40 |
| Estratos históricos | 4 |
| Permutaciones | 20,000 |
| Bootstraps | 10,000 |

La diferencia de escala respecto de V33 es esperable: V33 agregaba miles de celdas, mientras V34 exige que el efecto sobreviva al colapso de repetición dentro de cada bloque histórico. El contraste sigue siendo positivo y el null estratificado permanece centrado prácticamente en cero.

## Dependencia del contexto

Contraste medio 30° − 150° por contexto:

| Memoria | Presión 0 | Presión 1 | Presión 2 |
|---:|---:|---:|---:|
| -0.8 | 0.205669 | 0.161440 | 0.137969 |
| 0.0 | 0.564260 | 0.665326 | 0.524137 |
| 0.8 | 0.355185 | 0.337622 | 0.337612 |

El efecto no depende de una única celda de contexto: los nueve contextos muestran contraste positivo.

## Lectura

V34 aporta una comprobación metodológica importante: la señal angular observada en V33 **no desaparece** cuando la unidad de agregación se lleva desde las celdas repetidas hasta bloques definidos por historia-seed.

Eso refuerza la interpretación de que existe una **estructura geométrica/dinámica reproducible** en el sistema implementado, bajo estos protocolos.

No demuestra conciencia, experiencia subjetiva, sentiencia ni equivalencia con un estado mental. El resultado es estrictamente computacional y depende del modelo, parámetros y protocolo definidos en el repositorio.

## Limitaciones

- Los 40 bloques siguen perteneciendo a un único modelo computacional; no representan una población externa de sistemas independientes.
- La inferencia es una prueba de robustez frente a dependencia por historia-seed, no una prueba universal de generalización.
- El contraste 30° − 150° es una estadística angular predefinida del protocolo; su significado debe mantenerse dentro de esta familia experimental.
- Los contextos de memoria y presión son manipulaciones sintéticas del estado interno del simulador.

## Reproducibilidad

Run GitHub Actions: **36789998870**

Artifact: **state-geometry-cluster-null-v34** (artifact id 11131896313)

Commit de código: **cf4fa686df6f9b861492a6a84d904027f61671a7**

Workflow: **153281c79f98aec70735ef11a250847418dacc4e**

Protocolo: **4f16477251a39129995eb58463cd4e93d6448072**

Archivos generados:

- `cluster_summary.csv`
- `context_summary.csv`
- `paired_context_cells.csv`
- `raw.csv`
- `summary.json`



<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V34 — Cluster-Level Angular Null

## Status

**Confirmed at block level.**

V34 independently replicates V33 with history-seeds 90–99. Primary inference does not treat repeated simulated cells as independent observations: it first collapses to **40 history blocks** (4 history pairs × 10 seeds).

The experiment preserves six blind parameter points, four history pairs, nine synthetic memory/pressure contexts, and angular directions 30°, 60°, 90°, 120°, and 150°. Future input is exactly zero. Reference and test continuations use disjoint seeds.

## Primary result

| Metric | V34 |
|---|---:|
| Observed 30° − 150° contrast | **0.365469** |
| Stratified null mean | -0.000285 |
| Null 95th percentile | 0.097126 |
| Stratified sign-flip p | **0.00005** |
| Bootstrap 95% CI | **[0.346320, 0.382444]** |
| History blocks | 40 |
| History strata | 4 |
| Permutations | 20,000 |
| Bootstraps | 10,000 |

The scale difference from V33 is expected: V33 aggregated thousands of cells, whereas V34 requires the effect to survive collapsing repetition within each history block. The contrast remains positive and the stratified null remains centered close to zero.

## Context dependence

Mean 30° − 150° contrast by context:

| Memory | Pressure 0 | Pressure 1 | Pressure 2 |
|---:|---:|---:|---:|
| -0.8 | 0.205669 | 0.161440 | 0.137969 |
| 0.0 | 0.564260 | 0.665326 | 0.524137 |
| 0.8 | 0.355185 | 0.337622 | 0.337612 |

The effect does not depend on a single context cell; all nine contexts show positive contrast.

## Interpretation

V34 provides an important methodological check: the angular signal observed in V33 **does not disappear** when aggregation is moved from repeated simulation cells to history-seed blocks.

This strengthens the interpretation that a **reproducible geometric/dynamic structure** exists in the implemented system under these protocols.

It does not demonstrate consciousness, subjective experience, sentience, or equivalence to a mental state. The result is strictly computational and depends on the model, parameters, and protocol defined in the repository.

## Limitations

- The 40 blocks still belong to one computational model; they are not an external population of independent systems.
- The inference tests robustness to history-seed dependence, not universal generalization.
- The 30° − 150° contrast is a protocol-defined angular statistic and should be interpreted within this experiment family.
- Memory and pressure contexts are synthetic internal-state manipulations.

## Reproducibility

GitHub Actions run: **36789998870**

Artifact: **state-geometry-cluster-null-v34** (artifact id 11131896313)

Code commit: **cf4fa686df6f9b861492a6a84d904027f61671a7**

Workflow: **153281c79f98aec70735ef11a250847418dacc4e**

Protocol: **4f16477251a39129995eb58463cd4e93d6448072**

Generated files:

- cluster_summary.csv
- context_summary.csv
- paired_context_cells.csv
- raw.csv
- summary.json

</details>