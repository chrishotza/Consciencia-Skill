<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V41 — Transferencia de referencia entre pares históricos

## Estado

**OFICIAL — GitHub Actions run 36793638980.**

V41 conserva el readout reference-based de V34–V40, pero construye las referencias A/B usando un **history-pair template diferente** al del test.

Mapeo cíclico:

- test pair 0 → reference pair 1
- test pair 1 → reference pair 2
- test pair 2 → reference pair 3
- test pair 3 → reference pair 0

Las seeds de test y referencia fueron completamente disjuntas.

## Resultado primario

| Métrica | Resultado |
|---|---:|
| Contraste 30°−150° | **−0.214374** |
| Null estratificado, media | 0.000043 |
| Null 95% | 0.064753 |
| Permutation p | **1.000000** |
| Bootstrap 95% | **[−0.247079, −0.180408]** |
| Bloques history-seed | 40 |

Los nueve contextos memory×pressure presentaron contraste negativo.

## Interpretación

V40 mostró que separar la seed histórica concreta no destruye el efecto mientras se mantiene el mismo tipo de history-pair. V41 muestra que cambiar además el **tipo de historia** sí elimina la dirección observada y la desplaza hacia el signo opuesto.

Esto localiza una dependencia importante: el readout reference-based no parece transportar una geometría única entre los cuatro regímenes históricos utilizados. La compatibilidad entre el tipo de historia del test y el de la referencia emerge como variable experimental relevante.

No debe interpretarse como demostración de consciencia, subjetividad o experiencia. Es un resultado sobre la dinámica y el readout del simulador.

## Siguiente paso

V42 realizará la **matriz completa 4×4 test-pair × reference-pair**, en vez de estudiar solamente la diagonal implícita de V40 y una transferencia cíclica de V41. El objetivo es medir si existe una estructura de compatibilidad gradual entre regímenes.

## Reproducibilidad

Run: **36793638980**

Artifact: **11132601691**

Workflow commit: **95f2cc57b9c3c921ef42616a384cea8468df5c48**

Código: **a51967898fdd2f88f50fa07c11a509c7f2f676b5**

</details>

<a id="english"></a>

# V41 — Cross-Pair Reference Transfer

## Estado

**OFICIAL — GitHub Actions run 36793638980.**

V41 mantuvo el readout reference-based de V34–V40, pero construyó las referencias A/B usando un **history-pair template diferente** al del test.

Mapeo cíclico:

- test pair 0 → reference pair 1
- test pair 1 → reference pair 2
- test pair 2 → reference pair 3
- test pair 3 → reference pair 0

Las semillas de test y referencia fueron completamente disjuntas.

## Resultado primario

| Métrica | Resultado |
|---|---:|
| Contraste 30°−150° | **−0.214374** |
| Null estratificado, media | 0.000043 |
| Null 95% | 0.064753 |
| Permutation p | **1.000000** |
| Bootstrap 95% | **[−0.247079, −0.180408]** |
| Bloques history-seed | 40 |

Los nueve contextos memoria×presión presentaron contraste negativo.

## Interpretación

V40 mostró que separar la semilla histórica concreta no destruye el efecto mientras se mantiene el mismo tipo de history-pair. V41 muestra que cambiar además el **tipo de historia** sí elimina la dirección observada y la desplaza hacia el signo opuesto.

Esto localiza una dependencia importante: el readout reference-based no parece transportar una geometría única entre los cuatro regímenes históricos utilizados. La compatibilidad entre el tipo de historia del test y el de la referencia emerge como una variable experimental relevante.

No debe interpretarse como una demostración de conciencia, subjetividad o experiencia. Es un resultado sobre la dinámica y el readout del simulador.

## Siguiente paso

V42 realizará la **matriz completa 4×4 test-pair × reference-pair**, en vez de estudiar solamente la diagonal implícita de V40 y una transferencia cíclica de V41. El objetivo es medir si existe una estructura de compatibilidad gradual entre regímenes.

## Reproducibilidad

Run: **36793638980**

Artifact: **11132601691**

Workflow commit: **95f2cc57b9c3c921ef42616a384cea8468df5c48**

Código: **a51967898fdd2f88f50fa07c11a509c7f2f676b5**
