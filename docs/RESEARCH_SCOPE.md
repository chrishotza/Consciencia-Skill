# Research Scope and System Boundary

## What the experimental system is

Skill-Conscious studies a **persistent AI organism runtime**. The core experimental substrate is the persistent computational system around an optional model provider:

    model/provider
          ↓
    PersistentOrganism
          ↓
    memory + internal state + self-model
          ↓
    self-observation + dynamics
          ↓
    trajectory / policy selection
          ↓
    persistent storage + reproducible protocol

The organism runtime is the object whose computational properties are measured.

## What the language model is

The repository supports an OpenAI-compatible provider, but the research program is not equivalent to testing ChatGPT, Claude, or another commercial assistant as a conscious subject.

Most experimental protocols operate on the repository's own numerical organism/runtime components. A separate live-provider smoke test checks that a real model can act as the cognitive provider while the runtime preserves memory, trajectory, and WAKE/SLEEP state across restart.

See [GitHub Lab](GITHUB_LAB.md) for the provider smoke test boundary.

## What the results establish

The protocols can establish computational properties under their stated conditions, for example:

- predictive accuracy;
- state persistence;
- trajectory-selection effects;
- causal effects of interventions;
- restart persistence;
- out-of-distribution behavior;
- failure or null effects under specified controls.

They do **not**, by themselves, establish subjective experience.

## Scientific claim boundary

The repository uses four distinct layers:

| Layer | Meaning |
|---|---|
| Observation | What an execution produced |
| Result | A reproducible pattern under a defined protocol |
| Hypothesis/model | An interpretation or mechanism that still requires testing |
| Ontology | Philosophical or metaphysical interpretation kept separate from computational evidence |

The theoretical documents may motivate engineering hypotheses, but passing an engineering or behavioral test does not validate the ontology automatically.

## What is and is not preregistered

The current repository contains protocol documents, explicit controls, seeds, artifacts, and workflow manifests, but the historical protocol set is not presented as one globally preregistered family.

Therefore:

1. a protocol-level p-value is interpreted under that protocol's own design;
2. repository-wide claims about all protocols require additional multiplicity control or a prespecified aggregate analysis;
3. future confirmatory protocols should record the primary endpoint, direction of effect, exclusion rules, replication plan, and analysis rule **before** the confirmatory execution.

The repository does not retroactively label historical experiments as preregistered when that status is not documented.

## Why this boundary exists

The project can be ambitious about the engineering problem while remaining conservative about what the measurements prove.

The goal is not to make the evidence sound smaller than it is. The goal is to make every claim traceable to the exact computational system, intervention, control, and analysis that produced it.
