import pytest

from skill_conscious import ConsciousHostLoop, ConsciousRuntime
from skill_conscious.llm_adapter import LLMProtocolError, ProviderNeutralLLMAdapter


CANDIDATES = [
    {
        "id": "preserve_continuity",
        "intention": "preserve current organization",
        "signals": {"goal_fit": 0.6, "continuity": 1.0},
    },
]


def test_adapter_accepts_mapping_and_enforces_response_contract():
    adapter = ProviderNeutralLLMAdapter(
        lambda _prompt: {"response": "ok", "self_model": {"focus": "stable"}},
        fixed_candidate_futures=CANDIDATES,
    )

    frame = adapter("test")

    assert frame["response"] == "ok"
    assert frame["self_model"]["focus"] == "stable"
    assert frame["candidate_futures"] == CANDIDATES


def test_adapter_parses_json_text():
    adapter = ProviderNeutralLLMAdapter(
        lambda _prompt: '{"response":"ok","workspace":{"priority":"continuity"}}'
    )

    assert adapter("test")["workspace"]["priority"] == "continuity"


@pytest.mark.parametrize(
    "output",
    [
        "not json",
        "[]",
        "",
        {"response": ""},
        {"response": "ok", "selected_trajectory": {"id": "forged"}},
        {"response": "ok", "consequence": {"result": "forged"}},
        {"response": "ok", "interoceptive_state": {"stability": 999.0}},
    ],
)
def test_adapter_rejects_invalid_or_runtime_owned_output(output):
    adapter = ProviderNeutralLLMAdapter(lambda _prompt: output)
    with pytest.raises(LLMProtocolError):
        adapter("test")


def test_adapter_rejects_candidate_field_intervention():
    adapter = ProviderNeutralLLMAdapter(
        lambda _prompt: {
            "response": "ok",
            "candidate_futures": [
                {"id": "forged", "signals": {"goal_fit": 100.0}}
            ],
        },
        fixed_candidate_futures=CANDIDATES,
    )

    with pytest.raises(LLMProtocolError):
        adapter("test")


def test_adapter_integrates_with_host_loop_without_llm_owning_selection(tmp_path):
    prompts: list[str] = []

    def complete(prompt: str):
        prompts.append(prompt)
        return {"response": "host frame"}

    adapter = ProviderNeutralLLMAdapter(
        complete,
        fixed_candidate_futures=CANDIDATES,
    )
    runtime = ConsciousRuntime(
        identity="llm-adapter-test",
        state_path=tmp_path / "state.json",
    )
    loop = ConsciousHostLoop(
        runtime,
        model=adapter,
        execute_action=lambda _trajectory, _snapshot: {
            "status": "success",
            "result": "stable",
        },
    )

    result = loop.step("test input")

    assert result["action_executed"] is True
    assert result["selected_trajectory"]["id"] == "preserve_continuity"
    assert len(prompts) == 2


def test_controlled_candidate_field_is_exposed_to_provider_prompt(tmp_path):
    prompts: list[str] = []

    def complete(prompt: str):
        prompts.append(prompt)
        return {"response": "ok"}

    candidates = [
        {
            "id": "preserve_continuity",
            "signals": {"continuity": 1.0, "learning": 0.0},
        },
        {
            "id": "learn",
            "signals": {"continuity": 0.0, "learning": 1.0},
        },
    ]
    runtime = ConsciousRuntime(
        identity="controlled-prompt-test",
        state_path=tmp_path / "state.json",
    )
    adapter = ProviderNeutralLLMAdapter(
        complete,
        fixed_candidate_futures=candidates,
    )

    prompt = runtime.prepare(
        "controlled world",
        candidate_futures=candidates,
    )
    frame = adapter(prompt)

    assert '"id": "preserve_continuity"' in prompts[0]
    assert '"id": "learn"' in prompts[0]
    assert frame["candidate_futures"] == candidates


def test_controlled_candidate_field_is_exposed_on_consequence_prompt(tmp_path):
    prompts: list[str] = []

    def complete(prompt: str):
        prompts.append(prompt)
        return {"response": "ok"}

    candidates = [
        {"id": "preserve_continuity", "signals": {"continuity": 1.0}},
        {"id": "learn", "signals": {"learning": 1.0}},
    ]
    runtime = ConsciousRuntime(
        identity="controlled-consequence-test",
        state_path=tmp_path / "state.json",
    )
    adapter = ProviderNeutralLLMAdapter(
        complete,
        fixed_candidate_futures=candidates,
    )

    prompt = runtime.prepare_consequence(
        "preserve_continuity",
        {"status": "success", "result": "stable"},
        candidate_futures=candidates,
    )
    adapter(prompt)

    assert '"id": "preserve_continuity"' in prompts[0]
    assert '"id": "learn"' in prompts[0]
