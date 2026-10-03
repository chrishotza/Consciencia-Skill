# Provider-Neutral LLM Adapter

The LLM adapter is the boundary between an external language model and the persistent Skill-Conscious runtime.

## Contract

~~~text
EXTERNAL PROVIDER
       ↓
LLM COMPLETION
       ↓
JSON / MAPPING NORMALIZATION
       ↓
FRAME VALIDATION
       ↓
RUNTIME
~~~

The provider is deliberately not part of the runtime. A completion callable can wrap a hosted API, a local model, or another inference service.

The adapter enforces three boundaries:

1. The model must return a non-empty `response`.
2. Runtime-owned fields such as `selected_trajectory`, action history, and metacognitive runtime state cannot be written directly by the model.
3. A benchmark may provide a fixed candidate-future field. When it does, the model cannot replace that field.

The third rule is important for longitudinal experiments: the same candidate field, action boundary, authoritative outcomes, restart schedule, and metrics can be held constant while changing only the model provider or runtime condition.

This is an integration boundary, not a consciousness detector and not a claim that an external LLM becomes phenomenally conscious by using the runtime.


## Example

~~~python
from skill_conscious import ConsciousHostLoop, ConsciousRuntime
from skill_conscious.llm_adapter import ProviderNeutralLLMAdapter

adapter = ProviderNeutralLLMAdapter(provider_complete)
loop = ConsciousHostLoop(
    ConsciousRuntime(identity='agent', state_path='data/agent.json'),
    model=adapter,
    execute_action=execute_action,
)
~~~

`provider_complete` is the only provider-specific layer.

## Causal A/B probe

The repository also includes a deterministic provider A/B experiment:

~~~bash
python -m experiments.llm_longitudinal_benchmark --cycles 8 --restart-every 4
~~~

The probe creates two matched branches from the same runtime seed and exposes the same candidate-future field and outcome rule. The only experimental variable is the provider-authored persistent self-model:

~~~text
Provider A → continuity weight = 3, learning weight = 0
Provider B → continuity weight = 0, learning weight = 3
~~~

The runtime, not the provider, performs trajectory scoring and selection. A valid causal result is therefore:

~~~text
same initial state
      +
same candidate futures
      +
same outcome function
      +
different provider self-model
      ↓
different runtime trajectory
      ↓
different downstream state
~~~

This is a mechanism-level causal test. It does not establish phenomenal consciousness.

