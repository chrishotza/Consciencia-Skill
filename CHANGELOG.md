## 2026-10-02 — I5.22 verificado / I5.22 verified

- I5.22 corrected rerun: 24 replicates, seed **20261022**, 24 warmup, 15 cycles, 20,000 permutations.
- Workflow **37061263630**, artifact **11251161457**; tests **37061263638** and package check **37061263624** passed.
- All four invariants were preserved at 100%.
- Semantic specificity was null for signed AUC, absolute AUC, and future-action change; global lag×specificity interaction was non-significant for all three endpoints.
- Initial I5.22 integrity metric was discarded and replaced by the corrected run; only the corrected run is valid.
- Next: I5.23 cyclic shift sweep.

## 2026-10-02 — I5.21 verificado / I5.21 verified

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

- I5.21 repitió el control semántico con una permutación restringida dentro de cada ciclo de siete fases: **24 réplicas**, **24 warmup**, **15 ciclos**, seed **20261021**, **20.000 permutaciones**.
- Run **37059465725**, artifact **11249378346**; tests **37059465807** y paquete **37059465643** pasaron.
- Los invariantes t0, multiconjunto semántico global y multiconjunto de cada período se preservaron al 100%.
- Especificidad: AUC firmada nula; AUC absoluta y cambio de acción futura positivos.
- La interacción global lag×especificidad fue significativa para AUC absoluta y acción futura.
- Siguiente control: I5.22, desplazamiento cíclico semántico para preservar la estructura de transiciones.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

- I5.21 repeated the semantic control with a permutation restricted within each seven-phase cycle: **24 replicates**, **24 warmup cycles**, **15 cycles**, seed **20261021**, **20,000 permutations**.
- Run **37059465725**, artifact **11249378346**; tests **37059465807** and package check **37059465643** passed.
- t0, global semantic multiset, and within-period multiset invariants were all preserved at 100%.
- Specificity: signed AUC null; absolute AUC and future-action change positive.
- Global lag×specificity interaction was significant for absolute AUC and future action.
- Next control: I5.22, cyclic semantic phase-shift preserving transition structure.

</details>


