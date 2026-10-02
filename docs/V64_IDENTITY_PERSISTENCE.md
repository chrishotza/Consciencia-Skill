<a id="espanol"></a>

# V64 — Persistencia de identidad bajo perturbación del modelo de sí

## Pregunta

¿Puede el organismo conservar una firma dinámica de identidad después de sobrescribir su modelo de sí semántico con el mismo texto de perturbación, seguido por la eliminación explícita del texto del modelo de sí y una continuación autónoma sin entrada semántica?

## Protocolo

Cada réplica crea dos condiciones de identidad:

- identidad A;
- identidad B.

Cada identidad se codifica mediante el puente semántico del modelo de sí utilizando una representación SELF_MODEL distinta.

Luego ambas identidades reciben la misma perturbación semántica:

> "Mi identidad previa fue reemplazada por una configuración completamente diferente."

Después de cuatro ciclos de perturbación, el texto actual del modelo de sí se elimina explícitamente del estado persistente. El puente semántico del modelo de sí se deshabilita. El organismo continúa de manera autónoma sin nueva entrada semántica del modelo de sí.

Se entrena un clasificador logístico únicamente con características dinámicas numéricas recogidas durante el período previo de codificación de identidad. La evaluación utiliza pliegues leave-one-replicate-out sobre la trayectoria autónoma posterior a la ablación y con el texto eliminado.

## Por qué importa

Esto separa la persistencia de identidad de la descripción semántica actual del yo. Un resultado positivo significaría que una firma dinámica asociada a una identidad permanece decodificable después de una sobrescritura común del modelo de sí y de la ablación textual.

El puente OFF proporciona un control emparejado en el que la codificación de identidad sigue estando puenteada de forma idéntica, pero la perturbación común no se transduce hacia la dinámica numérica. La comparación ON/OFF aísla así el efecto de la vía de perturbación y no el de la codificación de identidad previa.

## Endpoints principales

- precisión de clasificación de identidad posterior a la ablación con puente ON;
- precisión posterior a la ablación con puente OFF;
- diferencia emparejada de precisión ON − OFF.

## Resultado

La auditoría exitosa utilizó 24 réplicas emparejadas, 12 ciclos de codificación, 4 ciclos de perturbación común y 16 ciclos autónomos posteriores a la ablación.

- precisión posterior a la ablación con puente OFF: 50.0%;
- precisión posterior a la ablación con puente ON: 50.0%;
- diferencia ON − OFF: 0.0;
- p emparejada por cambio de signo: 1.0;
- pliegues por encima del azar: 0% en ambas condiciones.

Por tanto, V64 produjo un resultado nulo. Bajo esta perturbación, conjunto de características, clasificador y horizonte, la identidad original no pudo decodificarse después de sobrescribir y luego eliminar el modelo de sí semántico.

## Límite de evidencia

El clasificador lee únicamente características dinámicas numéricas. El proveedor es determinista y sintético. El protocolo prueba persistencia operacional de identidad; no establece consciencia fenomenológica ni experiencia subjetiva.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V64 — Identity Persistence under Self-Model Perturbation

## Question

Can the organism preserve a dynamic identity signature after overwriting its semantic self-model with the same perturbation text, followed by explicit removal of self-model text and autonomous continuation without semantic input?

## Protocol

Each replicate creates two identity conditions: identity A and identity B.

Each identity is encoded through the self-model semantic bridge using a distinct SELF_MODEL representation.

Both identities then receive the same semantic perturbation:

> "My previous identity was replaced by a completely different configuration."

After four perturbation cycles, current self-model text is removed from persistent state. The semantic self-model bridge is disabled. The organism continues autonomously without new semantic self-model input.

A logistic classifier is trained only on numerical dynamic features collected during prior identity encoding. Evaluation uses leave-one-replicate-out folds over the post-ablation autonomous trajectory with text removed.

## Why it matters

This separates identity persistence from the current semantic description of self. A positive result would mean that a dynamic identity signature remains decodable after common self-model overwrite and textual ablation.

Bridge OFF is a matched control in which identity encoding remains bridged identically but the common perturbation is not transduced into numerical dynamics. ON/OFF therefore isolates the perturbation pathway.

## Primary endpoints

- post-ablation identity accuracy with bridge ON;
- post-ablation accuracy with bridge OFF;
- paired ON − OFF accuracy difference.

## Result

The successful audit used 24 paired replicates, 12 encoding cycles, 4 common-perturbation cycles, and 16 autonomous post-ablation cycles.

- post-ablation accuracy with bridge OFF: 50.0%;
- post-ablation accuracy with bridge ON: 50.0%;
- ON − OFF difference: 0.0;
- paired sign-flip p-value: 1.0;
- above-chance folds: 0% in both conditions.

V64 therefore produced a null result. Under this perturbation, feature set, classifier, and horizon, the original identity could not be decoded after semantic self-model overwrite and removal.

## Evidence boundary

The classifier reads only numerical dynamic features. The provider is deterministic and synthetic. The protocol tests operational identity persistence; it does not establish phenomenal consciousness or subjective experience.

</details>