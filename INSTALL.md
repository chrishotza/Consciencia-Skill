<a id="english"></a>

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

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Instalación de Skill-Conscious

Skill-Conscious está diseñado como dos capas instalables por separado.

## 1. Agent Skill

El Agent Skill portable se encuentra en:

`skills/skill-conscious/`

Su punto de entrada es:

`skills/skill-conscious/SKILL.md`

Copiá esa carpeta al directorio de skills compatible con tu agente de IA.

El paquete está pensado para ser pequeño. El agente debe cargar referencias bajo demanda en lugar de incorporar todo el repositorio de investigación.

## 2. Runtime Python del organismo

El repositorio también contiene el runtime del organismo persistente.

Instalá el proyecto en un entorno Python:

```bash
pip install -e .
```

Ejecutá el entrypoint del daemon existente:

```bash
skill-conscious
```

El comando heredado `consciencia-organismo` sigue disponible por compatibilidad.

## 3. Modo servidor

Una futura distribución de servidor debería conservar el mismo límite:

```
Agent Skill
    ↓
workflow / routing
    ↓
server o MCP
    ↓
PersistentOrganism
    ↓
storage + model provider
```

El servidor debe exponer operaciones y estado controlados, mientras los protocolos de investigación y la evidencia permanecen versionados en el repositorio.

## Objetivo de diseño

Un núcleo de investigación, múltiples superficies de entrega:

- Agent Skill portable;
- organismo Python local;
- despliegue server/MCP.

</details>

> 🌐 Language convention: [docs/LANGUAGE.md](docs/LANGUAGE.md)