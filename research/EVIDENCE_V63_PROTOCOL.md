<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V63 — Bucle causal del self-model

## Hipótesis

Un self-model semántico generado desde la trayectoria previa del organismo puede convertirse en una variable causalmente activa dentro de un loop computacional recurrente: puede alterar la dinámica interna mediante el self-model bridge y el estado alterado puede afectar la futura selección de trayectorias.

## Diseño

24 réplicas emparejadas × 32 ciclos de evaluación.

Cuatro brazos parten de un estado warmup clonado:

- selección self-model + bridge OFF;
- selección self-model + bridge ON;
- selección random + bridge OFF;
- selección random + bridge ON.

El provider mapea la acción seleccionada previamente al siguiente SELF_MODEL semántico. Semantic MEMORY se mantiene constante y no se enruta por el dynamic bridge.

## Endpoints primarios

1. regret self-model vs random con self-model bridge ON;
2. mejora de regret OFF→ON bajo selección self-model;
3. diferencias paired de oracle-hit;
4. difference-in-differences factorial de regret.

## Artifact exitoso

Workflow: organism-causal-self-model-loop-v63  
Artifact: organism-causal-self-model-loop-v63  
Réplicas: 24

Valores clave:

- regret self-model bridge-ON: 0.1422226601;
- regret random bridge-ON: 0.2666042539;
- advantage random-minus-self: 0.1243815939;
- mejora de regret bridge OFF→ON bajo self-model: 0.1454638980;
- difference-in-differences de regret: 0.2837493367;
- cambio oracle-hit bridge OFF→ON del self-model: +0.5065104167;
- p-values sign-flip para efectos principales/interacción: 0.00005.

## Limitaciones

El provider es determinista y sintético. La comparación de feedback signal es una asociación intra-run, no un efecto causal aislado, porque historia de acciones y estado interno coevolucionan.

El artifact establece comportamiento computacional en el arnés especificado. No establece consciencia fenomenológica ni experiencia subjetiva.

</details>

<a id="english"></a>

# Evidence V63 — Causal self-model loop

## Hypothesis

A semantic self-model generated from the organism's prior trajectory can become a causally active variable in a recurrent computational loop: it can alter internal dynamics through the self-model bridge, and the altered state can affect future trajectory selection.

## Design

24 matched replicates × 32 evaluation cycles.

Four arms start from cloned warmup state:
- self-model selection + bridge OFF;
- self-model selection + bridge ON;
- random selection + bridge OFF;
- random selection + bridge ON.

The provider maps the previous selected action to the next semantic SELF_MODEL. Semantic MEMORY is held constant and is not routed through the dynamic bridge.

## Primary endpoints

1. self-model vs random regret with the self-model bridge ON;
2. bridge OFF vs ON regret under self-model selection;
3. paired oracle-hit differences;
4. factorial difference-in-differences for regret.

## Successful artifact

Workflow: organism-causal-self-model-loop-v63
Artifact: organism-causal-self-model-loop-v63
Replicates: 24

Key values:
- bridge-ON self-model regret: 0.1422226601;
- bridge-ON random regret: 0.2666042539;
- random-minus-self regret advantage: 0.1243815939;
- bridge OFF→ON regret improvement under self-model: 0.1454638980;
- regret difference-in-differences: 0.2837493367;
- self-model bridge OFF→ON oracle-hit change: +0.5065104167;
- paired sign-flip p-values for the main effects/interaction: 0.00005.

## Limitations

The provider is deterministic and synthetic. The feedback signal comparison is a within-run association, not an isolated causal estimate, because action history and internal state co-evolve.

The artifact establishes computational behavior in the specified harness. It does not establish phenomenological consciousness or subjective experience.
