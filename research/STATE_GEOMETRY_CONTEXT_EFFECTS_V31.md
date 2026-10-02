<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V31 — Descomposición emparejada de efectos de contexto

## Estado

La primera ejecución V31 (36787649896) se **descarta por invalidez metodológica**, no como resultado científico. La implementación generaba las continuaciones A/B de referencia usando el mismo ángulo que la condición de prueba, haciendo tautológico el score de identidad.

La implementación corregida usa geometría A/B sin rotar (0°) como referencia local y geometría rotada (30°, 90°, 150°) como prueba, con state, memory y pressure del receptor idénticos entre referencia y prueba.

## Diseño corregido

- seis puntos ciegos V12;
- cuatro pares de historias;
- seeds independientes 60–69;
- state del receptor en midpoint A/B;
- memory y pressure sintéticos e independientes del donante;
- radio 1.1;
- ángulos de prueba 30°, 90°, 150°;
- input futuro exactamente cero;
- endpoint continuo primario: affinity firmada respecto de la **referencia local A/B sin rotar**.

El push corregido lanza una nueva ejecución V31.

Este experimento es mecanístico y no establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V31 — Paired Context Effect Decomposition

## Status
The first V31 run (`36787649896`) is **discarded as methodological invalidity**, not as a scientific result. Its implementation generated the A/B reference continuations using the same rotation angle as the test condition, which makes the identity score tautological.

The corrected implementation uses:
- unrotated donor A/B state geometry (0°) as the local reference pair;
- rotated donor geometry (30°, 90°, 150°) as the test conditions;
- identical receiver state, memory, and pressure context in reference and test.

## Corrected design
- six fixed V12 blind parameter points;
- four history pairs;
- independent seeds 60–69;
- receiver state fixed to A/B midpoint;
- donor-independent synthetic memory and pressure;
- radius 1.1;
- test angles 30°, 90°, 150°;
- future input exactly zero;
- primary continuous endpoint: signed affinity relative to the **unrotated** local A/B reference.

The corrected push automatically launches a new V31 run.

This experiment is mechanistic and does not establish consciousness or subjective experience.
