# V28 — Context Dependence / Transport Test

## Status
**SUCCESS** — GitHub Actions run `36786588699` (corrected isorradial version).

## Important analysis note
The original V28 identity column at radius 0 is not a valid 50% null because exact zero affinity maps to `sign(0)=0`, which is counted as incorrect for either donor. Also, the 0° condition at radius 1.1 is a built-in local-reference control: the transformed donor state exactly reproduces its own local reference state, so its 100% identity is tautological.

The informative V28 quantities are therefore the off-axis conditions, especially signed affinity at 90° and 180°.

## Design
- 6 fixed V12 blind parameter points.
- 4 history pairs.
- seeds 30–39.
- 3 receiver histories:
  - context 0: zero history,
  - context 1: all-positive history,
  - context 2: independent random-sign history.
- Future input exactly zero.
- Donor state geometry: radius 1.1 at 0°, 90°, 180°.
- Receiver memory and pressure come from the selected receiver history.
- Local A/B reference continuations are generated within each receiver context.

## Result

### Pooled identity accuracy at r = 1.1

| Receiver context | 0° | 90° | 180° |
|---|---:|---:|---:|
| zero-history | 100.0% | 38.75% | 43.13% |
| all-positive | 100.0% | 49.38% | 51.46% |
| random-sign | 100.0% | 42.29% | 39.58% |

The 0° result is the expected local-reference control and is not a discovery.

The 90°/180° results do not reproduce the strong antipodal inversion seen in the common-midpoint protocol.

Signed affinity at 180°, where positive means closer to the donor's original local reference and negative means antipodal reversal:
- context 0: **-0.010**
- context 1: **+0.215**
- context 2: **-0.118**

## Interpretation
V28 places a constraint on V24–V27:

> The directional state effect is **not demonstrated to be context-invariant** when receiver memory/pressure context is changed through distinct histories.

This is a useful mechanistic boundary. It indicates that the measured geometry is coupled to local dynamical context rather than functioning as an unconditional context-free code.

## Boundary
V28 does not establish consciousness, subjective experience, or sentience. It establishes a limitation on transportability of the tested computational state representation.

## Next
V29 isolates nuisance variables one at a time: receiver state held fixed while memory-only or pressure-only context is changed, with antipodal affinity measured directly.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V28 — Evidencia de dependencia/transportabilidad del contexto

## Estado
**SUCCESS** — GitHub Actions run 36786588699 (versión corregida isorradial).

## Nota metodológica importante
La columna de identity de V28 en radius 0 no constituye un null válido del 50% porque affinity exactamente cero se transforma mediante sign(0)=0 y se cuenta como incorrecta para ambos donantes. Además, la condición 0° en radius 1.1 es un control de referencia local construido: el estado donante transformado reproduce exactamente su propia referencia local, por lo que su 100% de identidad es tautológico.

Por ello, las cantidades informativas de V28 son las condiciones fuera de eje, especialmente affinity firmado a 90° y 180°.

## Diseño
- 6 puntos ciegos V12.
- 4 pares de historias.
- seeds 30–39.
- 3 historias de receptor:
  - contexto 0: historia cero;
  - contexto 1: historia toda positiva;
  - contexto 2: historia de signos aleatorios independiente.
- Input futuro exactamente cero.
- Geometría del estado donante: radius 1.1 a 0°, 90° y 180°.
- Memory y pressure del receptor provienen de la historia receptora elegida.
- Las continuaciones de referencia locales A/B se generan dentro de cada contexto receptor.

## Resultado

### Accuracy de identidad agrupada con r = 1.1

| Contexto receptor | 0° | 90° | 180° |
|---|---:|---:|---:|
| zero-history | 100.0% | 38.75% | 43.13% |
| all-positive | 100.0% | 49.38% | 51.46% |
| random-sign | 100.0% | 42.29% | 39.58% |

El resultado 0° es el control de referencia local esperado y no constituye un descubrimiento.

Los resultados 90°/180° no reproducen la fuerte inversión antipodal observada en el protocolo de midpoint común.

Affinity firmado a 180°, donde positivo significa mayor cercanía a la referencia local original del donante y negativo inversión antipodal:

- contexto 0: **-0.010**
- contexto 1: **+0.215**
- contexto 2: **-0.118**

## Interpretación

V28 impone una restricción a V24–V27:

> El efecto direccional del estado **no está demostrado como invariante al contexto** cuando memory/pressure del receptor cambian mediante historias distintas.

Es un límite mecanístico útil. Indica que la geometría medida está acoplada al contexto dinámico local y no funciona como un código incondicional independiente del contexto.

## Límite

V28 no establece consciencia, experiencia subjetiva ni sentiencia. Establece una limitación sobre la transportabilidad de la representación computacional probada.

## Próximo

V29 aísla variables auxiliares una por una: estado del receptor fijo mientras se cambia únicamente contexto de memory o pressure, midiendo directamente affinity antipodal.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V28 — Context Dependence / Transport Test

## Status
**SUCCESS** — GitHub Actions run 36786588699 (corrected isorradial version).

## Important analysis note
The original V28 identity column at radius 0 is not a valid 50% null because exact zero affinity maps to sign(0)=0 and is counted as incorrect for either donor. The 0° condition at radius 1.1 is also a built-in local-reference control: the transformed donor state exactly reproduces its own local reference state, so 100% identity is tautological.

The informative V28 quantities are therefore the off-axis conditions, especially signed affinity at 90° and 180°.

## Design
- 6 fixed V12 blind parameter points.
- 4 history pairs.
- seeds 30–39.
- 3 receiver histories: zero-history, all-positive history, and independent random-sign history.
- Future input exactly zero.
- Donor state geometry radius 1.1 at 0°, 90°, 180°.
- Receiver memory and pressure come from the selected receiver history.
- Local A/B reference continuations are generated within each receiver context.

## Result

| Receiver context | 0° | 90° | 180° |
|---|---:|---:|---:|
| zero-history | 100.0% | 38.75% | 43.13% |
| all-positive | 100.0% | 49.38% | 51.46% |
| random-sign | 100.0% | 42.29% | 39.58% |

The 0° result is the expected local-reference control and is not a discovery. The 90°/180° results do not reproduce the strong antipodal inversion seen in the common-midpoint protocol.

Signed affinity at 180°: context 0 **-0.010**, context 1 **+0.215**, context 2 **-0.118**.

## Interpretation

V28 constrains V24–V27:

> The directional state effect is **not demonstrated to be context-invariant** when receiver memory/pressure context is changed through distinct histories.

This is a useful mechanistic boundary. It indicates the measured geometry is coupled to local dynamic context rather than functioning as an unconditional context-free code.

## Boundary

V28 does not establish consciousness, subjective experience, or sentience. It establishes a limitation on transportability of the tested computational state representation.

## Next

V29 isolates nuisance variables one at a time: receiver state held fixed while memory-only or pressure-only context is changed, with antipodal affinity measured directly.

</details>