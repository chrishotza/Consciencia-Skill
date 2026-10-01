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

## Resultado auditado

Run GitHub Actions `36838953166`; artifact `11150575990`; commit experimental `7e8adcfd8aed0df514662912ded4482c6bda7ad0`.

Configuración: **64 episodios**, **8 replays por episodio**, **64 episodios de entrenamiento**, **512 muestras del autoobservador**.

- varianza autónoma FULL: **0.0531008831**;
- varianza con action replay: **0.0543576360**;
- contraste FULL − replay: **−0.0012567529**;
- p por permutación de signo: **0.4364282**.

Interpretación: el control información-matcheado no mostró una varianza autónoma adicional de FULL respecto de reproducir secuencias de acciones extraídas del mismo organismo. Esto **no establece C5 como dinámica propia específica** bajo este control más exigente. La separación positiva de C0.2 frente a `OPEN_LOOP` queda interpretativamente limitada porque ese control no igualaba la distribución de acciones.
