<a id="espanol"></a>

# C0.3 — Information-Matched Causal Self-Reference Control

## Objetivo

C0.2 mostró que la acción seleccionada cambia cuando el estado propio se enmascara. C0.3 pregunta algo más exigente:

> ¿la política es específicamente sensible a su estado propio actual, o simplemente responde a valores de estado con una sensibilidad que también aparece cuando se le presentan estados ajenos con la misma distribución empírica?

El control preserva el mismo snapshot de política y la misma distribución de estados observada en las trayectorias FULL, pero rompe la correspondencia entre el episodio y el estado que recibe la política.

## Diseño

Se generan 64 trayectorias FULL con el mismo entrenamiento base de C0.2.

Para cada episodio:

1. se calcula la acción con el estado propio real;
2. se calcula la acción con un estado tomado de otro episodio mediante una permutación sin puntos fijos;
3. se repite el paso con una segunda permutación independiente;
4. se compara la brecha real-versus-mezclada con la brecha entre dos estados mezclados.

El contraste por réplica es:

\[
\Delta_i =
|a(s_i)-a(s_{\pi_1(i)})|
-
|a(s_{\pi_1(i)})-a(s_{\pi_2(i)})|.
\]

Una media positiva indica que la acción cambia más cuando se sustituye el estado propio actual que cuando se intercambian dos estados ajenos extraídos de la misma distribución. La prueba de signo por permutación se aplica al vector \(\Delta\).

## Controles

- mismo autoobservador;
- misma política entrenada;
- mismo snapshot durante toda la sonda;
- sin entrada semántica;
- sin reentrenamiento externo;
- estados de control tomados de la distribución empírica de las propias trayectorias.

## Límite

C0.3 fortalece la atribución causal de la acción al estado propio bajo esta sonda, pero sigue siendo una propiedad operacional del sistema. No demuestra experiencia fenomenal.

## Resultado auditado

Run GitHub Actions `36838675864`; artifact `11150238362`; commit `413e70499977d759e9effb50505c4db6174925c8`.

- brecha estado propio → estado mezclado: **1.06640625**;
- brecha entre dos estados mezclados: **1.00000000**;
- contraste: **+0.06640625**;
- p por permutación de signo: **0.3140343**;
- discrepancia de acción real vs. estado mezclado: **0.5332031**.

Interpretación: el control información-matcheado no mostró una separación estadísticamente detectable entre sensibilidad al estado propio actual y sensibilidad a estados ajenos extraídos de la misma distribución empírica. C0.3, por tanto, no confirma una dependencia causal específicamente propia del episodio bajo este criterio más exigente.

## Estado

**Ejecutado y archivado.** El resultado debe tratarse como control de especificidad causal para C3, no como puntuación global de conciencia.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# C0.3 — Information-Matched Causal Self-Reference Control

## Objective
C0.2 showed that selected action changes when own state is masked. C0.3 asks whether the policy is specifically sensitive to its current own state or merely to state values drawn from the same empirical distribution.

The control preserves the same policy snapshot and empirical state distribution but breaks episode/state correspondence.

## Design
For 64 FULL trajectories using the C0.2 training base:
1. compute action from the real own state;
2. compute action from a state taken from another episode via a fixed-point-free permutation;
3. repeat with a second independent permutation;
4. compare the real-versus-mixed gap with the gap between two mixed states.

Per-replicate contrast:
Delta_i = |a(s_i)-a(s_pi1(i))| - |a(s_pi1(i))-a(s_pi2(i))|.
A positive mean indicates that substituting the current own state changes action more than swapping two matched non-own states. Sign-permutation testing is applied to Delta.

## Controls
- same self-observer;
- same trained policy;
- same snapshot;
- no semantic input;
- no external retraining;
- control states drawn from the organism’s own empirical trajectory distribution.

## Audited result
GitHub Actions run 36838675864; artifact 11150238362; commit 413e70499977d759e9effb50505c4db6174925c8.
- own-state → mixed-state gap: +1.06640625;
- gap between two mixed states: 1.00000000;
- contrast: +0.06640625;
- sign-permutation p-value: 0.3140343;
- real-action vs mixed-state discrepancy: 0.5332031.

Interpretation: the information-matched control did not show statistically detectable separation between sensitivity to the current own state and sensitivity to other states from the same empirical distribution. C0.3 therefore does not confirm episode-specific causal dependence under this stricter criterion.

## Boundary
This is an operational causal-specificity control, not a global consciousness score and not evidence of phenomenal experience.

</details>