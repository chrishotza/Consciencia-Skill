# V20b — Evidence: Corrected Delayed State Restoration

## GitHub validation

- Workflow: state-recovery-v20b
- Run: 36779259112
- Result: SUCCESS
- Artifact: 11126668057

## Result

The corrected post-restoration metric does **not** show a consistent recovery of donor identity after delayed state restoration.

| Delay | Identity accuracy | Mean affinity |
|---:|---:|---:|
| 0 | 51.96% | +0.2890 |
| 5 | 60.89% | -0.1214 |
| 10 | 46.07% | -0.2416 |
| 20 | 63.21% | -0.1493 |
| 40 | 45.18% | -0.2578 |
| 80 | 63.21% | -0.1554 |

The signal is unstable across delays and its pooled affinity changes sign. The baseline control converges toward chance at long delay (50.0% at delay 80), but the critical blind points do not exhibit monotonic donor recovery after restoration.

## Decision

V20b is treated as a **negative/null result** for the hypothesis that delayed re-injection of the boundary donor state, while retaining the receiver's post-lesion memory and pressure, reliably restores the original trajectory identity.

V20 original is also excluded from evidence because its metric mixed pre-restoration and post-restoration intervals.

## Scientific value

This null result constrains the interpretation of V15–V19: causal state lesion and immediate state transfer are supported, but that does not imply arbitrary late restoration can reconstruct the prior trajectory after intervening dynamics have evolved.

That distinction is useful: the recurrent state is causally relevant at the boundary, but its information is not necessarily sufficient for recovery after an uncontrolled temporal displacement.

This remains a computational dynamical result and does not establish subjective consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V20b — Evidencia: restauración corregida y demorada del estado

## Validación GitHub

- Workflow: state-recovery-v20b
- Run: 36779259112
- Result: SUCCESS
- Artifact: 11126668057

## Resultado

La métrica corregida posterior a la restauración **no** muestra recuperación consistente de la identidad donante después de una restauración demorada del estado.

| Delay | Identity accuracy | Mean affinity |
|---:|---:|---:|
| 0 | 51.96% | +0.2890 |
| 5 | 60.89% | -0.1214 |
| 10 | 46.07% | -0.2416 |
| 20 | 63.21% | -0.1493 |
| 40 | 45.18% | -0.2578 |
| 80 | 63.21% | -0.1554 |

La señal es inestable entre delays y su affinity agrupada cambia de signo. El baseline converge hacia el azar con delay largo (50.0% en delay 80), pero los puntos ciegos critical no muestran recuperación monótona del donante tras la restauración.

## Decisión

V20b se trata como **resultado negativo/nulo** para la hipótesis de que reinyectar tardíamente el state donante de frontera, manteniendo memory y pressure del receptor después de la lesión, restaura de forma fiable la identidad de la trayectoria original.

V20 original también se excluye de la evidencia porque su métrica mezclaba intervalos pre y post restauración.

## Valor científico

Este resultado nulo limita la interpretación de V15–V19: la lesión causal del estado y la transferencia inmediata de state están respaldadas, pero eso no implica que cualquier restauración tardía pueda reconstruir la trayectoria anterior después de que la dinámica haya evolucionado de manera no controlada.

La distinción es útil: el estado recurrente es causalmente relevante en la frontera, pero su información no es necesariamente suficiente para recuperar la trayectoria después de un desplazamiento temporal no controlado.

Sigue siendo un resultado dinámico computacional y no establece consciencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V20b — Evidence: Corrected Delayed State Restoration

## GitHub validation

- Workflow: state-recovery-v20b
- Run: 36779259112
- Result: SUCCESS
- Artifact: 11126668057

## Result

The corrected post-restoration metric does **not** show consistent donor-identity recovery after delayed state restoration.

| Delay | Identity accuracy | Mean affinity |
|---:|---:|---:|
| 0 | 51.96% | +0.2890 |
| 5 | 60.89% | -0.1214 |
| 10 | 46.07% | -0.2416 |
| 20 | 63.21% | -0.1493 |
| 40 | 45.18% | -0.2578 |
| 80 | 63.21% | -0.1554 |

The signal is unstable across delays and pooled affinity changes sign. Baseline approaches chance at long delay (50.0% at delay 80), but critical blind points do not show monotonic donor recovery after restoration.

## Decision

V20b is treated as a **negative/null result** for the hypothesis that delayed reinjection of boundary donor state, while retaining receiver memory and pressure after lesion, reliably restores original trajectory identity.

Original V20 is also excluded from evidence because its metric mixed pre- and post-restoration intervals.

## Scientific value

The null result constrains interpretation of V15–V19: causal state lesion and immediate state transfer are supported, but arbitrary late restoration need not reconstruct the prior trajectory after uncontrolled intervening dynamics.

The recurrent state is causally relevant at the boundary, but its information is not necessarily sufficient for recovery after temporal displacement.

This remains a computational dynamical result and does not establish subjective consciousness.

</details>