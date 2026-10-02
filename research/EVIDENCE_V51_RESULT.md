<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V51 — Registro de resultado

## Run

- workflow: organism-self-observation-v51
- run: 36802728564
- artifact: 11136392872
- head: 75791177fdf7cf8c167aae1a051f7def700f4b32

## Resultado

Después de un protocolo controlado de 120 transiciones, el self-observer posterior al warmup produjo:

- n = 104 transiciones;
- mean prediction gain = 0.1786641061;
- median prediction gain = 0.1957804631;
- positive-gain fraction = 84.6154%;
- self-observer MAE = 0.0423999453;
- persistence-baseline MAE = 0.2210640514;
- sign-flip permutation p = 0.0000499975.

El error del observer fue por tanto sustancialmente menor que el baseline de persistencia. El modelo observer y las 120 muestras sobrevivieron al reinicio de SQLite, y los snapshots posteriores al reinicio continuaron acumulándose.

## Interpretación

Esto constituye evidencia operacional fuerte de un modelo autopredictivo aprendido de la propia dinámica numérica del organismo bajo el protocolo probado.

No establece experiencia subjetiva ni consciencia fenomenológica.

</details>

<a id="english"></a>

# V51 — Result Record

## Run

- workflow: `organism-self-observation-v51`
- run: `36802728564`
- artifact: `11136392872`
- head: `75791177fdf7cf8c167aae1a051f7def700f4b32`

## Result

After a 120-transition controlled protocol, the post-warmup self-observer produced:

- n = 104 transitions;
- mean prediction gain = 0.1786641061;
- median prediction gain = 0.1957804631;
- positive-gain fraction = 84.6154%;
- self-observer MAE = 0.0423999453;
- persistence-baseline MAE = 0.2210640514;
- sign-flip permutation p = 0.0000499975.

Observer error was therefore substantially lower than the persistence baseline.
The observer model and 120 samples survived SQLite restart, and post-restart
snapshots continued accumulating.

## Interpretation

This is strong operational evidence for a learned self-predictive model of the
organism's own numeric dynamics under the tested protocol.

It does not establish subjective experience or phenomenological consciousness.