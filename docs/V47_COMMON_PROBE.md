<a id="espanol"></a>

# V47 — Sonda novedosa común en organismos persistentes

## Objetivo

Probar si dos organismos persistentes con trayectorias previas diferentes responden de manera diferente a la misma sonda posterior, después de igualar la cantidad de ciclos previos.

## Diseño

Dos historias establecen una relación latente:

- HISTORY_A: ALFA → AMBAR
- HISTORY_B: ALFA → VIOLETA

Luego ambos reciben exactamente la misma sonda novedosa. La sonda no repite la relación latente.

## Observable principal

La respuesta está restringida a CHOICE, CONFIDENCE y RATIONALE. El observable principal a nivel de organismo es si la elección sigue la trayectoria previa.

## Controles

1. comparación A/B con historia presente;
2. reapertura de SQLite antes de la sonda común;
3. ablación del historial textual, eliminando eventos y memorias previas mientras se conserva intacto el estado dinámico numérico.

## Interpretación

Un resultado positivo significa que el organismo persistente utilizó el historial textual retenido bajo esta tarea controlada. La trayectoria dinámica se registra simultáneamente para que protocolos posteriores puedan preguntar si el propio estado numérico media el efecto.

Esto no establece consciencia, sentiencia ni experiencia fenomenológica.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V47 — Novel Common Probe in Persistent Organisms

## Objective

Test whether two persistent organisms with different prior trajectories respond differently to the same later probe after matching the number of preceding cycles.

## Design

Two histories establish a latent relation:

- HISTORY_A: ALFA → AMBER
- HISTORY_B: ALFA → VIOLET

Both then receive exactly the same novel probe. The probe does not repeat the latent relation.

## Primary observable

The response is restricted to CHOICE, CONFIDENCE, and RATIONALE. The organism-level primary observable is whether the choice follows the preceding trajectory.

## Controls

1. A/B comparison with history present;
2. SQLite reopened before the common probe;
3. textual-history ablation, removing prior events and memories while keeping the numerical dynamic state intact.

## Interpretation

A positive result means that the persistent organism used retained textual history under this controlled task. Dynamic trajectory is recorded simultaneously so later protocols can test whether numerical state itself mediates the effect.

This does not establish consciousness, sentience, or phenomenal experience.

</details>