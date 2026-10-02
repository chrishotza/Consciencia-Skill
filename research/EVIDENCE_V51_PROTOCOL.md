<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V51 — Protocolo de evidencia

**Estado: protocolo implementado; resultado empírico pendiente hasta inspeccionar CI y artifacts LIVE.**

Controles requeridos:

1. la predicción usa solo observables previos y persistidos del organismo;
2. el estado siguiente real se mantiene oculto hasta después de la predicción;
3. el baseline de persistencia se calcula desde el estado anterior a la transición;
4. el modelo observer sobrevive a un reinicio de SQLite;
5. los snapshots posteriores al reinicio siguen acumulándose sin resetear el modelo;
6. el test sign-flip evalúa si la ganancia es sistemáticamente distinta de cero.

## Límite de evidencia

Superar V51 respalda la existencia de un modelo autopredictivo operacional del organismo.

No establece awareness fenomenológico.

</details>

<a id="english"></a>

# V51 — Evidence Protocol

**Status: protocol implemented; empirical result pending until CI and live artifacts are inspected.**

Required controls:

1. prediction uses only prior persisted organism observables;
2. actual next state is withheld until after prediction;
3. persistence baseline is computed from the pre-transition state;
4. observer model survives SQLite restart;
5. post-restart snapshots continue accumulating without resetting the model;
6. sign-flip test evaluates whether gain is systematically different from zero.

Evidence boundary:

Passing V51 supports the existence of an operational self-predictive model in the
organism. It does not establish phenomenological awareness.