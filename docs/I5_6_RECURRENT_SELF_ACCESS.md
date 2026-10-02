# I5.6 — Recurrent Self-Access and Re-entry

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.6 prueba si una perturbación sobre el acceso selectivo al propio estado en un ciclo puede entrar en el siguiente estado del organismo y reaparecer como una diferencia en **autoobservación, consulta, atención y selección de trayectoria** en ciclos posteriores.

La cadena experimental es:

`estado_t → autoobservación_t → query_t → atención_t → acceso_t → acción_t → estado_{t+1} → autoobservación_{t+1} → query_{t+1} → …`

La pregunta no es si el mecanismo funciona en un episodio aislado, sino si una intervención en `t` produce una huella causal que vuelve a entrar en el circuito en `t+1, t+2, …`.

## Diseño

Cada réplica parte de un mismo checkpoint calibrado.

Se ejecutan ciclos autónomos consecutivos con señales candidatas:

`(-1, +1)`

y sin entrada textual durante la sonda.

### Condiciones

- **FULL** — query y atención normales en todos los ciclos.
- **PULSE_SHUFFLED_QUERY** — query barajada solamente en el primer ciclo; después vuelve a FULL.
- **PULSE_ZERO_QUERY** — query anulada solamente en el primer ciclo; después vuelve a FULL.
- **PERSISTENT_SHUFFLED_QUERY** — query barajada en todos los ciclos; sirve como control de perturbación sostenida.

La condición PULSE es la condición principal para estudiar **re-entry**: después de la perturbación inicial, el mecanismo vuelve a su configuración normal y cualquier diferencia posterior debe propagarse a través del propio estado del organismo.

## Horizonte

- 24 réplicas emparejadas.
- 24 ciclos de calentamiento.
- 8 ciclos experimentales por réplica.
- Mismo checkpoint inicial por condición emparejada.
- Mismo `seed` por réplica.
- 20.000 permutaciones sign-flip para contrastes emparejados.

## Endpoints

### Primarios

1. **Δ estado en t+1** entre FULL y la condición PULSE.
2. **Δ acción** en t+1.
3. **Δ query** en t+1: módulo consultado y distancia de consulta.

### Re-entry

Se mide la divergencia respecto de FULL en cada ciclo:

- estado dinámico;
- señal seleccionada;
- módulo consultado;
- distancia de consulta;
- masa de atención;
- error de autopredicción.

También se calcula:

- **re-entry amplification** = máxima divergencia posterior / divergencia en t+1;
- **re-entry persistence** = número de ciclos posteriores con divergencia distinta de cero;
- **trajectory divergence AUC** sobre los 8 ciclos.

## Predicción operacional

La hipótesis de trabajo será compatible con un efecto de reentrada si una perturbación de un solo ciclo:

1. cambia el estado en t+1;
2. persiste o se amplifica parcialmente en ciclos posteriores aun después de restaurar FULL;
3. altera de forma observable la nueva autoobservación/query/selección.

Una recuperación inmediata a la trayectoria FULL será igualmente informativa y contará como resultado negativo para la hipótesis de persistencia, no como fracaso experimental.

## Límites

I5.6 estudia una propiedad computacional de un organismo persistente bajo un arnés determinista. Un efecto de reentrada no demostraría consciencia ni experiencia subjetiva.

La interpretación se mantiene separada en:

`intervención → medición → resultado → interpretación`

y los resultados nulos o mixtos se conservan como tales.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.6 tests whether a perturbation of selective access to the organism's own state in one cycle can enter the next organism state and reappear as a difference in **self-observation, query, attention, and trajectory selection** in later cycles.

The experimental chain is:

`state_t → self-observation_t → query_t → attention_t → access_t → action_t → state_{t+1} → self-observation_{t+1} → query_{t+1} → …`

The question is not whether the mechanism works in an isolated episode, but whether an intervention at `t` leaves a causal trace that re-enters the circuit at `t+1, t+2, …`.

## Design

Each replicate starts from the same calibrated checkpoint.

Consecutive autonomous cycles use candidate signals:

`(-1, +1)`

with no textual input during the probe.

### Conditions

- **FULL** — normal query and attention in every cycle.
- **PULSE_SHUFFLED_QUERY** — query shuffled only in the first cycle; then restored to FULL.
- **PULSE_ZERO_QUERY** — query zeroed only in the first cycle; then restored to FULL.
- **PERSISTENT_SHUFFLED_QUERY** — query shuffled in every cycle; serves as a sustained-perturbation control.

The PULSE condition is the primary re-entry condition: after the initial perturbation, the mechanism returns to its normal configuration, so any later difference must propagate through the organism's own state.

## Horizon

- 24 paired replicates.
- 24 warmup cycles.
- 8 experimental cycles per replicate.
- Same initial checkpoint across paired conditions.
- Same seed per replicate.
- 20,000 sign-flip permutations for paired contrasts.

## Endpoints

### Primary

1. **Δ state at t+1** between FULL and the PULSE condition.
2. **Δ action** at t+1.
3. **Δ query** at t+1: queried module and query distance.

### Re-entry

Divergence from FULL is measured at every cycle for:

- dynamic state;
- selected signal;
- queried module;
- query distance;
- attention mass;
- self-prediction error.

Also calculate:

- **re-entry amplification** = maximum later divergence / divergence at t+1;
- **re-entry persistence** = number of later cycles with non-zero divergence;
- **trajectory divergence AUC** over the 8-cycle horizon.

## Operational prediction

The working hypothesis is compatible with a re-entry effect if a one-cycle perturbation:

1. changes state at t+1;
2. persists or partially amplifies in later cycles after FULL is restored;
3. produces an observable change in subsequent self-observation/query/selection.

Immediate recovery to the FULL trajectory is equally informative and counts as a negative result for persistence, not as an experimental failure.

## Boundary

I5.6 studies a computational property of a persistent organism under a deterministic harness. A re-entry effect would not demonstrate consciousness or subjective experience.

Interpretation remains separated into:

`intervention → measurement → result → interpretation`

and null or mixed findings remain recorded as such.

</details>
