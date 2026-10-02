# V29 — Exploratory Auxiliary Context Isolation

## Status
**SUCCESS** — GitHub Actions run `36787019017`.

## Methodological disposition
V29 is retained as an exploratory run, **not as confirmatory evidence**.

Two limitations were identified:

1. With the receiver state fixed at the A/B midpoint, a 180° rotation of donor A maps exactly onto donor B (and vice versa). Therefore the 180° condition is a geometric identity swap by construction, not an independent test.
2. In MEM_A/MEM_B and PRESS_A/PRESS_B, the nuisance context is taken from one of the donor histories. That creates donor-linked context and can bias identity classification independently of the transplanted state geometry.

## Observed exploratory result
At 90°, pooled identity accuracy ranged from 52.08% to 58.75% across the tested contexts, with positive signed affinity in every context. The 180° condition was 0% identity across contexts by construction.

These numbers are therefore useful for diagnosing the design but should not be treated as evidence that memory or pressure independently controls the state code.

## Decision
V29 is explicitly marked **exploratory / confounded**.

## Next
V30 replaces donor-linked nuisance contexts with predeclared synthetic contexts independent of A/B history and removes the tautological 180° comparison as a primary endpoint.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V29 — Aislamiento exploratorio de contexto auxiliar

## Estado
**SUCCESS** — GitHub Actions run 36787019017.

## Disposición metodológica
V29 se conserva como ejecución exploratoria, **no como evidencia confirmatoria**.

Se identificaron dos limitaciones:

1. Con el estado del receptor fijado en el midpoint A/B, una rotación de 180° del donante A se transforma exactamente en B (y viceversa). Por lo tanto, 180° es un intercambio geométrico de identidad por construcción y no un test independiente.
2. En MEM_A/MEM_B y PRESS_A/PRESS_B, el contexto auxiliar procede de una de las historias donantes. Esto crea contexto ligado al donante y puede sesgar la clasificación de identidad independientemente de la geometría del state trasplantado.

## Resultado exploratorio observado
A 90°, la accuracy agrupada de identidad varió entre 52.08% y 58.75% entre los contextos probados, con affinity firmado positivo en todos ellos. La condición 180° fue 0% de identidad entre contextos por construcción.

Estas cifras son útiles para diagnosticar el diseño, pero no deben tratarse como evidencia de que memory o pressure controlen independientemente el código de state.

## Decisión
V29 queda marcado explícitamente como **exploratorio / confounded**.

## Próximo
V30 reemplaza los contextos nuisance ligados al donante por contextos sintéticos predeclarados e independientes de la historia A/B y elimina la comparación tautológica 180° como endpoint primario.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V29 — Exploratory Auxiliary Context Isolation

## Status
**SUCCESS** — GitHub Actions run 36787019017.

## Methodological disposition
V29 is retained as an exploratory run, **not as confirmatory evidence**.

Two limitations were identified:

1. With receiver state fixed at the A/B midpoint, a 180° rotation of donor A maps exactly onto donor B (and vice versa). Therefore 180° is a geometric identity swap by construction, not an independent test.
2. In MEM_A/MEM_B and PRESS_A/PRESS_B, nuisance context comes from one donor history. This creates donor-linked context and can bias identity classification independently of transplanted-state geometry.

## Observed exploratory result
At 90°, pooled identity accuracy ranged from 52.08% to 58.75% across tested contexts, with positive signed affinity in every context. The 180° condition was 0% identity across contexts by construction.

These values are useful for design diagnosis but should not be treated as evidence that memory or pressure independently controls the state code.

## Decision
V29 is explicitly marked **exploratory / confounded**.

## Next
V30 replaces donor-linked nuisance contexts with predeclared synthetic contexts independent of A/B history and removes the tautological 180° comparison as a primary endpoint.

</details>