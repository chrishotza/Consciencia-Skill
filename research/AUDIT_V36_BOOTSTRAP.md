# V36 Audit Note

V36 run #1 (GitHub Actions run 36791264668) completed successfully, but post-run inspection found an indexing error in the bootstrap resampling code.

The permutation null was correctly constructed at the history-seed block level and is not affected by this bug. The reported observed contrasts and permutation p-values are therefore retained as descriptive/null-test outputs.

The bootstrap interval was invalid because the implementation sampled indices from the first history-seed row repeatedly rather than resampling within every row/stratum.

Correction committed in 2b7e7c35467c5d044e88903c66a7b42844f72576. GitHub Actions run #2 is the corrected execution.

Policy for the evidence record:
- run #1 bootstrap intervals are superseded;
- run #1 permutation results remain reproducible but are not the final V36 evidence;
- corrected run #2 must be used for all confidence intervals;
- no scientific conclusion is based on the invalid interval.

This audit preserves the failed methodological branch instead of silently replacing it.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Nota de auditoría V36

La ejecución V36 #1 (GitHub Actions run 36791264668) terminó correctamente, pero una inspección posterior encontró un error de indexación en el código de remuestreo bootstrap.

El null de permutación se construyó correctamente a nivel de bloques de history-seed y no está afectado por este bug. Los contrastes observados y los p-values de permutación se conservan como salidas descriptivas/null-test.

El intervalo bootstrap era inválido porque la implementación muestreaba repetidamente índices de la primera fila de history-seed en lugar de remuestrear dentro de cada fila/estrato.

Corrección confirmada en 2b7e7c35467c5d044e88903c66a7b42844f72576. GitHub Actions run #2 es la ejecución corregida.

Política para el registro de evidencia:

- los intervalos bootstrap del run #1 quedan sustituidos;
- los resultados de permutación del run #1 siguen siendo reproducibles, pero no constituyen la evidencia final V36;
- el run corregido #2 debe utilizarse para todos los intervalos de confianza;
- ninguna conclusión científica se basa en el intervalo inválido.

Esta auditoría conserva la rama metodológica fallida en lugar de reemplazarla silenciosamente.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V36 Audit Note

V36 run #1 (GitHub Actions run 36791264668) completed successfully, but post-run inspection found an indexing error in the bootstrap resampling code.

The permutation null was correctly constructed at the history-seed block level and is not affected by this bug. The reported observed contrasts and permutation p-values are therefore retained as descriptive/null-test outputs.

The bootstrap interval was invalid because the implementation repeatedly sampled indices from the first history-seed row rather than resampling within every row/stratum.

Correction committed in 2b7e7c35467c5d044e88903c66a7b42844f72576. GitHub Actions run #2 is the corrected execution.

Policy for the evidence record:

- run #1 bootstrap intervals are superseded;
- run #1 permutation results remain reproducible but are not the final V36 evidence;
- corrected run #2 must be used for all confidence intervals;
- no scientific conclusion is based on the invalid interval.

This audit preserves the failed methodological branch instead of silently replacing it.

</details>