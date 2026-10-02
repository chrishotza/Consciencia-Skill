<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V20b — Restauración demorada del estado, corregida

## Corrección

V20 evaluaba inicialmente los primeros 60 pasos de la continuación completa incluso cuando la restauración ocurría después. Eso mezclaba la fase pre-restauración con la métrica de identidad.

V20b reemplaza esa métrica por una ventana post-restauración: los primeros 60 pasos futuros estrictamente posteriores a restaurar el state donante.

## Diseño

Seis puntos ciegos V12 más baseline, cuatro pares de historias, diez seeds de ruido emparejados por par e input futuro exactamente cero.

En la frontera histórica el receptor comienza con state, memory y pressure comunes. Después de un delay de 0, 5, 10, 20, 40 u 80 pasos, se restaura el state recurrente del donante. Memory y pressure del receptor permanecen como los generados durante la fase borrada/común.

La identidad se evalúa solo después de la restauración, frente a los segmentos correspondientes post-delay de las trayectorias de referencia del donante intacto/opuesto.

## Interpretación

Una curva de restauración que supere el baseline erased proporcionaría una prueba directa de recuperación causal complementaria a V15. La ventana post-restauración corregida evita contaminación por la fase pre-restauración.

Es un resultado dinámico computacional y no establece experiencia subjetiva.

</details>

<a id="english"></a>

# V20b — Corrected Delayed State Restoration

## Correction

V20 initially evaluated the first 60 steps of the full continuation even when restoration occurred later. That mixes the pre-restoration phase into the identity metric.

V20b replaces that metric with a post-restoration window: the first 60 future steps strictly after donor-state restoration.

## Design

Six V12 blind parameter points plus a baseline control, four history pairs, ten matched-noise seeds per pair, exact-zero future input.

At the history boundary the receiver starts from common state, memory, and pressure. After a delay of 0, 5, 10, 20, 40, or 80 steps, the donor recurrent state is restored. Receiver memory and pressure remain those generated during the erased/common phase.

Identity is evaluated only after restoration, against the corresponding post-delay segments of intact donor/opposite reference trajectories.

## Interpretation

A restoration curve that exceeds the erased baseline would provide a direct causal recovery test complementary to V15. The corrected post-restoration window avoids contamination by the pre-restoration phase.

This is a computational dynamical result and does not establish subjective consciousness.