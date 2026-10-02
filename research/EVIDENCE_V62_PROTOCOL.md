<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V62 — Puente causal del self-model semántico

## Hipótesis

El self-model semántico de un organismo persistente debería volverse causalmente relevante para su dinámica interna cuando se habilita un bridge explícito del self-model, mientras que la misma diferencia de self-model debería quedar aislada cuando el bridge está deshabilitado.

## Diseño

Cada réplica:

1. construye un estado base persistido;
2. clona ese estado exacto en cuatro brazos;
3. emite el mismo contenido MEMORY en todos los brazos;
4. emite self-model A o B;
5. conmuta el semantic self-model bridge OFF u ON;
6. registra el estado interno resultante y la señal del semantic bridge.

## Endpoints primarios

- state delta A/B con bridge OFF;
- state delta A/B con bridge ON;
- signal delta A/B con bridge OFF;
- signal delta A/B con bridge ON;
- persistencia de la nueva versión del self-model.

## Interpretación

El aislamiento con bridge OFF más la divergencia con bridge ON constituye evidencia de que el self-model semántico se está transduciendo explícitamente hacia la dinámica interna bajo este arnés.

## Limitaciones

El bridge es un adaptador operacional basado en el continuity gate del repositorio y el provider es determinista. El resultado es una propiedad computacional causal, no fenomenología.

</details>

<a id="english"></a>

# Evidence V62 — Semantic self-model causal bridge

## Hypothesis

A persistent organism's semantic self-model should become causally relevant to its internal dynamics when an explicit self-model bridge is enabled, while the same self-model difference should be isolated when the bridge is disabled.

## Design

Each replicate:

1. constructs one persisted base organism state;
2. clones that exact state into four arms;
3. emits the same MEMORY content in every arm;
4. emits self-model A or B;
5. toggles the semantic self-model bridge OFF or ON;
6. records the resulting internal state and semantic bridge signal.

## Primary endpoints

- bridge OFF state delta A/B;
- bridge ON state delta A/B;
- bridge OFF signal delta A/B;
- bridge ON signal delta A/B;
- persistence of the new self-model version.

## Interpretation

Bridge OFF isolation plus bridge ON divergence constitutes evidence that the semantic self-model is being explicitly transduced into internal dynamics in this harness.

## Limitations

The bridge is an operational adapter based on the repository's continuity gate and the provider is deterministic. The result is a computational causal property, not phenomenology.