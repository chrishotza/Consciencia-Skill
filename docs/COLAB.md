# Colab

## Experimento 01

Abrir el [cuaderno de referencia de continuidad](https://colab.research.google.com/github/chrishotza/Consciencia-Skill/blob/main/notebooks/01_continuity_baseline.ipynb).

Clona el repositorio público y ejecuta el motor relacional actual.

## Experimento 02

El cuaderno de API en vivo utiliza un proveedor LLM real y estado persistente en SQLite.

Colab se utiliza como laboratorio, no como anfitrión permanente 24/7. Un organismo continuo necesita un entorno de ejecución persistente fuera de los límites normales de las sesiones de cuaderno.

## Secretos

Guardar las credenciales de API en **Colab Secrets**. Nunca subir claves a GitHub.

Requeridos:

- `ONTTO_API_KEY`
- `ONTTO_MODEL`

Opcionales:

- `ONTTO_API_BASE_URL`
- `ONTTO_AGENT_ID`

## Evidencia

Cada ejecución en vivo debe conservar:

- semilla y configuración;
- modelo y proveedor;
- ciclos de VIGILIA;
- ciclos de SUEÑO;
- snapshots del estado;
- memorias;
- telemetría de tokens/costo cuando el proveedor la exponga.


<details>
<summary>🇺🇸 English — open</summary>

# Colab

## Experiment 01
Open the [continuity reference notebook](https://colab.research.google.com/github/chrishotza/Consciencia-Skill/blob/main/notebooks/01_continuity_baseline.ipynb). Clone the public repository and run the current relational engine.

## Experiment 02
The live API notebook uses a real LLM provider and persistent SQLite state.
Colab is a laboratory, not a permanent 24/7 host. A continuous organism needs a persistent execution environment outside normal notebook session limits.

## Secrets
Store API credentials in **Colab Secrets**. Never upload keys to GitHub.
Required:
- ONTTO_API_KEY
- ONTTO_MODEL
Optional:
- ONTTO_API_BASE_URL
- ONTTO_AGENT_ID

## Evidence
Every live run should preserve:
- seed and configuration;
- model and provider;
- WAKE cycles;
- SLEEP cycles;
- state snapshots;
- memories;
- token/cost telemetry when exposed by the provider.

</details>

> Language convention: docs/LANGUAGE.md

<details>
<summary>🇺🇸 English — open</summary>

# Colab

## Experiment 01
Open the continuity reference notebook. Clone the public repository and run the current relational engine.

## Experiment 02
The live API notebook uses a real LLM provider and persistent SQLite state.
Colab is a laboratory, not a permanent 24/7 host. A continuous organism needs a persistent execution environment outside normal notebook session limits.

## Secrets
Store API credentials in Colab Secrets. Never upload keys to GitHub.
Required:
- ONTTO_API_KEY
- ONTTO_MODEL
Optional:
- ONTTO_API_BASE_URL
- ONTTO_AGENT_ID

## Evidence
Every live run should preserve seed/configuration, model/provider, WAKE cycles, SLEEP cycles, state snapshots, memories, and token/cost telemetry when exposed by the provider.

</details>

> Language convention: docs/LANGUAGE.md