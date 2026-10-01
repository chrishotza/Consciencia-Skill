# C0.3 — Information-Matched Causal Self-Reference Control

## Objetivo

C0.2 mostró que la acción seleccionada cambia cuando el estado propio se enmascara. C0.3 pregunta algo más exigente:

> ¿la política es específicamente sensible a su estado propio actual, o simplemente responde a valores de estado con una sensibilidad que también aparece cuando se le presentan estados ajenos con la misma distribución empírica?

El control preserva el mismo snapshot de política y la misma distribución de estados observada en las trayectorias FULL, pero rompe la correspondencia entre el episodio y el estado que recibe la política.

## Diseño

Se generan 64 trayectorias FULL con el mismo entrenamiento base de C0.2.

Para cada episodio:

1. se calcula la acción con el estado propio real;
2. se calcula la acción con un estado tomado de otro episodio mediante una permutación sin puntos fijos;
3. se repite el paso con una segunda permutación independiente;
4. se compara la brecha real-versus-mezclada con la brecha entre dos estados mezclados.

El contraste por réplica es:

\[
\Delta_i =
|a(s_i)-a(s_{\pi_1(i)})|
-
|a(s_{\pi_1(i)})-a(s_{\pi_2(i)})|.
\]

Una media positiva indica que la acción cambia más cuando se sustituye el estado propio actual que cuando se intercambian dos estados ajenos extraídos de la misma distribución. La prueba de signo por permutación se aplica al vector \(\Delta\).

## Controles

- mismo autoobservador;
- misma política entrenada;
- mismo snapshot durante toda la sonda;
- sin entrada semántica;
- sin reentrenamiento externo;
- estados de control tomados de la distribución empírica de las propias trayectorias.

## Límite

C0.3 fortalece la atribución causal de la acción al estado propio bajo esta sonda, pero sigue siendo una propiedad operacional del sistema. No demuestra experiencia fenomenal.

## Resultado auditado

Run GitHub Actions `36838675864`; artifact `11150238362`; commit `413e70499977d759e9effb50505c4db6174925c8`.

- brecha estado propio → estado mezclado: **1.06640625**;
- brecha entre dos estados mezclados: **1.00000000**;
- contraste: **+0.06640625**;
- p por permutación de signo: **0.3140343**;
- discrepancia de acción real vs. estado mezclado: **0.5332031**.

Interpretación: el control información-matcheado no mostró una separación estadísticamente detectable entre sensibilidad al estado propio actual y sensibilidad a estados ajenos extraídos de la misma distribución empírica. C0.3, por tanto, no confirma una dependencia causal específicamente propia del episodio bajo este criterio más exigente.

## Estado

**Ejecutado y archivado.** El resultado debe tratarse como control de especificidad causal para C3, no como puntuación global de conciencia.
