<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V17 — Transplante causal cuantizado solo-state

## Pregunta

V16 mostró que unos pocos bits pueden preservar identidad cuando el donante conserva todo su contexto. V17 prueba una condición más fuerte: ¿puede un state recurrente comprimido transferir identidad a un receptor cuya memory y pressure explícitas no contienen información específica del donante?

## Diseño

Se reutilizan seis puntos paramétricos del holdout ciego V12. Cada punto utiliza cuatro protocolos de pares históricos y diez seeds de ruido emparejados.

En la frontera:

- donor A o B aporta state_prev y state;
- memory y pressure del receptor se reemplazan por el midpoint común A/B;
- input externo futuro exactamente cero;
- el state donante se conserva a precisión completa o se cuantiza uniformemente a 1, 2, 3, 4, 6 u 8 bits en [-1, 1].

La identidad se clasifica por affinity frente a referencias de continuación A/B intactas durante los primeros 60 pasos futuros.

## Regla de interpretación

Una accuracy de identidad alta con receptor solo-state demuestra que el estado recurrente puede transferir causalmente identidad histórica sin memory o pressure explícitos específicos del donante. Mantener identidad a 3–4 bits mostraría además que el portador transferible es compacto.

Como estos puntos fueron usados como holdout ciego V12, esto es una réplica/extensión del resultado de transplante causal, no un re-test de los candidatos exactos V10/V11.

Sigue siendo un hallazgo dinámico computacional, no una demostración de consciencia subjetiva.

</details>

<a id="english"></a>

# V17 — Quantized State-Only Causal Transplant

## Question

V16 showed that a few bits can preserve identity when the donor retains its full contextual state. V17 tests the stronger condition: can a compressed recurrent state transfer identity to a receiver whose explicit memory and pressure contain no donor-specific information?

## Design

Six parameter points from the V12 blind holdout are reused. Each point uses four history-pair protocols and ten matched-noise seeds.

At the boundary:
- donor A or B supplies `state_prev` and `state`;
- receiver memory and pressure are replaced by the common A/B midpoint;
- future external input is exactly zero;
- the donor state is either kept full precision or uniformly quantized to 1, 2, 3, 4, 6, or 8 bits over [-1, 1].

Identity is classified by affinity to the intact A/B continuation references over the first 60 future steps.

## Interpretation rule

High identity accuracy under the state-only receiver demonstrates that the recurrent state can causally transfer historical identity without donor-specific explicit memory or pressure. Retention at 3–4 bits would additionally show that the transferable carrier is compact.

Because these parameter points were used as V12 blind holdout points, this is a replication/extension of the causal transplant result rather than a re-test of the exact V10/V11 candidates.

This remains a computational dynamical finding, not a demonstration of subjective consciousness.