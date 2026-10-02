<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V39 — Margen continuo del decoder reference-free

V39 retoma el resultado negativo de V37 con un readout continuo en lugar de accuracy umbralizada.

Un decoder logístico estandarizado se entrena con nueve history-seeds y se evalúa sobre la décima. No se construye una referencia de continuación dentro de la misma historia.

Para cada trayectoria reservada, el decoder produce una probabilidad/logit de identidad del donante. El score se firma según la etiqueta real del donante, de modo que valores positivos mayores indican una decodificación más consistente con el donante.

La estadística primaria es la diferencia entre la media de decoding firmado a 30° y 150°, promediada a nivel de bloque history-seed reservado.

Diseño: seis puntos paramétricos fijos, cuatro estratos history-pair, nueve contextos sintéticos memory/pressure, ángulos 0°, 30°, 150°, radio 1.1, input futuro cero y seeds de continuación disjuntas.

Inferencia: sign-flip emparejado sobre los diez bloques history reservados.

Propósito: determinar si el resultado negativo de V37 era principalmente un artefacto de threshold/accuracy.

El test no establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V39 — Reference-Free Continuous Decoder Margin

V39 revisits the negative V37 result with a continuous readout instead of thresholded accuracy.

A standardized logistic decoder is trained on nine history-seeds and evaluated on the tenth. No within-history reference continuation is constructed.

For each held-out trajectory, the decoder produces a probability/logit for donor identity. The score is signed by the true donor label, so larger positive values mean stronger donor-consistent decoding.

The primary statistic is the difference between mean signed decoding at 30° and 150°, averaged at held-out history-seed block level.

Design: six fixed parameter points, four history-pair strata, nine synthetic memory/pressure contexts, angles 0°, 30°, 150°, radius 1.1, zero future input, and disjoint continuation seeds.

Inference: paired sign-flip across the ten held-out history blocks.

Purpose: determine whether V37's negative result was mainly a threshold/accuracy artifact. The test does not establish consciousness or subjective experience.
