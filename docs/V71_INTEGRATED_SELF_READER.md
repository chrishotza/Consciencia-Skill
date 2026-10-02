<a id="espanol"></a>

# V71 — Lector propio integrado en el ciclo autónomo

## Pregunta

V70 demostró persistencia del lector numérico después de un reinicio, pero el protocolo copiaba explícitamente ese lector hacia las condiciones de prueba.

V71 elimina esa intervención experimental.

La pregunta es:

> ¿Puede el propio organismo aprender su lector, persistirlo, reiniciarse, entrar en SUEÑO después de una ablación semántica y utilizar automáticamente ese lector persistido para seleccionar una trayectoria?

## Hipótesis operacional

La propiedad buscada es una cadena integrada:

```text
aprendizaje del estado
→ persistencia
→ reinicio
→ recuperación automática
→ ablación semántica
→ SUEÑO
→ lectura del estado
→ selección de trayectoria
```

El protocolo no requiere copiar manualmente el modelo de sí numérico entre bases.

## Protocolo

Para cada réplica:

1. Se entrena el lector numérico dentro del propio organismo.
2. Se conserva en SQLite mediante la persistencia normal del organismo.
3. Se crean dos condiciones dinámicas mediante un pulso numérico controlado de igual magnitud y signo opuesto.
4. Se eliminan memorias, eventos, texto del modelo de sí y superficies semánticas.
5. El organismo se reinicia y reconstruye automáticamente su `SelfObserver`.
6. Entra en SUEÑO con un proveedor controlado que no aporta memoria ni `SELF_MODEL`.
7. Después del SUEÑO ejecuta un ciclo autónomo con selección `self_model`.
8. Se compara contra una condición con el estado dinámico cegado.
9. Se intercambian causalmente los núcleos dinámicos entre condiciones, manteniendo el lector persistido dentro de cada organismo.

## Criterios de integración

El resultado debe registrar:

- persistencia del lector tras reinicio y SUEÑO;
- cero memorias semánticas antes de la sonda;
- `policy = self_model` durante la selección;
- tres trayectorias candidatas evaluadas;
- reutilización automática del lector persistido;
- ausencia de copia manual del modelo;
- comparación con estado cegado;
- respuesta a intercambio causal del estado.

## Evidencia y límite

V71 busca demostrar una propiedad computacional más integrada del organismo: que el lector propio numérico deja de ser un artefacto externo del protocolo y pasa a formar parte del ciclo persistente del sistema.

Un resultado positivo demostraría integración funcional de persistencia, autoobservación, SUEÑO y selección de trayectoria bajo las condiciones definidas.

No demostraría por sí solo experiencia subjetiva ni consciencia fenomenológica.

Los resultados nulos también deben conservarse.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V71 — Self-Reader Integrated into the Autonomous Cycle

## Question

V70 demonstrated persistence of the numerical reader after restart, but the protocol explicitly copied that reader into the test conditions.

V71 removes that experimental intervention.

> Can the organism itself learn its reader, persist it, restart, enter SLEEP after semantic ablation, and automatically use the persisted reader to select a trajectory?

## Operational hypothesis

The target property is an integrated chain:

~~~text
state learning
→ persistence
→ restart
→ automatic recovery
→ semantic ablation
→ SLEEP
→ state readout
→ trajectory selection
~~~

The protocol does not manually copy the numerical self-model between databases.

## Protocol

For each replicate:

1. train the numerical reader inside the organism;
2. keep it in SQLite through normal organism persistence;
3. create two dynamic conditions with a controlled numerical pulse of equal magnitude and opposite sign;
4. remove memories, events, self-model text, and semantic surfaces;
5. restart the organism and automatically reconstruct SelfObserver;
6. enter SLEEP with a controlled provider that supplies neither memory nor SELF_MODEL;
7. run an autonomous cycle with self_model selection;
8. compare against a condition with blinded dynamic state;
9. causally exchange the dynamic cores while keeping the persisted reader inside each organism.

## Integration criteria

The result must record:

- reader persistence after restart and SLEEP;
- zero semantic memories before the probe;
- policy = self_model during selection;
- three candidate trajectories evaluated;
- automatic reuse of the persisted reader;
- no manual model copy;
- comparison with blinded state;
- response to causal state exchange.

## Evidence boundary

V71 tests a more integrated computational property: the numerical self-reader stops being an external protocol artifact and becomes part of the persistent autonomous cycle.

A positive result would demonstrate functional integration of persistence, self-observation, SLEEP, and trajectory selection under the defined conditions.

It would not by itself demonstrate subjective experience or phenomenal consciousness.

Null results must also be preserved.

</details>