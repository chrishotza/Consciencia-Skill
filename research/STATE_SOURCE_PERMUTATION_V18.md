<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V18 — Control de fuente/permutación del estado

## Pregunta

V17 mostró que el state del donante por sí solo puede transferir identidad histórica cuando memory y pressure del receptor son comunes. V18 pregunta si la identidad de continuación sigue específicamente a la **fuente del state** en lugar de a una etiqueta nominal del receptor.

## Protocolo

Se utilizan seis puntos ciegos V12, tres historias distintas por seed, diez seeds de ruido emparejados por punto, input futuro exactamente cero y un receptor cuyo memory y pressure son la media común de las tres historias.

El receptor recibe state de una historia fuente a la vez. La identidad de fuente se clasifica frente a tres continuaciones de referencia intactas. State se prueba a precisión completa y a 3, 4 y 6 bits.

Un control de permutación repite el test cambiando la etiqueta nominal del receptor. Como todo contexto no-state es común, un verdadero portador de fuente-state debería conservar la clasificación de la fuente del state independientemente de esa etiqueta nominal.

## Regla de interpretación

Accuracy alta de clasificación de fuente y predicción sin cambios cuando se permuta el receptor nominal constituirían un test limpio de seguimiento de fuente: la identidad histórica está unida al state recurrente transferido y no al contexto receptor.

Junto con V17, esto prueba suficiencia causal y especificidad de fuente del state recurrente compacto.

Sigue siendo un resultado dinámico computacional y no establece experiencia subjetiva.

</details>

<a id="english"></a>

# V18 — State Source / Permutation Control

## Question

V17 showed that donor state alone can transfer historical identity when receiver memory and pressure are common. V18 asks whether the continuation identity specifically follows the *source of the state* rather than any nominal receiver label.

## Protocol

The experiment uses the six V12 blind parameter points, three distinct histories per seed, ten matched-noise seeds per point, exact-zero future input, and a receiver whose memory and pressure are the common mean of all three histories.

The receiver receives state from one source history at a time. Source identity is classified against three intact reference continuations. State is tested at full precision and at 3, 4, and 6 bits.

A permutation control repeats the test while changing the nominal receiver label. Because all non-state context is common, a genuine state-source carrier should preserve the classification of the state source regardless of that nominal label.

## Interpretation rule

High source-classification accuracy and an unchanged prediction when the nominal receiver is permuted would provide a clean source-following test: historical identity is attached to the transferred recurrent state rather than to the receiver context.

Together with V17, this tests both causal sufficiency and source specificity of the compact recurrent state.

This remains a computational dynamical result and does not establish subjective consciousness.