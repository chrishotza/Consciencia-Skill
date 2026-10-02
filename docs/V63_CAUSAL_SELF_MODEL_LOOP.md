<a id="espanol"></a>

# V63 — Bucle causal del modelo de sí

## Resultado

24 réplicas emparejadas × 32 ciclos de evaluación en cuatro brazos.

Con el puente del modelo de sí ON:

- regret medio del modelo de sí: 0.1422226601;
- regret medio del control aleatorio: 0.2666042539;
- ventaja de regret aleatorio − modelo de sí: 0.1243815939;
- p emparejada por cambio de signo: 0.00005;
- tasa de aciertos del oráculo del modelo de sí: 60.6771%;
- tasa de aciertos del control aleatorio: 33.8542%.

Para el brazo de selección mediante modelo de sí:

- regret medio con puente OFF: 0.2876865581;
- regret medio con puente ON: 0.1422226601;
- mejora de regret OFF − ON: 0.1454638980;
- p emparejada por cambio de signo: 0.00005;
- tasa de aciertos del oráculo: 10.0260% → 60.6771%;
- p emparejada por cambio de signo para el cambio de tasa de aciertos: 0.00005.

La diferencia de diferencias de regret entre los brazos con modelo de sí y aleatorio fue 0.2837493367, con p emparejada por cambio de signo = 0.00005.

La cobertura de acciones alcanzó el 100% de las réplicas para puente ON + modelo de sí, puente OFF + aleatorio y puente ON + aleatorio; puente OFF + modelo de sí alcanzó 66.67%.

Para puente ON + modelo de sí, la señal del puente causal condicionada por acción se observó después de ambas ramas. Entre 243 observaciones posteriores a -1 y 501 posteriores a +1, las señales medias fueron aproximadamente +0.4999 y -0.2406, respectivamente, con diferencia absoluta 0.7405. Esto es una asociación dentro del bucle, no una estimación causal aislada.

## Interpretación

V62 mostró la transducción causal en un paso de la autorrepresentación semántica hacia el estado numérico. V63 extiende esa vía a un bucle recurrente condicionado por acciones:

```
trayectoria previa
    →
siguiente modelo de sí
    →
dinámica interna
    →
siguiente selección de trayectoria
```

El arnés determinista emparejado, por tanto, respalda un acoplamiento computacional recurrente entre la autorrepresentación semántica y la selección de trayectorias futuras.

## Límite de evidencia

El proveedor es determinista y sintético. Estos resultados establecen comportamiento computacional dentro del arnés probado; no establecen consciencia fenomenológica ni experiencia subjetiva.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V63 — Causal Self-Model Loop

## Result

Twenty-four paired replicates × 32 evaluation cycles across four arms.

With the self-model bridge ON:

- mean self-model regret: 0.1422226601;
- mean random-control regret: 0.2666042539;
- random − self-model regret advantage: 0.1243815939;
- paired sign-flip p-value: 0.00005;
- self-model oracle hit rate: 60.6771%;
- random-control oracle hit rate: 33.8542%.

For the self-model-selection arm:

- mean regret with bridge OFF: 0.2876865581;
- mean regret with bridge ON: 0.1422226601;
- OFF − ON regret improvement: 0.1454638980;
- paired sign-flip p-value: 0.00005;
- oracle hit rate: 10.0260% → 60.6771%;
- paired sign-flip p-value for the hit-rate change: 0.00005.

Difference-in-differences in regret between self-model and random arms: 0.2837493367, with paired sign-flip p = 0.00005.

Action coverage reached 100% of replicates for bridge ON + self-model, bridge OFF + random, and bridge ON + random; bridge OFF + self-model reached 66.67%.

For bridge ON + self-model, the causal-bridge signal conditioned on action appeared after both branches. Across 243 observations after -1 and 501 after +1, mean signals were approximately +0.4999 and -0.2406, with absolute difference 0.7405. This is an association inside the loop, not an isolated causal estimate.

## Interpretation

V62 showed one-step causal transduction from semantic self-representation into numerical state. V63 extends that pathway into an action-conditioned recurrent loop:

~~~text
prior trajectory
    →
next self-model
    →
internal dynamics
    →
next trajectory selection
~~~

The matched deterministic harness therefore supports recurrent computational coupling between semantic self-representation and future trajectory selection.

## Evidence boundary

The provider is deterministic and synthetic. The result establishes computational behavior within the tested harness; it does not establish phenomenal consciousness or subjective experience.

</details>