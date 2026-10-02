<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V57 — Protocolo de evidencia

**Estado: protocolo implementado; resultado empírico pendiente.**

Controles:

1. historia de warmup idéntica dentro de cada par;
2. conjunto candidato idéntico;
3. selector self-model y selector random parten de estados persistidos idénticos;
4. el oracle se calcula post hoc y no se expone durante la selección;
5. las diferencias entre réplicas emparejadas se evalúan con test de permutación sign-flip;
6. se conservan las predicciones candidatas crudas y los estados realizados.

## Límite de evidencia

V57 prueba la utilidad causal de un self-model interno para seleccionar futuras trayectorias.

</details>

<a id="english"></a>

# V57 — Evidence Protocol

**Status: protocol implemented; empirical result pending.**

Controls:

1. identical warmup history within each pair;
2. identical candidate set;
3. self-model selector and random selector start from identical persisted states;
4. oracle is computed post hoc and is not exposed during selection;
5. paired replicate differences are evaluated with a sign-flip permutation test;
6. raw candidate predictions and realized states are retained.

Evidence boundary:

V57 tests causal utility of an internal self-model for future trajectory selection.