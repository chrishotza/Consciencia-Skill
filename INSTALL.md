# Installing Skill-Conscious

Skill-Conscious is designed to have two separately installable layers.

## 1. Agent Skill

The portable Agent Skill is:

`skills/skill-conscious/`

Its entrypoint is:

`skills/skill-conscious/SKILL.md`

Copy that folder into the skill directory supported by your AI agent.

The package is intentionally small. The agent should load references on demand rather than ingesting the entire research repository.

## 2. Python organism runtime

The repository also contains the persistent organism runtime.

Install the project in a Python environment:

```bash
pip install -e .
```

Run the existing daemon entrypoint:

```bash
skill-conscious
```

The legacy command `consciencia-organismo` remains available for compatibility.

## 3. Server mode

A future server distribution should keep the same boundary:

```
Agent Skill
    ↓
workflow / routing
    ↓
server or MCP
    ↓
PersistentOrganism
    ↓
storage + model provider
```

The server should expose controlled operations and status, while research protocols and evidence remain versioned in the repository.

## Design goal

One research core, multiple delivery surfaces:

- portable Agent Skill;
- local Python organism;
- server/MCP deployment.


<details>
<summary>🇺🇸 English — open</summary>

# Installing Skill-Conscious

Skill-Conscious is designed as two separately installable layers.

## 1. Agent Skill

The portable Agent Skill is:

`skills/skill-conscious/`

Its entrypoint is:

`skills/skill-conscious/SKILL.md`

Copy that folder into the skill directory supported by your AI agent.

The package is intentionally small. The agent should load references on demand instead of ingesting the entire research repository.

## 2. Python organism runtime

The repository also contains the persistent organism runtime.

Install the project in a Python environment:

```bash
pip install -e .
```

Run the existing daemon entrypoint:

```bash
skill-conscious
```

The legacy command `consciencia-organismo` remains available for compatibility.

## 3. Server mode

A future server distribution should keep the same boundary:

```
Agent Skill
    ↓
workflow / routing
    ↓
server or MCP
    ↓
PersistentOrganism
    ↓
storage + model provider
```

The server should expose controlled operations and status, while research protocols and evidence remain versioned in the repository.

## Design goal

One research core, multiple delivery surfaces:

- portable Agent Skill;
- local Python organism;
- server/MCP deployment.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
