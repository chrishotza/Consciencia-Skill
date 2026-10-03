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

