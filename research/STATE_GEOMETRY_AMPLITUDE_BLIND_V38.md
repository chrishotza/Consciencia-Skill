<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V38 — Decoder cross-history ciego a amplitud

V38 repite la lógica del decoder reference-free con history-seeds nuevas 130–139.

Antes de extraer features, cada trayectoria futura del estado se normaliza mediante L2. Por lo tanto, el decoder recibe solamente estadísticas de forma de trayectoria invariantes a escala y no la amplitud absoluta.

El modelo se entrena con nueve history-seeds y se evalúa sobre la décima reservada. No se construye ninguna referencia de continuación de la misma historia.

Diseño: seis puntos paramétricos fijos, cuatro estratos history-pair, nueve contextos memory/pressure, ángulos 0°, 30° y 150°, input futuro exactamente cero y seeds de continuación disjuntas.

Estadística primaria: diferencia de accuracy held-out 30° menos 150° en los diez bloques history-seed reservados.

Inferencia: sign-flip emparejado sobre los diez bloques history reservados.

El experimento prueba si la señal angular reference-free sobrevive al eliminar la escala global de trayectoria. No establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V38 — Amplitude-Blind Cross-History Decoder

V38 repeats the reference-free decoder logic with fresh history seeds 130–139.

Before feature extraction, each future state trajectory is L2-normalized. The decoder therefore receives only scale-invariant trajectory-shape statistics rather than absolute trajectory amplitude.

The model is trained on nine history seeds and evaluated on the held-out tenth seed. No same-history continuation reference is constructed.

Design: six fixed parameter points, four history-pair strata, nine memory/pressure contexts, angles 0°, 30°, and 150°, exactly zero future input, and disjoint continuation seeds.

Primary statistic: held-out accuracy difference 30° minus 150° across the ten held-out history-seed blocks.

Inference: paired sign-flip across the ten held-out history blocks.

The experiment tests whether the reference-free angular signal survives removal of global trajectory scale. It does not establish consciousness or subjective experience.
