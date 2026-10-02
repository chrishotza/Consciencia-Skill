<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V21 — Control del orden temporal del estado

## Pregunta

V16 mostró que ambos slots temporales contienen información. V21 pregunta si importan su **orden y relación temporal**, en lugar de que la identidad dependa solo del par no ordenado de valores escalares.

## Protocolo

Seis puntos ciegos V12, cuatro pares de historias, diez seeds de ruido emparejados por par, input futuro exactamente cero y memory/pressure comunes del receptor.

Para cada estado donante se comparan:

- intact: conservar ambos slots;
- swap_slots: intercambiar state_prev y state conservando ambos valores exactamente;
- flatten_same_value: reemplazar ambos slots por la media del donante;
- common: borrar completamente el state donante;
- time_reverse_centered: invertir las dos desviaciones del donante alrededor del contexto común.

La identidad se clasifica por affinity frente a las referencias intactas donante/opuesta durante los primeros 60 pasos futuros.

## Regla de interpretación

Si swap_slots o la reversión temporal centrada causa una pérdida sustancial de identidad respecto de intact mientras preserva información de magnitud escalar, el resultado respalda una interpretación de organización temporal: el state porta información mediante dinámica ordenada y no solo dos números independientes.

Es un test dinámico computacional y no establece experiencia subjetiva.

</details>

<a id="english"></a>

# V21 — State Temporal-Order Control

## Question

V16 showed that both temporal state slots carry information. V21 asks whether their **ordering and temporal relation** matter, rather than identity depending only on the unordered pair of scalar values.

## Protocol

Six V12 blind parameter points, four history pairs, ten matched-noise seeds per pair, exact-zero future input, and common receiver memory/pressure.

For each donor state we compare:
- `intact`: preserve both temporal slots;
- `swap_slots`: exchange `state_prev` and `state` while preserving both values exactly;
- `flatten_same_value`: replace both slots by their donor mean;
- `common`: erase donor state completely;
- `time_reverse_centered`: reverse the two donor deviations around the common context.

Identity is classified by affinity to the intact donor/opposite references over the first 60 future steps.

## Interpretation rule

If `swap_slots` or centered temporal reversal causes a substantial loss of identity relative to intact while preserving scalar magnitude information, the result supports a temporal-organization interpretation: the state carries information through ordered dynamics, not just through two independent numbers.

This is a computational dynamical test and does not establish subjective consciousness.