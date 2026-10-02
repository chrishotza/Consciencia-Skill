# Skill-Conscious Server Contract

This document defines the stable boundary for a future HTTP or MCP server.

The server is a transport layer around the organism. It must not contain research logic that belongs in `src/ontto/` or `research/`.

## Core principle

```
Agent Skill
    ↓
server / MCP
    ↓
PersistentOrganism
    ↓
storage + provider
```

The Agent Skill describes **when and how** an agent should use the organism.

The server exposes **controlled operations**.

The organism remains the source of runtime behavior.

## Canonical operations

| Operation | Purpose | Mutation |
|---|---|---|
| `health` | Service/process health | no |
| `status` | Current organism status | no |
| `submit_input` | Queue external input | yes |
| `wake` | Execute one WAKE cycle | yes |
| `dream` | Execute one SLEEP/DREAM cycle | yes |
| `recent_memory` | Read bounded recent memory | no |
| `recent_events` | Read bounded recent events | no |
| `state_summary` | Read a safe state summary | no |
| `self_observer_summary` | Read bounded self-model metadata | no |

## Required boundaries

### No arbitrary database access

Clients must not receive raw SQL access or arbitrary table mutation.

### Bounded reads

Memory, events, state summaries, and evidence responses must have explicit limits.

### Explicit mutations

Wake, dream, input submission, and future learning operations must be explicit operations.

### Auditability

Each mutation should produce an auditable event containing:

- agent id;
- operation;
- request id;
- timestamp;
- result status.

### Reproducibility

Research experiments remain repository workflows. A production server should not silently mutate research protocols.

## Suggested request model

Every mutation should accept:

```json
{
  "agent_id": "consciencia-001",
  "request_id": "unique-id",
  "payload": {}
}
```

`request_id` should support idempotency for operations where duplicate execution would be harmful.

## Suggested response model

```json
{
  "ok": true,
  "agent_id": "consciencia-001",
  "operation": "wake",
  "request_id": "unique-id",
  "data": {},
  "error": null
}
```

## MCP mapping

If exposed through MCP, keep tool names aligned with the canonical operations:

- `skill_conscious_health`
- `skill_conscious_status`
- `skill_conscious_submit_input`
- `skill_conscious_wake`
- `skill_conscious_dream`
- `skill_conscious_recent_memory`
- `skill_conscious_recent_events`
- `skill_conscious_state_summary`
- `skill_conscious_self_observer_summary`

The Agent Skill should reference the tool contract rather than embedding transport-specific implementation details.

## Deployment modes

### Local
Agent Skill + local Python organism.

### Server
Agent Skill + remote API/MCP + persistent organism service.

### Hybrid
Agent runs locally while the organism and storage live on a private server.

## Security baseline

The future server must add authentication, authorization, request limits, bounded payloads, secret isolation, structured audit logging, and explicit control over which operations can mutate organism state.

## Compatibility rule

Do not let server-specific names leak into the research core.

The stable boundary is:

`server operation` → `organism method`

not:

`server operation` → `research implementation`.


<details>
<summary>🇪🇸 Español — abrir</summary>

# Contrato del servidor Skill-Conscious

Este documento define el límite estable para un servidor HTTP o MCP futuro.
El servidor es una capa de transporte alrededor del organismo. No debe contener lógica de investigación que pertenezca a src/ontto/ o research/.

## Principio central
```
Agent Skill
    ↓
server / MCP
    ↓
PersistentOrganism
    ↓
storage + provider
```

El Agent Skill describe cuándo y cómo usar el organismo. El servidor expone operaciones controladas. El organismo sigue siendo la fuente del comportamiento de runtime.

## Operaciones canónicas
| Operación | Propósito | Mutación |
|---|---|---|
| health | salud del proceso | no |
| status | estado actual | no |
| submit_input | encolar entrada externa | sí |
| wake | ejecutar un ciclo WAKE | sí |
| dream | ejecutar un ciclo SLEEP/DREAM | sí |
| recent_memory | leer memoria reciente acotada | no |
| recent_events | leer eventos recientes acotados | no |
| state_summary | resumen seguro del estado | no |
| self_observer_summary | metadatos acotados del modelo de sí | no |

## Límites
Sin acceso SQL arbitrario; lecturas acotadas; mutaciones explícitas; eventos auditables; experimentos de investigación separados de los workflows de producción.

## Modos de despliegue
Local: Agent Skill + organismo Python local.
Server: Agent Skill + API/MCP + servicio de organismo persistente.
Hybrid: agente local y organismo/storage en servidor privado.

## Seguridad
El servidor futuro debe agregar autenticación, autorización, límites de requests, payloads acotados, aislamiento de secretos, logging estructurado y control explícito de operaciones mutables.

## Regla de compatibilidad
No permitir que nombres específicos del servidor se filtren al núcleo de investigación.
La frontera estable es server operation → organism method.

</details>


<details>
<summary>🇪🇸 Español — abrir</summary>

# Contrato del servidor Skill-Conscious

Este documento define el límite estable para un servidor HTTP o MCP futuro. El servidor es una capa de transporte alrededor del organismo y no debe contener lógica de investigación de src/ontto/ o research/.

## Principio central
Agent Skill → server / MCP → PersistentOrganism → storage + provider.
El Agent Skill describe cuándo y cómo usar el organismo. El servidor expone operaciones controladas. El organismo sigue siendo la fuente del comportamiento.

## Operaciones canónicas
health; status; submit_input; wake; dream; recent_memory; recent_events; state_summary; self_observer_summary.
Las operaciones de lectura son acotadas y las mutaciones explícitas.

## Límites
Sin acceso SQL arbitrario. Lecturas acotadas. Mutaciones explícitas. Auditoría de cambios. Los experimentos de investigación siguen siendo workflows del repositorio y no deben ser mutados silenciosamente por el servidor de producción.

## Despliegue
Local: Agent Skill + organismo Python local. Server: Agent Skill + API/MCP + organismo persistente. Hybrid: agente local y organismo/storage en servidor privado.

## Seguridad
El servidor futuro debe agregar autenticación, autorización, límites de requests, payloads acotados, aislamiento de secretos, logging estructurado y control explícito de operaciones mutables.

## Compatibilidad
No permitir que nombres específicos del servidor se filtren al núcleo de investigación. La frontera estable es operación de servidor → método del organismo.

</details>
