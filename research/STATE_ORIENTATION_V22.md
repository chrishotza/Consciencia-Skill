<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V22 — Orientación del estado / rotación de norma igual

## Pregunta

V21 mostró que importa la organización temporal. V22 pregunta si el state recurrente codifica identidad en la **orientación de su vector temporal de estado**, independientemente de su magnitud total.

## Protocolo

Seis puntos ciegos V12, cuatro pares de historias, diez seeds de ruido emparejados por par, input futuro exactamente cero y memory/pressure comunes del receptor.

En la frontera se define la desviación bidimensional del donante:

d = (state_prev - common_prev, state - common_state).

El experimento rota este vector 0, 45, 90, 135, 180, 225, 270 y 315 grados alrededor del contexto común. La rotación conserva exactamente la norma euclídea; solo cambia la orientación.

La identidad se clasifica por affinity frente a referencias A/B intactas durante los primeros 60 pasos futuros.

## Regla de interpretación

Si la identidad cambia sistemáticamente con el ángulo de rotación a pesar de mantener fija la magnitud de la desviación, el resultado respalda una representación geométrica/orientacional de información histórica en el estado recurrente.

Una inversión aproximada de 180 grados que favorezca al donante opuesto sería especialmente informativa porque es el análogo de norma igual de V19.

Sigue siendo un test dinámico computacional y no establece experiencia subjetiva.

</details>

<a id="english"></a>

# V22 — State Orientation / Equal-Norm Rotation

## Question

V21 showed that temporal organization matters. V22 asks whether the recurrent state encodes identity in the **orientation of its temporal state vector**, independently of its total magnitude.

## Protocol

Six blind parameter points from V12, four history pairs, ten matched-noise seeds per pair, exact-zero future input, and common receiver memory/pressure.

At the boundary, define the two-dimensional donor deviation:

`d = (state_prev - common_prev, state - common_state)`.

The experiment rotates this vector by 0, 45, 90, 135, 180, 225, 270, and 315 degrees around the common context. Rotation preserves the Euclidean norm exactly; only orientation changes.

Identity is classified by affinity to intact A/B continuation references over the first 60 future steps.

## Interpretation rule

If identity changes systematically with rotation angle despite fixed state-deviation magnitude, the result supports a geometric/orientational representation of historical information in the recurrent state.

An approximately 180-degree inversion that favors the opposite donor would be especially informative because it is the equal-norm analogue of V19.

This remains a computational dynamical test and does not establish subjective consciousness.