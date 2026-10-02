<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V44 — Transporte causal de memory sin referencia

V44 pregunta si la historia codificada en la variable interna memory es simplemente legible o si la dinámica posterior la utiliza causalmente.

Un decoder solo-state se entrena con trayectorias futuras limpias y se evalúa leave-one-parameter-out. El decoder nunca recibe memory ni pressure como features.

Para cada contexto receptor reservado, el input futuro es exactamente cero. Solo cambia un componente del contexto interno inicial:

- contexto receptor intacto;
- memory reemplazada por memory de una historia donante de otra clase;
- pressure reemplazada;
- state reemplazado como control causal positivo.

La estadística primaria es el cambio emparejado en la probabilidad de clase donante-minus-receptor causado por reemplazar memory, relativo a la trayectoria receptora intacta. Como el decoder solo ve la trayectoria futura resultante del state, un efecto positivo de memory indica que cambiar memory alteró la dinámica posterior en dirección de la clase histórica donante.

El experimento utiliza rangos disjuntos de seeds de receptor y donante y seis puntos paramétricos ciegos.

No establece consciencia, experiencia subjetiva, sentiencia ni awareness fenomenológico.

</details>

<a id="english"></a>

# V44 — Reference-Free Causal Memory Transport

V44 asks whether encoded history in the internal memory variable is merely readable, or whether it is causally used by downstream dynamics.

A state-only decoder is trained on clean future trajectories and evaluated leave-one-parameter-out. The decoder never receives memory or pressure as features.

For each held-out receiver context, future input is exactly zero. Only one component of the internal starting context is changed:
- intact receiver context;
- memory swapped with a donor history from another history class;
- pressure swapped;
- state swapped as a positive causal control.

The primary statistic is the paired change in donor-minus-receiver class probability caused by memory replacement, relative to the intact trajectory. Because the decoder sees only the resulting future state trajectory, a positive memory effect indicates that changing memory altered downstream state dynamics in the direction of the donor history class.

The experiment uses disjoint receiver and donor history seed ranges and six blind parameter points.

This experiment does not establish consciousness, subjective experience, sentience, or phenomenological awareness.
