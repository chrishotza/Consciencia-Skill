<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V27 — Robustez al ruido de la geometría del estado

V27 prueba si el efecto direccional del estado observado en V24–V26 sobrevive a incrementos controlados del ruido dinámico.

Se conservan los seis puntos ciegos fijos, cuatro pares de historias, input futuro cero, memory/pressure comunes del receptor y la misma regla de transformación del estado.

Se usan seeds independientes 20–29. La desviación estándar del ruido se barre en:
0.0, 0.005, 0.01, 0.025, 0.05, 0.10.

Se prueban dos radios (0.5 y 1.1) y tres orientaciones (0°, 90°, 180°). El objetivo es robustez, no optimización de parámetros.

V27 no prueba consciencia; prueba si la geometría causal reproducible del estado es robusta frente a ruido dinámico.

</details>

<a id="english"></a>

# V27 — Noise Robustness of State Geometry

V27 tests whether the V24–V26 directional state effect survives controlled increases in dynamical noise.

The six fixed blind parameter points, four history pairs, zero future input, common receiver memory/pressure, and state transformation rule are preserved.

Independent seeds 20–29 are used. Noise standard deviation is swept over:
0.0, 0.005, 0.01, 0.025, 0.05, 0.10.

Two radii (0.5 and 1.1) and three orientations (0°, 90°, 180°) are tested. The purpose is robustness, not parameter optimization.

V27 does not test consciousness; it tests whether the reproducible causal state geometry is robust to dynamical noise.
