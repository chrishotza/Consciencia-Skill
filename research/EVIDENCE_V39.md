<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V39 — Decoder continuo sin referencia

## Estado

**OFICIAL — resultado negativo.**

V39 mantiene el decoder cross-history de V37 pero sustituye accuracy binaria por dos márgenes continuos: signed probability margin y signed logistic log-odds.

## Resultado

| Métrica | 30°−150° | Null 95% | p |
|---|---:|---:|---:|
| signed probability margin | **-0.040861** | 0.024093 | **1.0000** |
| signed log-odds | **-0.089071** | 0.053049 | **1.0000** |

Media por ángulo:

| Ángulo | Signed margin | Signed logit | Accuracy |
|---:|---:|---:|---:|
| 0° | -0.00829 | -0.01714 | 50.38% |
| 30° | 0.04042 | 0.08313 | 59.09% |
| 150° | **0.08128** | **0.17220** | **62.90%** |

## Lectura

Cambiar de accuracy a un margen continuo **no recupera** la dirección 30°−150°. El resultado sigue favoreciendo la dirección opuesta con el decoder reference-free.

Esto refuerza la conclusión metodológica de V37: el fenómeno fuerte de V34–V36 no puede tratarse como una propiedad angular universal de la trayectoria independiente del esquema de lectura.

La formulación más precisa es que el efecto robusto observado hasta V36 está ligado a una clase concreta de lectura basada en referencias de continuación construidas a partir del estado histórico donante/receptor.

Esto no invalida automáticamente la geometría observada; identifica una dependencia importante del readout que debe aislarse.

No demuestra consciencia, subjetividad ni experiencia.

## Reproducibilidad

Run: **36792742254**

Artifact: **11132661307**

Commit final: **d7dbea783a116995a00fdb4a7f407c2a25e79006**

</details>

<a id="english"></a>

# V39 — Reference-Free Continuous Decoder

## Estado

**OFICIAL — resultado negativo.**

V39 mantiene el decoder cross-history de V37 pero sustituye accuracy binaria por dos márgenes continuos: signed probability margin y signed logistic log-odds.

## Resultado

| Métrica | 30°−150° | Null 95% | p |
|---|---:|---:|---:|
| signed probability margin | **-0.040861** | 0.024093 | **1.0000** |
| signed log-odds | **-0.089071** | 0.053049 | **1.0000** |

Media por ángulo:

| Ángulo | Signed margin | Signed logit | Accuracy |
|---:|---:|---:|---:|
| 0° | -0.00829 | -0.01714 | 50.38% |
| 30° | 0.04042 | 0.08313 | 59.09% |
| 150° | **0.08128** | **0.17220** | **62.90%** |

## Lectura

El cambio de accuracy a un margen continuo **no rescata** la dirección 30°−150°. El resultado sigue favoreciendo la dirección opuesta bajo el decoder reference-free.

Esto fortalece la conclusión metodológica de V37: el fenómeno fuerte de V34–V36 no puede tratarse como una propiedad angular universal de la trayectoria independiente del esquema de lectura.

La evidencia favorece una formulación más precisa: el efecto robusto observado hasta V36 está ligado a una clase concreta de lectura basada en referencias de continuación construidas a partir del estado histórico donante/receptor.

Esto no invalida automáticamente la geometría observada; identifica una dependencia importante del readout que debe aislarse.

No demuestra conciencia, subjetividad ni experiencia.

## Reproducibilidad

Run: **36792742254**

Artifact: **11132661307**

Commit final: **d7dbea783a116995a00fdb4a7f407c2a25e79006**
