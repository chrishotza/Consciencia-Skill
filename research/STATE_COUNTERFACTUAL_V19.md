<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V19 — Inversión contrafáctica del estado

## Pregunta

V18 mostró que la clasificación sigue la fuente del estado transferido y no la etiqueta nominal del receptor. V19 prueba un contrafactual más fuerte: reflejar el estado donante alrededor del estado común A/B manteniendo memory y pressure comunes e input futuro cero.

## Protocolo

Se usan seis puntos ciegos V12, cuatro pares históricos y diez seeds de ruido emparejados por par.

Para cada donante:

- intact: conservar el state donante;
- erase: reemplazar state por el midpoint común A/B;
- invert: reflejar ambos slots temporales alrededor del midpoint común;
- invert_quantized: realizar la misma reflexión y luego cuantizar ambos slots a 3 bits.

Memory y pressure del receptor son siempre comunes, por lo que la identidad específica del donante entra solo por state.

## Predicción

Si state codifica identidad histórica de manera direccional, el state invertido debería mover preferentemente la continuación hacia la referencia del donante opuesto. El readout informa tanto accuracy del donante original como accuracy del donante invertido.

## Límites

Es un test causal contrafactual del encoding de state en el modelo dinámico implementado. Incluso una inversión exitosa demostraría transporte de información dependiente del estado, no consciencia subjetiva.

</details>

<a id="english"></a>

# V19 — State Counterfactual Inversion

## Question

V18 showed that classification follows the source of the transferred state rather than the nominal receiver label. V19 tests a stronger counterfactual: reflect the donor state around the common A/B state while keeping memory and pressure common and future input zero.

## Protocol

Six V12 blind parameter points, four history pairs, and ten matched-noise seeds per pair are used.

For each donor:
- `intact`: retain the donor state;
- `erase`: replace the state with the A/B common midpoint;
- `invert`: reflect both temporal state slots around the common midpoint;
- `invert_quantized`: perform the same reflection and then quantize both state slots to 3 bits.

The receiver memory and pressure are always common, so donor-specific identity enters only through state.

## Prediction

If state encodes historical identity directionally, the inverted state should preferentially move the continuation toward the opposite donor reference. The readout therefore reports both original-donor accuracy and flipped-donor accuracy.

## Interpretation limits

This is a counterfactual causal test of state encoding in the implemented dynamical model. Even a successful inversion would establish state-dependent information transport, not subjective consciousness.