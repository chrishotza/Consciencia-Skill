# I5.18 — Global Phase × Bridge Interaction and Multiplicity Control

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.17 mostró un perfil del efecto bridge a través de los seis lags, pero sus p-valores eran contrastes locales por lag. I5.18 añade el análisis global que faltaba antes de interpretar ese perfil mecanísticamente.

I5.18 no recolecta nuevas trayectorias: consume el `summary.json` congelado de I5.17 y aplica un plan estadístico explícito.

## Análisis primario

La matriz principal es réplica × lag para cada endpoint bridge ON − OFF:

- AUC firmada;
- AUC absoluta;
- cambio de acción futura.

Se calculan dos pruebas complementarias.

### 1. Interacción global fase × bridge

Para cada réplica se conservan los seis efectos emparejados y se permutan las etiquetas de lag dentro de esa réplica. El estadístico es la suma de cuadrados de las medias por lag alrededor de la media global.

La hipótesis nula es que el efecto bridge no depende del lag bajo el intercambio de las etiquetas temporales.

### 2. Control de multiplicidad max-T

Para cada lag se conserva el contraste ON − OFF, pero las inversiones de signo se hacen a nivel de réplica. En cada permutación se obtiene el máximo valor absoluto entre los seis contrastes. Los p-valores por lag se corrigen de forma conjunta usando esa distribución max-T.

Esto evita convertir seis p-valores locales en una falsa afirmación global.

## Endpoint secundario

También se calcula el efecto bridge medio agregando los seis lags dentro de cada réplica y aplicando sign-flip a nivel de réplica.

## Datos y límites

Los datos son los efectos por réplica ya producidos por I5.17. No se generan nuevas muestras.

I5.18 es un control estadístico sobre el resultado de I5.17; no demuestra consciencia, experiencia subjetiva ni una interpretación mecanística por sí mismo.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.17 showed a bridge-effect profile across the six lags, but its p-values were local per-lag contrasts. I5.18 adds the missing global analysis before stronger mechanistic interpretation.

I5.18 does not collect new trajectories: it consumes the frozen I5.17 `summary.json` and applies an explicit statistical plan.

## Primary analysis

The main matrix is replicate × lag for each bridge ON − OFF endpoint:

- signed AUC;
- absolute AUC;
- future-action change.

Two complementary tests are computed.

### 1. Global phase × bridge interaction

For each replicate, the six paired effects are retained and lag labels are permuted within that replicate. The statistic is the sum of squares of lag means around the grand mean.

The null hypothesis is that the bridge effect does not depend on lag under exchange of the temporal labels.

### 2. max-T multiplicity control

For each lag the ON − OFF contrast is retained, but sign flips are applied at the replicate level. Each permutation records the maximum absolute value across the six lag contrasts. Lag-wise p-values are then jointly corrected against that max-T distribution.

This prevents six local p-values from being converted into a spurious global claim.

## Secondary endpoint

The mean bridge effect across all six lags is also computed by averaging within replicate and applying a replicate-level sign-flip test.

## Data and boundary

The data are the per-replicate effects already produced by I5.17. No new samples are generated.

I5.18 is a statistical control on the I5.17 result; it does not establish consciousness, subjective experience, or a mechanistic interpretation on its own.

</details>
