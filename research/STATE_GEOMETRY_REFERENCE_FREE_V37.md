<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V37 — Decoder cross-history sin referencia

V37 elimina las referencias de continuación A/B dentro de historia usadas en V33–V35.

Un decoder logístico se entrena únicamente con trayectorias de las otras nueve history-seeds y se evalúa sobre la history-seed reservada. Las propias trayectorias de prueba nunca se comparan contra una continuación generada desde la misma historia.

El decoder recibe 12 observables fijos de trayectoria calculados solo a partir de la continuación de prueba:

mean, standard deviation, mean absolute state, range, mean velocity, velocity standard deviation, mean absolute velocity, acceleration standard deviation, mean absolute acceleration, endpoint displacement, early-window mean y late-window mean.

El test contiene seis puntos paramétricos fijos, cuatro estratos history-pair, nueve contextos memory/pressure, ángulos 0°, 30° y 150°, input futuro cero y seeds de continuación disjuntas.

Análisis primario: diferencia de accuracy held-out entre 30° y 150°.

La inferencia usa sign-flip emparejado sobre los diez bloques history-seed reservados.

La interpretación se restringe a geometría computacional de trayectorias. Los resultados positivos no establecen consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V37 — Reference-Free Cross-History Decoder

V37 removes the within-history A/B continuation references used in V33–V35.

A logistic decoder is trained only on trajectories from the other nine history seeds and evaluated on the held-out history seed. The test trajectories themselves are never compared against a continuation generated from the same history.

The decoder receives 12 fixed trajectory observables computed solely from the test continuation:
mean, standard deviation, mean absolute state, range, mean velocity, velocity standard deviation, mean absolute velocity, acceleration standard deviation, mean absolute acceleration, endpoint displacement, early-window mean, and late-window mean.

The test contains six fixed parameter points, four history-pair strata, nine memory/pressure contexts, angles 0°, 30°, 150°, zero future input, and disjoint continuation seeds.

Primary analysis: held-out accuracy difference between 30° and 150°.

Inference is paired sign-flip across the ten held-out history-seed blocks.

Interpretation is restricted to computational trajectory geometry. Positive results do not establish consciousness or subjective experience.
