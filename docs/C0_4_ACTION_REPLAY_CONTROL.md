# C0.4 — Information-Matched Action-Replay Control

## Objetivo

C0.4 ataca una ambigüedad de C0.2 en C5: la mayor varianza autónoma de FULL puede deberse simplemente a que FULL selecciona señales, mientras OPEN_LOOP fuerza señal cero.

El nuevo control conserva acciones provenientes del mismo organismo, pero rompe su correspondencia con el episodio actual.

## Diseño

Para cada episodio FULL se conserva:

- el contexto inicial;
- la secuencia de acciones seleccionadas durante 8 pasos;
- la trayectoria y su varianza.

El control toma una secuencia de acciones de otro episodio mediante una permutación sin puntos fijos y la reproduce desde el mismo contexto inicial y con la misma semilla dinámica.

La magnitud principal es:

\[
\Delta_i =
Var(x_i^{FULL})
-
Var(x_i^{REPLAY}).
\]

Se promedian 8 secuencias replay por episodio y se evalúa el vector \Delta con una prueba de signo por permutación.

El control conserva la distribución empírica de las acciones, pero elimina la relación en tiempo real entre estado propio y selección de acción.

## Estado

Protocolo preparado para ejecución mediante GitHub Actions.
