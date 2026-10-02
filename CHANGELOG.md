## 2026-10-02 — I5.19 verificado / I5.19 verified

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

- I5.19 repitió I5.17 con semilla independiente **20261019** y aplicó sin cambios el análisis I5.18: 24 réplicas, 24 warmup, 15 ciclos y 20.000 permutaciones.
- Run **37056574657**, artifact **11247979913**; tests **37056574726** y paquete **37056574723** pasaron.
- El efecto bridge ON−OFF medio se replicó en AUC firmada (**-1.39819**, p=0.00030), AUC absoluta (**-0.73065**, p=0.00190) y cambio de acción futura (**-0.11806**, p=0.00110).
- La interacción global fase × bridge volvió a ser no significativa en los tres endpoints.
- Siguiente control: I5.20, especificidad del bridge bajo permutación semántica.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

- I5.19 reran I5.17 with independent seed **20261019** and applied the I5.18 analysis unchanged: 24 replicates, 24 warmup cycles, 15 cycles, and 20,000 permutations.
- Run **37056574657**, artifact **11247979913**; tests **37056574726** and package check **37056574723** passed.
- The average bridge ON−OFF effect replicated for signed AUC (**-1.39819**, p=0.00030), absolute AUC (**-0.73065**, p=0.00190), and future-action change (**-0.11806**, p=0.00110).
- The global phase × bridge interaction was again non-significant for all three endpoints.
- Next control: I5.20, bridge specificity under semantic permutation.

</details>

## 2026-10-02 — I5.18 verificado / I5.18 verified

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

- I5.18 se ejecutó sobre los efectos por réplica congelados de I5.17, sin nuevas trayectorias: **24 réplicas**, **15 ciclos** y **20.000 permutaciones**.
- Run research-lab **37052907187**, artifact **11246744569**; tests **37052907473** y paquete **37052907326** pasaron.
- El efecto bridge ON−OFF medio fue distinto de cero para AUC firmada (**-1.38013**, p=0.00005), AUC absoluta (**-0.52589**, p=0.00290) y cambio de acción futura (**-0.08681**, p=0.00090).
- La interacción global fase × bridge no fue significativa en ninguno de los tres endpoints.
- Se define I5.19 como replicación independiente con protocolo estadístico congelado.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

- I5.18 ran on frozen per-replicate I5.17 bridge effects with no new trajectories: **24 replicates**, **15 cycles**, **20,000 permutations**.
- Research-lab run **37052907187**, artifact **11246744569**; tests **37052907473** and package check **37052907326** passed.
- The mean bridge ON−OFF effect was non-zero for signed AUC (**-1.38013**, p=0.00005), absolute AUC (**-0.52589**, p=0.00290), and future-action change (**-0.08681**, p=0.00090).
- The global phase × bridge interaction was non-significant for all three endpoints.
- I5.19 is now defined as an independent replication with the analysis protocol frozen.

</details>

# Historial de cambios

## 2026-10-02 — I5.17 verificado / I5.17 verified

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

- I5.17 ejecutado y verificado mediante GitHub Actions: run **37047719727**, artifact **11244733803**, commit **578802962b4f37066db95d46567245dcbb9ac83b**.
- 24 réplicas, 24 ciclos de warmup, 15 ciclos experimentales y **180 tests** pasaron.
- Se registró 100% de coincidencia de acción t0 y 100% de coincidencia de distribución de SELF_MODEL.
- El bridge ON−OFF mostró efectos de AUC firmada en los seis lags probados; la simetría absoluta +k/-k no fue significativa.
- El siguiente control propuesto es I5.18: interacción global fase × bridge con corrección por multiplicidad.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

- I5.17 was executed and verified through GitHub Actions: run **37047719727**, artifact **11244733803**, commit **578802962b4f37066db95d46567245dcbb9ac83b**.
- 24 replicates, 24 warmup cycles, 15 experimental cycles, and **180 tests** passed.
- Applied-action match at t0 and SELF_MODEL distribution match were both 100%.
- Bridge ON−OFF produced signed-AUC effects across all six tested lags; absolute +k/-k symmetry was not significant.
- The next proposed control is I5.18: global phase × bridge interaction with multiplicity correction.

</details>


## 2026-10-02 — Consistencia y bilingüismo / Consistency and bilingual layer

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

- Convención única de selección de idioma para documentación humana.
- Reglas explícitas de estructura, nomenclatura, evidencia y limpieza.
- Nuevo AGENTS.md para orientar a agentes sobre la ruta mínima de lectura.
- AI_MAP y llms.txt sincronizados con el estado actual y las rutas reales.
- Workflows one-shot de materialización retirados del CI activo y su procedencia documentada.
- Corrección de referencias obsoletas y de terminología inconsistente.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

- Single language-selection convention for human-facing documentation.
- Explicit structure, naming, evidence, and cleanup rules.
- New AGENTS.md guiding agents through the minimal retrieval route.
- AI_MAP and llms.txt synchronized with current state and real paths.
- One-shot materialization workflows removed from active CI and their provenance documented.
- Obsolete references and inconsistent terminology corrected.

</details>

## Próxima versión — 0.1.0

### Fundamento conceptual
- incorporación del **Manifiesto Matemático del Ser** como documento fundacional;
- incorporación de **TCF — Teoría de Continuidad Fundamental** como segunda capa de formalización dinámica;
- separación explícita entre ontología, ingeniería y evidencia.

### Arquitectura
- organismo persistente con memoria y estado durables;
- ciclos de vigilia y sueño;
- autoobservación y selección de trayectorias;
- puentes semánticos hacia la dinámica interna;
- continuidad entre organismo LLM, estado persistente y dinámica numérica.

### Investigación
- protocolos V47–V67 documentados;
- documentación de los protocolos migrada al español;
- registro experimental consolidado migrado al español;
- resultados positivos, nulos y limitaciones conservados;
- V67 auditado y corregido; resultado nulo bajo ablación semántica total y estado transferido;
- V68 incorporado para medir la persistencia temporal de la huella dinámica generada durante SUEÑO;
- V69 incorporado para probar lectura propia del estado y selección causal de trayectorias;
- V70 incorporado para persistir el lector propio y recuperarlo después de reinicios.

### Repositorio
- README principal en español y reestructurado;
- índice de documentación completado hasta V67;
- fundamentos organizados en `docs/fundamentos/`;
- hoja de ruta pública;
- guía de contribución e issues en español;
- empaquetado Python inicial mediante `pyproject.toml`;
- `CITATION.cff`;
- `.gitignore`;
- workflows de comprobación y laboratorio reproducible.

### Nota
Esta versión sigue siendo una versión de investigación. Los resultados computacionales documentados no constituyen por sí solos evidencia de consciencia fenomenológica o experiencia subjetiva.
