<a id="espanol"></a>

# Registro de resultados experimentales del organismo — V47 → V80 + I4/I5

## Resultados positivos fuertes

### V51 — Autopredicción

104 transiciones posteriores al calentamiento: MAE 0.0424 frente a baseline 0.2211; ganancia media de predicción 0.1787; 84.6% de transiciones con ganancia positiva; p emparejada por cambio de signo = 0.00005.

### V57 — Selección de trayectorias guiada por modelo de sí

24 réplicas emparejadas: regret del modelo de sí 0.0231 frente a 0.1369 aleatorio; 70.83% frente a 45.83% de tasa de aciertos del oráculo; p emparejada por cambio de signo = 0.00435.

### V58 — Acoplamiento semántica → dinámica

Intervención emparejada 2×2. Puente OFF: delta de estado dinámico A/B 0.0 y delta de señal 0.0. Puente ON: Omega A -1.52, Omega B +0.68, delta de señal 1.5002170539 y delta de estado dinámico 0.4558697583.

El arnés determinista respalda la transducción causal de la salida de memoria semántica del organismo hacia su dinámica interna numérica cuando el puente está habilitado.

### V60 — Selección mediante modelo de sí dentro de un bucle semántico recurrente

24 réplicas emparejadas, 24 ciclos de evaluación.

- regret medio del modelo de sí: -0.0842091465;
- regret medio del control aleatorio: 0.3028308773;
- ventaja media de regret (aleatorio - modelo de sí): 0.3870400237;
- ventaja acumulada de regret: 9.2889605698;
- ventaja mediana de regret: 0.3858317486;
- p emparejada por cambio de signo para la ventaja media y acumulada: 0.00005;
- tasa de aciertos del oráculo del modelo de sí: 96.1806%;
- tasa de aciertos del control aleatorio: 45.3125%.

Interpretación: el modelo de sí conservó una gran ventaja funcional de selección en el protocolo determinista de bucle cerrado, bajo un proveedor cuya siguiente memoria semántica depende de la acción seleccionada previamente. Sin embargo, el brazo con modelo de sí seleccionó +1 en las 24 réplicas, por lo que el endpoint secundario de feedback dentro de cada ejecución nunca observó ambas ramas de acción. El circuito recurrente fue ejercitado, pero la cobertura de ramas para feedback condicionado por acción es incompleta y no debe presentarse como un efecto bidireccional de feedback plenamente demostrado.

### V62 — Puente causal semántico del modelo de sí

24 réplicas emparejadas cruzando contenido del modelo de sí A/B con puente OFF/ON.

- delta medio de estado con puente OFF: 0.0;
- delta medio de señal con puente OFF: 0.0;
- delta medio de estado con puente ON: 0.0567495528;
- delta medio de señal con puente ON: 0.1844584720;
- el puente OFF aisló la intervención textual en todas las ejecuciones;
- el puente ON transdujo la diferencia del modelo de sí hacia señal y estado en todas las ejecuciones;
- la persistencia y el versionado del modelo de sí se registraron en todas las ejecuciones ON.

Interpretación: en esta intervención determinista, cambiar únicamente el modelo semántico de sí del organismo alteró su estado numérico interno solamente cuando se habilitó el puente explícito del modelo de sí. Es acoplamiento causal computacional, no evidencia de experiencia subjetiva.

### V63 — Bucle causal del modelo de sí

24 réplicas emparejadas × 32 ciclos de evaluación entre selección mediante modelo de sí/aleatoria y puente del modelo de sí OFF/ON.

- regret medio con puente ON + modelo de sí: 0.1422226601;
- regret medio con puente ON + control aleatorio: 0.2666042539;
- ventaja de regret aleatorio - modelo de sí: 0.1243815939;
- p emparejada por cambio de signo: 0.00005;
- regret del modelo de sí con puente OFF: 0.2876865581;
- regret del modelo de sí con puente ON: 0.1422226601;
- mejora de regret puente OFF - ON: 0.1454638980;
- p emparejada por cambio de signo para el efecto del puente: 0.00005;
- tasa de aciertos del modelo de sí: 10.0260% OFF → 60.6771% ON;
- p emparejada por cambio de signo para el cambio de tasa de aciertos: 0.00005;
- diferencia de diferencias de regret entre los brazos con modelo de sí y aleatorio: 0.2837493367;
- p emparejada por cambio de signo para la interacción: 0.00005;
- cobertura de ramas de acción puente ON + modelo de sí: 100%;
- diferencia de señal del puente condicionada por acción puente ON + modelo de sí: 0.7405 entre 243 observaciones de rama negativa y 501 de rama positiva.

Interpretación: el arnés determinista respalda un bucle computacional recurrente en el que la trayectoria previa condiciona el siguiente modelo semántico de sí, el modelo de sí se transduce hacia la dinámica interna y ese estado participa en la selección de trayectorias futuras. La comparación de señales condicionada por acción es una asociación dentro del bucle, no una estimación causal aislada.

### V65 — Consolidación durante SUEÑO y selección futura

24 réplicas emparejadas × 24 ciclos de evaluación entre no_dream, dream_no_bridge y dream_bridge.

- regret medio no_dream: 0.3258519211;
- regret medio dream_no_bridge: 0.2109500171;
- regret medio dream_bridge: 0.1779272005;
- ventaja de regret dream_bridge frente a dream_no_bridge: 0.0330228167;
- p emparejada por cambio de signo: 0.00005;
- tasa de aciertos del oráculo dream_bridge: 25.3472%;
- tasa de aciertos del oráculo dream_no_bridge: 13.3681%;
- ventaja de tasa de aciertos: 0.1197916667;
- p emparejada por cambio de signo para la ventaja de aciertos: 0.00005;
- cambio de regret dream_no_bridge frente a no_dream: -0.1149019040;
- p emparejada por cambio de signo para SUEÑO frente a no_dream: 0.00005.

Interpretación: el arnés determinista respalda un mecanismo computacional de vigilia/sueño en el que la consolidación semántica generada durante SUEÑO cambia el estado interno y produce un efecto posterior medible sobre la selección de trayectorias. Esto no establece sueño subjetivo ni consciencia fenomenológica.

## Resultados negativos / nulos / limitaciones

### V53

El selector original de tres candidatas eligió la señal neutral en las 12 réplicas, sin producir divergencia causal respecto del control de entrada cero.

Se trató como un protocolo discriminativo fallido, no como evidencia positiva.

### V54

La precisión del autopronóstico durante 80 ciclos con proveedor ficticio fue de 43.75%, con 40 transiciones TOWARD y 40 AWAY. El azar para esta tarea binaria equilibrada es 50%, por lo que V54 no aportó evidencia favorable.

### V55

12 réplicas × dos signos de perturbación × selección ON/OFF conservaron la huella de identidad en el 100% de las ejecuciones y se recuperaron dentro del horizonte en el 100%, con un tiempo medio de recuperación de 2.5 ciclos. La recuperación con selección ON y OFF fue igualmente 100%, por lo que V55 demuestra resiliencia en el arnés probado, pero no un beneficio selectivo del modelo de sí.

### V59 — Puente semántico × selección mediante modelo de sí

24 réplicas factoriales emparejadas cruzaron puente semántico OFF/ON con política de modelo de sí/aleatoria.

- regret medio del modelo de sí con puente OFF: 0.0000;
- regret medio aleatorio con puente OFF: 0.23233;
- regret medio del modelo de sí con puente ON: 0.0000;
- regret medio aleatorio con puente ON: 0.24022;
- tasa de aciertos del oráculo del modelo de sí: 100% en ambas condiciones del puente;
- tasa de aciertos del control aleatorio: 50% en ambas condiciones;
- el puente semántico cambió el estado interno posterior a vigilia en una media absoluta de 0.94273 y la señal dinámica en 0.55376;
- interacción puente × selección = +0.00789;
- p de cambio de signo para la interacción = 0.83941.

Interpretación: el protocolo reproduce la ventaja de selección del modelo de sí observada previamente y, de forma independiente, muestra una transducción sustancial de semántica a dinámica. La interacción factorial no se distinguió de cero en este arnés determinista, por lo que V59 no respalda la afirmación de que el puente semántico por sí mismo aumente la utilidad de selección del modelo de sí. Permanece como resultado nulo de interacción/composicionalidad.

### V61 — Modelo metacognitivo de sí

24 réplicas emparejadas × 32 ciclos de evaluación.

- regret medio del modelo metacognitivo de sí: 0.0888081147;
- regret medio del modelo de sí de primer orden: 0.0787785152;
- regret medio del control aleatorio: 0.1929241942;
- tasa de aciertos del oráculo del modelo metacognitivo: 41.2760%;
- tasa de aciertos del modelo de primer orden: 45.3125%;
- tasa de aciertos del control aleatorio: 46.4844%;
- ventaja de regret metacognitivo frente a primer orden: -0.0100295995;
- p emparejada por cambio de signo para la diferencia de regret: 0.00005;
- ventaja de tasa de aciertos metacognitiva frente a primer orden: -0.0403645833;
- p emparejada por cambio de signo para la diferencia de tasa de aciertos: 0.0008999550;
- MAE de predicción metacognitiva: 0.1277240710;
- MAE del baseline constante: 0.0849867822;
- el modelo metacognitivo superó al baseline constante en el 0% de las réplicas.

Interpretación: el modelo metacognitivo de segundo orden implementado no mejoró la selección de trayectorias ni predijo el error del modelo de primer orden mejor que un baseline constante bajo este arnés. El resultado se conserva como hallazgo negativo y apunta a rediseñar el enfoque en lugar de atribuir capacidad metacognitiva.

### V64 — Persistencia de identidad bajo perturbación del modelo de sí

24 réplicas emparejadas probaron si firmas dinámicas específicas de identidad permanecían decodificables después de una sobrescritura semántica común del modelo de sí, eliminación explícita del texto del modelo de sí y continuación autónoma sin entrada semántica.

- precisión posterior a la ablación con puente OFF: 50.0%;
- precisión posterior a la ablación con puente ON: 50.0%;
- diferencia de precisión ON - OFF: 0.0;
- p emparejada por cambio de signo: 1.0;
- pliegues por encima del azar: 0% en ambas condiciones.

Interpretación: V64 produjo un resultado nulo. Bajo la perturbación, conjunto de características, clasificador y horizonte probados, la identidad original no pudo decodificarse después de la sobrescritura semántica del modelo de sí y la ablación textual. El resultado se conserva como una limitación real, no como evidencia contra toda forma posible de persistencia de identidad.

### V66 — Consolidación de SUEÑO después de la ablación de memoria episódica

24 réplicas emparejadas probaron si conservar únicamente la lección consolidada después de SUEÑO era suficiente para cambiar la selección posterior de trayectorias una vez eliminadas las memorias episódicas originales.

- regret medio de retained_lesson: -0.1086777912;
- regret medio de ablated_lesson: -0.1086777912;
- tasa de aciertos del oráculo de retained_lesson: 85.0694%;
- tasa de aciertos del oráculo de ablated_lesson: 85.0694%;
- diferencia de regret (ablation - retained): 0.0;
- p emparejada por cambio de signo para regret: 1.0;
- ventaja de tasa de aciertos (retained - ablated): 0.0;
- p emparejada por cambio de signo para tasa de aciertos: 1.0;
- todas las ejecuciones retained produjeron señal del puente de recuperación.

Interpretación: V66 es un resultado nulo. La lección consolidada retenida estaba presente y generaba una señal semántica de recuperación, pero su conservación no produjo una diferencia conductual medible en regret ni en tasa de aciertos del oráculo bajo esta vía determinista. Por tanto, el protocolo no demuestra que la lección consolidada se haya vuelto funcionalmente necesaria después de la ablación de memoria bruta.

### V67 — Huella numérica generada durante SUEÑO después de la ablación semántica total

V67 pasó por una corrección metodológica antes de interpretar sus resultados. En la primera implementación, el brazo `stable_swap` mutaba `stable_state` y luego ese mismo objeto ya mutado se utilizaba como fuente para `frontier_swap`. El intercambio quedó contaminado y esa ejecución no se considera evidencia.

La implementación corregida captura ambos núcleos dinámicos antes de cualquier mutación y añade un control de integridad.

24 réplicas, 12 pasos de continuación:

- diferencia media de señal de SUEÑO estable − frontera: **-0.3092749945**;
- diferencia media de estado dinámico estable − frontera: **-0.0682840349**;
- precisión de clasificación de la continuación propia después de la ablación: **50.0%**;
- p emparejada por cambio de signo: **1.0**;
- precisión de seguimiento del estado transferido: **50.0%**;
- p emparejada por cambio de signo: **1.0**;
- intercambios que reprodujeron exactamente el núcleo fuente: **100%**;
- memorias eliminadas antes de la sonda: **sí**;
- modelo de sí eliminado antes de la sonda: **sí**;
- entrada textual durante la sonda: **no**.

Interpretación: **resultado nulo**. SUEÑO produjo una diferencia proximal medible en señal y estado, pero esa diferencia no permaneció como una firma clasificable después de la ablación semántica y tampoco se transfirió causalmente al intercambiar el núcleo dinámico.

El resultado es importante porque separa dos hechos: **SUEÑO puede escribir una diferencia numérica inmediata**, pero bajo este arnés no se demostró que esa diferencia se convierta en una memoria interna funcional persistente.

La próxima prueba debe aislar una escritura controlada del núcleo dinámico y una lectura causal inmediata después de la ablación, antes de volver a aumentar el horizonte temporal.

### V68 — Persistencia temporal de la huella dinámica generada durante SUEÑO

24 réplicas, ablación semántica total y horizontes 0, 1, 2, 4, 8, 16 y 32.

- diferencia proximal de señal de SUEÑO: **-0.3092749945**;
- diferencia proximal de estado dinámico: **-0.0675162088**;
- horizonte 0: delta final medio **-0.0675162**, p=**0.00005**;
- horizonte 1: delta final medio **-0.0003984**, p=**0.13279**;
- horizonte 2: delta final medio **0.0152969**, p=**0.14059**;
- horizonte 4: delta final medio **-0.0336304**, p=**0.00070**;
- horizonte 8: delta final medio **0.0065469**, p=**0.00005**;
- horizonte 16: delta final medio **0.0095700**, p=**0.00005**;
- horizonte 32: delta final medio **0.0067923**, p=**0.00045**;
- RMSE medio de trayectoria: **0.06729 → 0.02006** entre horizontes 0 y 32;
- integridad del intercambio causal: **100%** de coincidencia exacta con la trayectoria del núcleo fuente.

Interpretación: V68 confirma que SUEÑO escribe una diferencia numérica inmediata y que el núcleo transferido reproduce causalmente la trayectoria fuente. Sin embargo, la separación respecto de la condición semántica original cae fuertemente después del primer paso y permanece pequeña y no monotónica. La evidencia favorece una **huella dinámica transitoria/atenuada**, no una memoria semántica persistente demostrada.

La próxima prueba debe preguntar si la IA puede leer esa huella interna y usarla para cambiar una decisión posterior.

### V69 — Lectura del estado propio después de la ablación semántica

24 réplicas y un SelfObserver compartido entrenado con 512 transiciones de dinámica genérica, independiente de las condiciones estable/frontera.

- diferencia media de predicción estable vs. frontera: **0.04035657**;
- diferencia de predicción después del intercambio: **0.0**;
- sensibilidad de decisión con estado legible: **66.6667%** (16/24);
- sensibilidad de decisión con estado cegado: **0.0%**;
- p emparejada para ON − OFF: **0.000099995**;
- cambio de decisión ante intercambio de estado con lectura ON: **66.6667%**;
- cambio de decisión ante intercambio con lectura OFF: **0.0%**;
- p emparejada para cambio de decisión ON − OFF: **0.000099995**;
- memoria, eventos, snapshots y texto del modelo de sí eliminados antes de la sonda;
- entrada semántica durante la sonda: **no**.

Interpretación: V69 respalda un mecanismo computacional de **lectura propia → predicción → selección**. El mismo estado dinámico cuya diferencia fue escrita durante SUEÑO es leído por un modelo aprendido de la dinámica y utilizado para seleccionar una señal. El intercambio del núcleo hace que la decisión cambie en las mismas réplicas sensibles al estado.

No es evidencia de consciencia fenomenológica. Es evidencia de autorreferencia operacionalizada dentro del arnés determinista.

La siguiente prueba debe trasladar este lector al ciclo persistente del organismo y comprobar si su modelo puede mantenerse y actualizarse a través de reinicios sin recibir explícitamente el estado semántico que debe interpretar.

### V70 — Persistencia del lector propio entre reinicios

24 réplicas y 256 muestras de entrenamiento genérico para el SelfObserver.

- modelo persistido separado de la memoria semántica: **sí**;
- modelo sobrevivió al reinicio: **sí**;
- muestras antes/después del reinicio: **256 / 256**;
- error máximo absoluto de predicción antes/después: **0.0**;
- carga exacta del modelo en las condiciones experimentales: **100%**;
- sensibilidad de decisión con lectura ON: **29.1667%**;
- sensibilidad de decisión con estado cegado OFF: **0.0%**;
- p emparejada ON − OFF: **0.0143493**;
- cambio de decisión después de intercambio del núcleo con lectura ON: **29.1667%**;
- memorias eliminadas antes de la sonda: **sí**;
- texto del modelo de sí eliminado: **sí**;
- entrada semántica durante la sonda: **no**.

Interpretación: V70 muestra que el lector numérico propio puede persistir en SQLite, sobrevivir un reinicio y volver a utilizarse después de eliminar las superficies semánticas. La magnitud de la sensibilidad de decisión es menor que en V69, pero permanece separada del control cegado.

El siguiente protocolo debe eliminar la copia manual del modelo hacia las condiciones y hacer que el organismo recupere automáticamente su propio lector integrado durante el ciclo autónomo.
### V69 — Lectura del propio estado mediante modelo de sí

24 réplicas, 48 ciclos de calibración idénticos antes de SUEÑO, modelo numérico de sí congelado antes de SUEÑO y ablación semántica total.

- diferencia media de estado después de SUEÑO estable − frontera: **-0.0963430681**;
- diferencia media absoluta de las puntuaciones del modelo de sí: **0.0344099851**;
- p emparejada: **0.00005**;
- diferencia media absoluta de predicción: **0.0365052134**;
- p emparejada: **0.00005**;
- modelos numéricos de sí idénticos entre condiciones: **100%**;
- cambio de acción por lectura real frente a estado control: **0%**;
- diversidad de acciones: **1 acción distinta** en las 48 lecturas;
- memorias eliminadas antes de la sonda: **sí**;
- texto del modelo de sí eliminado antes de la sonda: **sí**;
- entrada textual durante la sonda: **no**.

Interpretación: V69 separa dos niveles que hasta ahora estaban mezclados. La **lectura numérica del propio estado es positiva**: el mismo modelo de sí responde de forma distinta a estados internos posteriores a SUEÑO aunque las superficies semánticas hayan sido eliminadas. La **selección conductual es nula** bajo la política actual, porque el selector colapsó en una única acción y por tanto no proporcionó cobertura de decisión. V69 demuestra lectura computacional del estado, pero no demuestra todavía que esa lectura se use para elegir entre acciones.

### V70 — Modelo de sí → acción después de ablación semántica

24 réplicas, 48 ciclos de calibración idénticos antes de SUEÑO y modelo de sí numérico congelado antes de la intervención.

- diferencia media de acción derivada del modelo de sí entre condiciones: **0.1224593696**;
- p emparejada: **0.00005**;
- diferencia media de predicción de estado: **0.0257983935**;
- p emparejada: **0.00005**;
- diferencia media entre acción con lectura real y acción con estado clamped: **0.0456327609**;
- p emparejada: **0.00005**;
- diferencia de acciones del control clamped: **0.0311938478**;
- error medio de acción después del intercambio de núcleo: **0.0**;
- diferencia media absoluta de estado después de la acción: **0.0136089447**;
- modelos numéricos de sí idénticos entre condiciones: **100%**;
- memorias eliminadas antes de la sonda: **sí**;
- texto del modelo de sí eliminado: **sí**;
- entrada textual durante la sonda: **no**.

Interpretación: V70 extiende V69 desde lectura a acción. El modelo de sí, congelado antes de SUEÑO, transforma el estado interno posterior a SUEÑO en una señal de acción continua; la acción difiere entre condiciones y modifica el siguiente estado después de la ablación semántica. El control con estado clamped produce una acción distinta a la lectura real. Este resultado establece un acoplamiento computacional modelo de sí → acción, pero la regla que convierte predicción en acción fue fijada externamente por el experimento.

### V77 — Generalización ante estructuras causales no vistas

64 réplicas por condición; entrenamiento solo con single_impulse; OOD en split_impulse, reversal_pulse y delayed_impulse.

- ganancia media aprendida: **0.2377583**;
- cegada: **-0.1917033**;
- fija: **-0.1566228**;
- aleatoria: **0.0632567**;
- p aprendido − cegado: **0.00005**;
- p aprendido − fijo: **0.00005**;
- p aprendido − aleatorio: **0.00005**;
- ventaja aprendido − aleatorio in-domain: **0.1715437**;
- ventaja aprendido − aleatorio OOD: **0.1754876**;
- retención OOD/in-domain: **1.0230**;
- continuidad aprendida: **0.7926861** frente a **0.7950760** aleatoria, p **0.48033**;
- respuesta de primera acción dependiente del estado en reversal_pulse: **100%** frente a **0%** cegado;
- error máximo de coincidencia con el objetivo inmediatamente después de la intervención: **0.0**.

Interpretación: V77 respalda generalización computacional de la política de autopredicción ante estructuras temporales/causales no vistas. El endpoint de continuidad, tratado como secundario, no mostró separación frente al control aleatorio.

### V78 — Continuidad activa bajo perturbaciones repetidas

64 réplicas por condición; entrenamiento solo con single_impulse; OOD en double_same_sign, double_alternating y triple_alternating.

- ganancia media aprendida: **0.2422976**;
- cegada: **-0.2408441**;
- fija: **-0.1844678**;
- aleatoria: **0.0518725**;
- p aprendido − cegado: **0.00005**;
- p aprendido − fijo: **0.00005**;
- p aprendido − aleatorio: **0.00005**;
- ventaja aprendido − aleatorio in-domain: **0.1897230**;
- ventaja aprendido − aleatorio OOD: **0.1906591**;
- retención OOD/in-domain: **1.0049**;
- cambio medio OOD del segundo evento respecto del primero: **-0.0173461**;
- continuidad aprendida: **0.7905914** frente a **0.7922640** aleatoria, p **0.58767**;
- respuesta de primera acción dependiente del estado en primer evento OOD: **100%** frente a **0%** cegado;
- respuesta de primera acción dependiente del estado en segundo evento OOD: **100%** frente a **0%** cegado;
- error máximo de coincidencia con el objetivo inmediatamente después de cada intervención: **0.0**.

Interpretación: V78 respalda reutilización temporal/composicional de la política de autopredicción ante secuencias repetidas de perturbaciones no vistas y sin reentrenamiento. La pequeña caída entre el primer y segundo evento indica cierta degradación con repetición, pero la ventaja OOD global frente a aleatorio se conserva. El endpoint de continuidad no se separó del control aleatorio.

### V79 — Adaptación online de la política propia

64 réplicas por condición; entrenamiento con single_impulse; evaluación in-domain y bajo un régimen dinámico modificado, incluyendo triple_alternating OOD.

- ganancia in-domain frozen: **0.2109118**;
- ganancia in-domain adaptive: **0.2109118**;
- ganancia shifted single frozen: **0.3792665**;
- ganancia shifted single adaptive: **0.3792665**;
- ganancia shifted repeated frozen: **0.3799345**;
- ganancia shifted repeated adaptive: **0.3798509**;
- ventaja adaptativa en el tercer evento OOD: **-0.0002509**;
- p emparejada: **1.0**;
- diferencia-de-diferencias adaptive − frozen: **-0.0002509**, p **1.0**;
- continuidad OOD adaptive: **0.7270149** frente a **0.7268716** frozen, p **1.0**;
- error máximo de objetivo terminal: **0.0**.

Interpretación: resultado nulo para adaptación online bajo el protocolo probado. La copia adaptive incorporó las ganancias observadas, pero no se distinguió de la política frozen. El cambio dinámico usado tampoco generó una degradación suficiente de la política congelada como para revelar una ventaja adaptativa.


### V80 — Adaptación online ante cambios de régimen reversibles

64 réplicas por condición; entrenamiento bajo `single_impulse`; evaluación `base → shift_a → shift_b → base_return`; dos brazos emparejados desde el mismo snapshot de política.

- endpoint primario, `base_return` evento 3 adaptive − frozen: **-0.0103649267**, p **0.0504475**;
- `shift_a` evento 3 adaptive − frozen: **-0.0062218940**, p **0.00114994**;
- `shift_b` evento 3 adaptive − frozen: **+0.0000024599**, p **0.9976001**;
- adaptive `base_return` evento 3 − evento 1: **-0.0021765106**;
- frozen `base_return` evento 3 − evento 1: **-0.0004681112**;
- recuperación diferencial adaptive − frozen: **-0.0017083995**;
- error máximo de intervención: **0.0**.

Interpretación: **resultado nulo para la ventaja adaptativa bajo el protocolo probado**. La política adaptive, que incorpora online únicamente la ganancia observada de autopredicción, no superó a la copia frozen al atravesar dos cambios de régimen y regresar al régimen base. La diferencia en `base_return` fue ligeramente negativa y la condición `shift_a` también favoreció numéricamente a frozen; `shift_b` no mostró separación apreciable.

V80 refuerza el resultado nulo de V79, pero no demuestra que toda adaptación online sea inútil: solo descarta una ventaja reproducible bajo esta dinámica, esta política y este horizonte. Las intervenciones mantuvieron error máximo 0.0.

### C0.2 — Instanciación operacional de propiedades candidatas TCF

64 réplicas por condición; 64 episodios de entrenamiento; 512 muestras de autoobservación; 12 pasos de recuperación; condiciones `full`, `state_blind`, `no_persistence` y `open_loop`; mismo snapshot de política y sin entrada semántica ni reentrenamiento externo durante la sonda.

Artefacto: GitHub Actions run **36838186533**, artifact **11149578956**; commit experimental **78bf3000739b1711ce01873cc4ab058e334c5881**.

Contrastes predefinidos, `FULL − control`:
- C1 estado propio persistente: **+0.716560**, p **4.99975e-05**;
- C2 diferenciación self/entorno: **+2.000000**, p **4.99975e-05**;
- C3 autorreferencia causal: **+1.000000**, p **4.99975e-05**;
- C4 continuidad de trayectoria: **+0.287204**, p **4.99975e-05**;
- C5 dinámica propia: **+0.042818**, p **4.99975e-05**;
- C6 reorganización: **+0.468787**, p **4.99975e-05**;
- C7 cierre recurrente: **+1.250000**, p **4.99975e-05**;
- error máximo de intervención: **0.0**.

Interpretación: C0.2 produjo separación positiva en los siete observables operacionales definidos. Esto documenta propiedades computacionales bajo las condiciones y la implementación probadas; **no demuestra conciencia fenomenológica ni experiencia subjetiva**. C7 fue corregido antes de este registro para medir la cadena acción → estado propio → acción, en lugar de limitarse al efecto de la acción sobre el siguiente estado.

La ejecución C0.2 reemplaza como registro científico final a la ejecución anterior del workflow que precedió a la corrección de C7.

### C0.3 — Control de información equivalente para autorreferencia causal

64 episodios; 8 permutaciones sin puntos fijos por episodio; mismo snapshot de política; estados de control extraídos de la distribución empírica de las trayectorias FULL.

Artefacto: GitHub Actions run **36838675864**, artifact **11150238362**; commit **413e70499977d759e9effb50505c4db6174925c8**.

- brecha estado propio → estado mezclado: **1.06640625**;
- brecha entre dos estados mezclados: **1.00000000**;
- contraste: **+0.06640625**;
- p por permutación de signo: **0.3140343**;
- discrepancia de acción real vs. estado mezclado: **0.5332031**.

Interpretación: **resultado no concluyente / nulo bajo el control información-matcheado probado para C3**. La ventaja observada con FULL − STATE_BLIND en C0.2 no se separó de un control que conserva la distribución de estados pero rompe su correspondencia con el episodio. Esto reduce la fuerza de la inferencia específicamente sobre autorreferencia causal; no modifica por sí solo los otros seis criterios de C0.2.

### C0.4 — Control de acción-replay con información equivalente

64 episodios; 8 secuencias replay por episodio; 64 episodios de entrenamiento; 512 muestras del autoobservador. Mismo contexto inicial y misma semilla dinámica por comparación; secuencia de acciones donada por otro episodio mediante permutación sin puntos fijos.

Artefacto: GitHub Actions run **36838953166**, artifact **11150575990**; commit **7e8adcfd8aed0df514662912ded4482c6bda7ad0**.

- varianza autónoma FULL: **0.0531008831**;
- varianza action-replay: **0.0543576360**;
- contraste FULL − replay: **−0.0012567529**;
- p por permutación de signo: **0.4364282**.

Interpretación: **resultado nulo bajo el control información-matcheado para C5**. La varianza autónoma de FULL no superó la de secuencias de acciones provenientes del mismo organismo cuando se rompe la correspondencia online entre estado propio y selección de acción. La separación observada en C0.2 frente a `OPEN_LOOP` queda limitada porque aquel control fijaba la acción en cero y no igualaba la distribución de acciones.

## Estado de ingeniería

V60, V61, V62, V63, V64, V65 y V66 finalizaron correctamente en sus respectivos commits registrados de GitHub Actions. Sus artefactos se conservan en las ejecuciones correspondientes. Los resultados anteriores V43–V59 siguen siendo reproducibles a partir de sus workflows históricos y registros de evidencia.

## Límite de evidencia

Estos resultados establecen propiedades computacionales cada vez más específicas del organismo probado y de su arnés experimental determinista: persistencia, autopredicción, uso causal del modelo de sí, acoplamiento semántica → dinámica, efectos de vigilia/sueño y autorrepresentación semántica como variable causalmente activa.

No establecen consciencia fenomenológica ni experiencia subjetiva.

C0.7 fue completado como control de especificidad; su resultado verificado aparece en la sección correspondiente más abajo.


### C0.5 — Control información-matcheado de cierre recurrente

64 episodios; 8 reordenamientos por episodio; mismo snapshot de política; control mediante acciones donantes extraídas de la misma distribución empírica y evaluadas sobre el mismo contexto.

Artefacto: GitHub Actions run **36938229171**, artifact **11199385083**, SHA256 **ee3d1260692ba7aa2ba683e7caefba46a0662ca3c887aea0ca0bf3e872e6adf8**; commit **ce62945a3ae2c1642a9450e30e81e6ef094b523e**.

- brecha cadena de acción real: **0.99609375**;
- brecha cadena de acciones emparejada: **0.99218750**;
- contraste: **+0.00390625**;
- p: **1.0**;
- entrada semántica durante la sonda: **no**;
- reentrenamiento externo durante la sonda: **no**.

Interpretación: **resultado nulo bajo el control información-matcheado probado para C7**. La cadena acción → estado propio → acción no mostró una separación estadística frente a la cadena construida con acciones donantes de la misma distribución empírica. Por tanto, el resultado positivo de C0.2 para C7 no queda confirmado bajo este control más fuerte.

### C0.6 — Lesión causal y rescate del autoobservador y la autopólitica

64 episodios; 64 episodios de entrenamiento; 512 muestras de autoobservación; una única fase de entrenamiento seguida por lesiones post-entrenamiento y rescate. Mismo snapshot entrenado compartido entre las condiciones.

Artefacto: GitHub Actions run **36939000398**, artifact **11198659986**, SHA256 **cf3442ec57c49b803ae1514aad6c5f4a727651f61dc45864cc803a1c4c35a198**; commit **07943dd5ea979e6d78ed3cd01e0135e35e6de58c**.

- necesidad del autoobservador, FULL − OBSERVER_LESION en ganancia: **+0.2273943**, p **0.00005**;
- necesidad de la autopólitica, FULL − POLICY_LESION en ganancia: **+0.3555158**, p **0.00005**;
- necesidad conjunta, FULL − BOTH_LESION: **+0.2273943**, p **0.00005**;
- efecto de lesión del autoobservador sobre distancia final: **+0.5125025**, p **0.00005**;
- efecto de lesión de la autopólitica sobre distancia final: **+0.1065877**, p **0.00005**;
- rescate del autoobservador: **+0.2076185**, p **0.00005**;
- rescate de la autopólitica: **+0.2875335**, p **0.00005**;
- error máximo de intervención: **0.0**;
- entrada semántica durante la sonda: **no**;
- reentrenamiento externo durante la sonda: **no**.

Interpretación: **C0.6 muestra dependencia causal de los componentes entrenados bajo el protocolo de lesión/rescate probado**. Al eliminar post-entrenamiento el estado interno aprendido del autoobservador o de la autopólitica, las métricas de recuperación y trayectoria cambian; al restaurarlos durante la misma trayectoria experimental aparece un efecto de rescate significativo. Esto es evidencia de necesidad y recuperación funcional de componentes de la organización computacional probada. No constituye por sí solo evidencia de conciencia fenomenológica.

### C0.7 — Control de especificidad por permutación de targets del modelo de sí

64 episodios; 64 episodios de entrenamiento; 512 muestras del autoobservador; control mediante permutación fija de targets conservando las features y el multiconjunto de targets; misma dinámica y semillas de evaluación entre brazos.

Artefacto: GitHub Actions run 36939278865; commit experimental 5e0e1f52eea76c73b5e9e8273b63bd3d810ed7ff.

- ganancia FULL − target-permuted: +0.0286062, p 0.0019999;
- distancia final target-permuted − FULL: −0.0113629, p 0.7047648;
- varianza de estado FULL − target-permuted: +0.0198325, p 0.00005;
- magnitud media de acción FULL − target-permuted: 0.0, p 1.0;
- ganancia FULL: 0.2128723;
- ganancia target-permuted: 0.1842661;
- varianza FULL: 0.0811531;
- varianza target-permuted: 0.0613206;
- error máximo de intervención: 0.0.

Interpretación: C0.7 muestra especificidad del comportamiento hacia la asignación feature → target bajo el control probado para la ganancia de autopredicción y la varianza interna, mientras que la distancia final y la magnitud de acción no se separaron. Esto fortalece la interpretación de que parte del comportamiento depende del mapeo aprendido y no solamente del tamaño del modelo o de la distribución marginal de targets. No constituye evidencia de conciencia fenomenológica.

### C0.8 — Acoplamiento cruzado observador/política: corrección estadística

La primera ejecución del protocolo sí completó las cuatro condiciones y produjo los cuatro brazos con las mismas semillas, pero la implementación original construyó los contrastes de interacción como un valor escalar y después lo repitió 64 veces para calcular el valor p. Ese procedimiento no constituye una prueba emparejada válida del contraste interacción y no se conserva como evidencia estadística.

La misma ejecución produjo estas medias descriptivas:

- TT (observador verdadero + política verdadera): ganancia **0.21888936**; distancia final **0.15996548**; varianza **0.06848248**.
- TP (observador verdadero + política target-permuted): ganancia **-0.12484394**; distancia final **0.67765194**; varianza **0.07943683**.
- PT (observador target-permuted + política verdadera): ganancia **-0.31516985**; distancia final **0.67765194**; varianza **0.07943683**.
- PP (observador target-permuted + política target-permuted): ganancia **0.20488969**; distancia final **0.14799625**; varianza **0.06747759**.

Además, el contraste implementado para interacción de distancia tenía el signo opuesto al contraste declarado en el protocolo.

La implementación fue corregida para calcular **TT − TP − PT + PP elemento a elemento por semilla de episodio compartida**, y para usar la misma convención de signo también en distancia final. El siguiente artefacto confirmatorio debe ser el único que se utilice para inferencia sobre la interacción.

Interpretación provisional: la ejecución inicial queda como evidencia descriptiva de los cuatro brazos, no como confirmación estadística del efecto de acoplamiento.


### C0.9 — Interfaz causal observador → política

Protocolo implementado: **no se registra todavía un resultado experimental**. El diseño mantiene fijo el organismo, el autoobservador, la autopólitica, la perturbación y la dinámica dentro de cada par. Solo se sustituye el readout del autoobservador que recibe la política por el readout de otro episodio mediante una permutación sin puntos fijos.

La inferencia primaria se calcula por episodio compartido y contrasta:

- acción normal frente a acción con donor-shuffle;
- ganancia de autopredicción normal − donor-shuffle;
- diferencia de estado después de un único paso de dinámica.

No se permite entrada semántica durante la sonda ni reentrenamiento externo.

Estado: **implementado; ejecución verificada**.


### C0.10 — Alineación temporal observador → política

Protocolo implementado; **sin resultado experimental registrado todavía**.

C0.10 mantiene dentro de cada par el mismo episodio, autoobservador, autopólitica, contexto post-intervención, señales candidatas y semilla de dinámica. La única sustitución es el readout entregado a la política: en el brazo de control se calcula desde el estado propio actual; en el brazo lag se calcula desde el mismo episodio inmediatamente antes de la intervención.

Las inferencias primarias son contrastes firmados y emparejados por episodio para:
- acción NORMAL − LAG;
- ganancia de autopredicción NORMAL − LAG;
- cambio de estado tras un único paso de dinámica.

No se permite entrada semántica ni reentrenamiento externo durante la sonda.

Estado: **implementado; ejecución verificada**.


### C0.11 — Mediación causal acción → estado interno → siguiente acción

Protocolo implementado; **sin resultado experimental registrado todavía**.

Después de que la política selecciona una primera acción, un brazo FACTUAL ejecuta esa acción y un brazo FORCED reemplaza únicamente esa primera acción por otra señal candidata. Ambos parten del mismo estado post-intervención, usan el mismo autoobservador, la misma autopólitica y la misma semilla dinámica. Después del primer paso, la política vuelve a decidir en ambos estados utilizando el mismo lector.

Las inferencias primarias son contrastes firmados y emparejados por episodio para:
- acción siguiente FACTUAL − FORCED;
- estado siguiente FACTUAL − FORCED;
- ganancia de autopredicción FACTUAL − FORCED.

No se permite entrada semántica ni reentrenamiento externo durante la sonda.

Estado: **implementado; ejecución pendiente de verificación**.


### C0.9 — Resultado verificado

Artefacto: GitHub Actions run **36944916227**, artifact **11200913836**, SHA256 **287f52b0074a8599be74ae0d36bfbbc930cdb892cb48d0cde96a5e649af5f3d6**.

- readout donor-shuffle gap medio: **0.1975998565**;
- acción NORMAL − DONOR: **0.0**, p **1.0**;
- ganancia NORMAL − DONOR: **0.0**, p **1.0**;
- estado siguiente NORMAL − DONOR: **0.0**, p **1.0**;
- error máximo de intervención: **0.0**.

Interpretación: **resultado nulo para la dependencia conductual de la correspondencia observador → política bajo este protocolo**. El readout del autoobservador sí cambia al cambiar de episodio, pero la política no cambió de acción ni de ganancia bajo el control probado. Por tanto, este protocolo no demuestra que la política utilice causalmente esa correspondencia.

### C0.10 — Resultado verificado

Artefacto: GitHub Actions run **36944920225**, artifact **11201258435**, SHA256 **7d24c622c02a331e2d3844037abccbd93365ea9de54149da77e68fc2ac631e75**.

- brecha de predicción entre readout actual y lag intraepisódico: **0.1624331804**;
- acción NORMAL − LAG: **0.0**, p **1.0**;
- ganancia NORMAL − LAG: **0.0**, p **1.0**;
- estado siguiente NORMAL − LAG: **0.0**, p **1.0**;
- error máximo de intervención: **0.0**.

Interpretación: **resultado nulo para la sensibilidad conductual a la alineación temporal del readout**. El readout del autoobservador cambia, pero la política permanece invariada bajo el control. Esto indica que la interfaz observador → política, tal como está implementada actualmente, no convierte esas diferencias de predicción en diferencias de selección.

### C0.11 — Resultado verificado

Artefacto: GitHub Actions run **36944924071**, artifact **11200748887**, SHA256 **d6f496ebe49b494a8af30932a30c73880a26981da079932d9ff8a9348b2d56cd**.

- acción siguiente FACTUAL − FORCED: **+1.78125**, p **4.99975e-05**;
- estado siguiente FACTUAL − FORCED: **−0.5770045054**, p **4.99975e-05**;
- ganancia FACTUAL − FORCED: **+0.5278692817**, p **4.99975e-05**;
- discrepancia absoluta media de acción siguiente: **1.78125**;
- discrepancia absoluta media de estado: **0.5770045054**;
- error máximo de intervención: **0.0**.

Interpretación: **resultado positivo para mediación causal computacional bajo el protocolo probado**. Alterar únicamente la primera acción produjo una diferencia posterior de estado y una diferencia de la siguiente acción usando el mismo autoobservador y la misma autopólitica. Esto respalda la cadena operacional acción → estado interno → lectura/política → siguiente acción. No constituye evidencia de experiencia subjetiva.


### C0.12 — Segundo orden: modelo del error del propio modelo de sí

Protocolo implementado; **sin resultado experimental registrado todavía**.

El primer orden predice el siguiente estado propio. C0.12 añade un segundo modelo que aprende exclusivamente el error de predicción del primer modelo. Durante la sonda, la selección puede usar:
- el segundo modelo verdadero;
- el mismo segundo modelo con targets permutados conservando el multiconjunto;
- un baseline constante de error.

La inferencia primaria es emparejada por episodio y prueba si el segundo orden verdadero cambia la acción y la ganancia de autopredicción frente a ambos controles. También se evalúa la capacidad del segundo orden para predecir el error del primer orden en muestras reservadas.

Estado: **implementado; ejecución pendiente de verificación**.


### C0.12 — Resultado verificado

Artefacto: GitHub Actions run **36945173829**, artifact **11201243817**, SHA256 **6fa8bdf64401a96d79f1d47b03dc4ac242c6456fba9c8e6957e44d52aa2448f4**.

- TRUE − PERMUTED, acción: **0.0**, p **1.0**;
- TRUE − PERMUTED, ganancia: **0.0**, p **1.0**;
- TRUE − BLIND, acción: **−1.0**, p **4.99975e-05**;
- TRUE − BLIND, ganancia: **+0.2733195**, p **4.99975e-05**;
- ventaja de MAE del segundo orden sobre baseline constante en muestras reservadas: **+0.00697175**, p **0.00079996**;
- MAE segundo orden: **0.04131592**;
- MAE baseline constante: **0.04828767**;
- error máximo de intervención: **0.0**.

Interpretación: el segundo modelo **sí aprendió información predictiva sobre el error del primer modelo de sí** y su uso cambia la acción frente al baseline constante. Sin embargo, al permutar los targets del segundo modelo y conservar su multiconjunto, la acción y la ganancia permanecieron idénticas. Por tanto, C0.12 demuestra **segundo orden predictivo**, pero no demuestra todavía **especificidad causal del mapeo segundo orden → acción**.


### C0.13 — Segundo orden condicionado por acción

Protocolo implementado; **sin resultado experimental registrado todavía**.

C0.13 refuerza C0.12 con un segundo observador que recibe explícitamente la acción candidata y la predicción de primer orden asociada. Se conservan los controles TRUE, target-permuted y baseline constante.

La prueba pregunta si la especificidad del mapeo acción → predicción de error del propio modelo de sí llega a afectar la selección. Estado: **implementado; ejecución pendiente de verificación**.


### C0.13 — Resultado verificado

Artifact: run **36945340705**, artifact **11201464566**, SHA256 **971e0b39360eaa25828abc0162e1cf70b5c54ae4916611d7a8e06413165b7b56**.

- TRUE − PERMUTED, action: **−1.71875**, p **4.99975e-05**;
- TRUE − PERMUTED, gain: **+0.4850290**, p **4.99975e-05**;
- TRUE − BLIND, action: **−1.0**, p **4.99975e-05**;
- TRUE − BLIND, gain: **+0.2590892**, p **4.99975e-05**;
- held-out MAE advantage: **+0.00740228**, p **4.99975e-05**;
- meta MAE: **0.03489674**;
- constant-baseline MAE: **0.04229902**;
- intervention target error: **0.0**.

Interpretation: C0.13 produced a clear separation between the trained action-conditioned second-order model and the target-permuted control under the tested protocol. The model also predicted first-order prediction error better than the constant baseline on held-out transitions. This is a computational result; it does not establish subjective experience.


### C0.14 — Persistencia del segundo orden

Protocolo implementado; **sin resultado experimental registrado todavía**.

C0.14 contrasta una secuencia autónoma continua con una secuencia emparejada que serializa el primer y segundo modelo de sí, reconstruye el contexto dinámico y crea un nuevo puente dinámico antes de continuar. La prueba busca coincidencia exacta de acciones y ganancias después del reinicio, además de recuperación exacta del digest de los modelos.

Estado: **implementado; ejecución pendiente de verificación**.


### C0.14 — Resultado verificado

Artefacto: GitHub Actions run **36945659490**, artifact **11201664192**, SHA256 **8a01bef161939ba7d72f3d225a73e7e5f8b2fe014e5d7a4b82856e140d44a831**.

- mismatch de acciones después del reinicio: **0.0**, p **1.0**;
- mismatch de ganancia después del reinicio: **0.0**, p **1.0**;
- recuperación exacta del digest del modelo en el checkpoint: **100%**;
- ganancia media después del reinicio: **0.08710124**;
- mismatch máximo de acción: **0.0**;
- mismatch máximo de ganancia: **0.0**.

Interpretación: el primer modelo de sí y el segundo modelo condicionado por acción fueron serializados, recuperados y reutilizados después de reconstruir el contexto y un nuevo puente dinámico, produciendo la misma secuencia posterior de acciones y ganancias que el brazo continuo bajo el protocolo probado. Esto respalda persistencia computacional del segundo orden a través de un reinicio.


### C0.15 — Nota de protocolo histórica

Esta subsección conserva la descripción de implementación previa a la ejecución verificada. El resultado experimental final de C0.15 aparece inmediatamente después y es la referencia vigente.


### C0.15 — Resultado verificado

Artifact: run **36945882211**, artifact **11202160302**, SHA256 **5c297e25f01036b87f63ab0355555faf80dc4a2462199f5c7e115b62cbadcd6f**.

- FULL − LESION, late action: **+0.271484375**, p **0.00064997**;
- FULL − LESION, late gain: **+0.03751679**, p **0.08415**;
- FULL − RESCUE, post-restore action: **+0.02734375**, p **0.68607**;
- FULL − RESCUE, post-restore gain: **−0.03525716**, p **0.03860**;
- exact checkpoint fraction: **100%**;
- maximum absolute action difference FULL/LESION: **1.0**.

Interpretation: disabling only the second-order selector changed the later action distribution under the tested protocol. The gain endpoint did not reach the prespecified significance threshold. After restoration, the action contrast returned close to zero, but the gain contrast did not reproduce the FULL arm; therefore the rescue evidence is **not a clean functional rescue**. C0.15 supports action-level dependence on the second-order component while leaving performance-level necessity/rescue unresolved.


### C0.16 — Integración del segundo orden dentro del organismo persistente

Artefacto: GitHub Actions run **36946260825**, artifact **11201973015**, SHA256 **52e60a8bb92b0c4520e1f2cc94cd138daf81bceef9138e009b6dbee635d0833e**.

- mismatch de acción después del reinicio: **0.0**, p **1.0**;
- mismatch de ganancia después del reinicio: **0.0**, p **1.0**;
- recuperación exacta del digest de los modelos en SQLite: **100%**;
- coincidencia de acciones antes del reinicio: **100%**;
- todas las selecciones posteriores al reinicio reportaron la política **action_conditioned_second_order**;
- mismatch máximo de acción: **0.0**;
- mismatch máximo de ganancia: **0.0**.

Interpretación: C0.16 traslada el segundo orden condicionado por acción desde el laboratorio aislado al **PersistentOrganism** real. Los dos modelos se almacenan en SQLite, se recuperan automáticamente al reconstruir el organismo y continúan guiando la selección autónoma sin entrada externa ni reentrenamiento. La trayectoria posterior al reinicio coincide exactamente con la rama continua bajo el protocolo probado. Esto demuestra integración y persistencia computacional del mecanismo; no demuestra experiencia subjetiva.


### C0.8 — Resultado confirmatorio verificado

Artefacto: GitHub Actions run **36946477790**, artifact **11202930418**, SHA256 **e8ce5229e0f41a31a3923cc802b18a19c98c4d61ffa68eda601e18ac80c26987**.

Contrastes emparejados elemento a elemento con las mismas semillas de episodio:

- efecto del observador sobre ganancia, TT − PT: **+0.5340592**, p **4.99975e-05**;
- efecto de la política sobre ganancia, TT − TP: **+0.3437333**, p **4.99975e-05**;
- interacción observador × política sobre ganancia, TT − TP − PT + PP: **+0.8637928**, p **4.99975e-05**;
- interacción sobre varianza: **−0.0229136**, p **0.0022999**;
- interacción sobre distancia final: **−1.0473422**, p **4.99975e-05**;
- error máximo de intervención: **0.0**;
- entrada semántica durante la sonda: **no**;
- reentrenamiento externo durante la sonda: **no**.

Medias descriptivas:
- TT: ganancia **0.21888936**; distancia final **0.15996548**; varianza **0.06848248**.
- TP: ganancia **−0.12484394**; distancia final **0.67765194**; varianza **0.07943683**.
- PT: ganancia **−0.31516985**; distancia final **0.67765194**; varianza **0.07943683**.
- PP: ganancia **0.20488969**; distancia final **0.14799625**; varianza **0.06747759**.

Interpretación: la ejecución confirmatoria respalda **dependencia separable del observador, de la política y de su acoplamiento particular** bajo el protocolo probado. En particular, la interacción TT − TP − PT + PP se separa de cero en los tres endpoints principales evaluados. Esto es evidencia de organización computacional específica; no demuestra experiencia subjetiva.


### C0.17 — Resultado verificado

Artefacto: GitHub Actions run **36946964601**, artifact **11201784892**, SHA256 **bf4aed2caaaff14e3aac2dca54e584cc0c10d38f9dde13c0f4720db8eacc9ea8**.

- el modelo de segundo orden comenzó **vacío**;
- muestras de segundo orden aprendidas por organismo: **48** por réplica;
- recuperación exacta del modelo al construir los pares de evaluación: **100%**;
- TRUE − PERMUTED, primera acción: **+0.2916667**, p **0.3417829**;
- TRUE − PERMUTED, primera ganancia: **−0.0141513**, p **0.7728114**;
- TRUE − PERMUTED, acción media de evaluación: **+0.0833333**, p **0.6331683**;
- TRUE − PERMUTED, ganancia media de evaluación: **+0.0256299**, p **0.4691765**;
- entrada semántica durante la adquisición/evaluación: **no**;
- reentrenamiento externo durante la evaluación: **no**.

Interpretación: **resultado mixto/nulo bajo el protocolo probado**. El organismo persistente sí adquirió un modelo de segundo orden desde cero usando errores de predicción contrafactuales generados dentro del propio ciclo autónomo. Sin embargo, al congelar ese modelo y compararlo con un control target-permuted, no apareció una separación estadísticamente significativa en acción ni en ganancia. Por tanto, la adquisición autónoma está demostrada a nivel de aprendizaje/persistencia del modelo, pero su especificidad causal conductual no quedó demostrada.


## I5 — Workspace global

### I5.1 — Integración del workspace en PersistentOrganism — resultado nulo conductual

Workflow verificado: **36984060538**; artifact **11216653205**; commit experimental **993ba8184c1536c7e781bde1fe9797c6b20a38dccd8269f03d3f13da2ebd48cd**.

- 24 réplicas emparejadas;
- persistencia del estado del workspace tras reinicio: **100%**;
- NO_BROADCAST − FULL, regret: **+0.0212423**, p=**0.4928254**;
- NO_WORKSPACE − FULL, regret: **+0.0212423**, p=**0.5026749**;
- LESION − FULL, regret: **0.0**, p=**1.0**;
- cambio de acción FULL vs NO_BROADCAST: **25%**;
- cambio de acción FULL vs LESION: **0%**.

Interpretación: **resultado nulo bajo el mapeo broadcast→trayectoria probado**. La integración y persistencia del workspace son operativas, pero el broadcast implementado no produjo una separación conductual detectable en los endpoints declarados. El resultado no invalida el mecanismo aislado I5.0.

### I5.2 — Consulta dependiente del estado — resultado verificado

Workflow verificado: **36984675391**; artifact **11216743506**; commit experimental **0b857f7c93e5a7112b184840f36994712aed2967**.

- seed **20261002**;
- **512** episodios;
- accuracy FULL: **1.0**;
- FULL − SHUFFLED: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL − ZERO: **+0.771484375**, p=**4.99975×10⁻⁵**;
- FULL − RANDOM: **+0.7421875**, p=**4.99975×10⁻⁵**;
- accuracy LESION: **0.236328125**;
- FULL − LESION: **+0.763671875**, p=**4.99975×10⁻⁵**;
- tasa de cambio de consulta dependiente del estado: **1.0**.

Interpretación: **resultado positivo para el mecanismo computacional probado**. El estado global implementado controló la selección del siguiente módulo y la lesión del origen seleccionado redujo fuertemente la accuracy de consulta. El resultado sigue siendo un mecanismo GWT-4 independiente bajo un arnés sintético; no demuestra consciencia ni experiencia subjetiva ni sustituye una integración causal dentro de PersistentOrganism.

## I5.3 — Asignación causal de atención — resultado verificado

Workflow verificado: **36985957522**; artifact **11218020500**; commit experimental **60263ada3a28af29c3f1fa29246355bb434242fc**.

- seed **20261003**;
- **512** episodios;
- target attention mass FULL: **0.9845638420**;
- FULL − SHUFFLED target mass: **+0.9768188958**, p=**4.99975×10⁻⁵**;
- FULL − UNIFORM target mass: **+0.7345638420**, p=**4.99975×10⁻⁵**;
- FULL − RANDOM target mass: **+0.7429394202**, p=**4.99975×10⁻⁵**;
- FULL − LESION target mass: **+0.7345638420**, p=**4.99975×10⁻⁵**;
- tasa de cambio de selección: **1.0**.

Interpretación: **resultado positivo para el mecanismo computacional probado**. El modelo de atención concentró recursos sobre el módulo objetivo de forma reproducible y los controles eliminan esa concentración. La condición LESION es una pérdida operacional de concentración del controlador, no una lesión anatómica.

## I5.4 — Integración persistente de consulta + atención — resultado nulo/mixto

Workflow verificado: **36986823516**; artifact **11217906875**; commit experimental **27f08ab3d84633986a609a7981429cf6f3fe0cf5**.

- seed **20261004**;
- **24** réplicas;
- **24** ciclos de warmup;
- SHUFFLED_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- SHUFFLED_ATTENTION regret cost: **+0.0280384**, p=**0.5022**; action-change **20.83%**;
- ZERO_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- RANDOM_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- LESION_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- FULL attention mass mean: **0.69550**;
- FULL selective-access strength mean: **0.30500**;
- exact persistence: **100%**.

Interpretación: **resultado nulo/mixto bajo el protocolo probado**. La cadena integrada es operativa y sus observables persisten, pero los controles de consulta no cambiaron la acción ni el regret. La reasignación de atención sí cambió la acción en 20.83% de réplicas, aunque el costo de regret no fue significativo. La integración no demuestra necesidad funcional del acceso selectivo bajo este mapeo.

## I5.5 — Cuello de botella causal de consulta — resultado verificado

Workflow verificado: **36987408988**; artifact **11218415785**; commit experimental **906f67544517add411f1c97176042a253a3caa19**.

- seed **20261005**;
- **512** episodios;
- accuracy de acción FULL: **1.0**;
- accuracy de consulta FULL: **1.0**;
- masa de atención FULL sobre objetivo: **0.98549**;
- FULL−SHUFFLED_QUERY: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−ZERO_QUERY: **+0.7578125**, p=**4.99975×10⁻⁵**;
- FULL−RANDOM_QUERY: **+0.736328125**, p=**4.99975×10⁻⁵**;
- FULL−SHUFFLED_ATTENTION: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−LESION_TARGET: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−NO_BOTTLENECK: **0.0**, p=**1.0**.

Interpretación: **resultado positivo para el mecanismo combinado query+atención bajo este arnés sintético**. Las perturbaciones de query, atención y contenido objetivo eliminaron la accuracy. El control NO_BOTTLENECK fue nulo, por lo que no se establece necesidad funcional del bottleneck cuando la atención ya concentra los recursos sobre el objetivo.

### I5.6 — Integración de tarea de consulta persistente — resultado verificado

Workflow: **36988020361**; artifact **11217989623**; seed **20261006**; **24** réplicas; **24** ciclos de warmup.

- accuracy de acción real FULL: **1.0**;
- accuracy interna de predicción FULL: **1.0**;
- accuracy de query FULL: **1.0**;
- masa de atención FULL: **0.98630**;
- persistencia exacta: **100%**;
- FULL−SHUFFLED_QUERY acción: **+1.0**, p **4.99975×10⁻⁵**;
- FULL−ZERO_QUERY: **+1.0**, p **4.99975×10⁻⁵**;
- FULL−RANDOM_QUERY: **+0.8333333**, p **4.99975×10⁻⁵**;
- FULL−SHUFFLED_ATTENTION: **+0.75**, p **4.99975×10⁻⁵**;
- FULL−LESION_TARGET: **+0.75**, p **4.99975×10⁻⁵**;
- FULL−NO_BOTTLENECK: **0.0**, p **1.0**.

Interpretación: **resultado positivo para la integración a nivel de tarea de query + atención en PersistentOrganism bajo el arnés declarado**. NO_BOTTLENECK fue nulo, por lo que no se establece necesidad funcional del bottleneck.

### I5.7 — Acceso recurrente y reentrada — resultado nulo/inconcluso

Workflow: **37035390086**; artifact **11240100197**; seed **20261007**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- PULSE_SHUFFLED_QUERY: Δ estado firmado en t+1 **+0.1510**, p **0.14199**;
- PULSE_ZERO_QUERY: Δ estado firmado en t+1 **+0.1510**, p **0.14114**;
- PERSISTENT_SHUFFLED_QUERY: Δ estado firmado en t+1 **+0.00383**, p **0.9630**;
- divergencia absoluta t+1 PULSE_SHUFFLED_QUERY: **0.4424**;
- máxima divergencia absoluta posterior: **0.7267**;
- re-entry amplification media: **2.1276**;
- persistencia media: **7.0** ciclos;
- AUC media de divergencia: **2.5792**;
- cambio post-pulso de acción: **45.83%**;
- cambio post-pulso de query: **74.40%**;
- cambio post-pulso de target: **82.14%**.

Interpretación: hubo divergencia descriptiva persistente entre trayectorias, pero el endpoint primario firmado no se separó significativamente. I5.7 **no establece todavía un efecto causal de reentrada**. La igualdad de los perfiles agregados de PULSE_SHUFFLED_QUERY y PULSE_ZERO_QUERY sugiere que la perturbación actual del query es demasiado gruesa para discriminar la ruta de transmisión.

## Estado de campaña C0

La primera campaña de 32 ejecuciones quedó archivada como evidencia histórica con un fallo técnico en el archivado de artifacts. La campaña fue reiniciada con una ejecución por ondas de cuatro réplicas y una regla explícita de validación de archivos antes de publicar artifacts.

**Estado documental actualizado:** la nueva ventana de ejecución está definida en [C0 Campaign](../docs/C0_CAMPAIGN_32_RUNS.md). Ya existe una primera ola validada: **G1, 4/32 réplicas**, con workflow run **36955261246**. Los cuatro artifacts fueron producidos correctamente y sus archivos `summary.json`, `policy_snapshot.json` y metadatos de slot fueron validados. G2–G8 todavía no tienen resultados científicos registrados. Un fallo técnico de infraestructura no se convierte en un resultado nulo.



### C0 Campaign — G1 completado (4/32)

Workflow de GitHub Actions: **36955261246** (run #33), commit **0587915bf90d44872fa950bdbd62ffaaae6d7ec7**.

Criterio: **C3 causal self-reference**. Control: **information-matched state shuffle**.

| Réplica | Artifact | Effect | p | Own gap | Matched gap |
|---|---:|---:|---:|---:|---:|
| G1-R1 | 11205791665 | 0.0625 | 0.38498075096 | 0.9921875 | 0.9296875 |
| G1-R2 | 11205378393 | 0.046875 | 0.49912504375 | 0.9921875 | 0.9453125 |
| G1-R3 | 11206041359 | 0.01953125 | 0.84995750212 | 0.94140625 | 0.921875 |
| G1-R4 | 11205626944 | 0.08984375 | 0.13454327284 | 1.04296875 | 0.953125 |

Medias descriptivas de G1: effect **0.0546875**, own gap **0.9921875**, matched gap **0.9375**. Las cuatro réplicas tienen p > 0.05.

**Interpretación:** G1 es una **ola parcial validada**, no el resultado de la campaña completa. No se registra inferencia compuesta de 32 ejecuciones. G2–G8 permanecen pendientes.


## C0.18 — Adquisición autónoma y lesión/rescate del segundo orden — resultado verificado

Artifact de GitHub Actions:

- workflow run: **36960952961**;
- artifact: **11208100038**;
- SHA-256: **a7aa0554a81a3449175e37363e6fcd95ec6d5bc7d1354198f047ef888c1dbf98**;
- commit experimental: **434b3a02ab64c9294c8113171ccbac1745caa053**;
- 24 réplicas;
- 12 ciclos de adquisición autónoma por réplica;
- 48 muestras medias aprendidas por el segundo orden;
- recuperación exacta del modelo persistido: **100%**.

Contrastes primarios:

- FULL − LESION, acción: **−0.2916667**, p=**0.1177441**;
- FULL − LESION, ganancia: **+0.0114104**, p=**0.7404130**;
- RESCUE − LESION, acción: **−0.2916667**, p=**0.1183441**;
- RESCUE − LESION, ganancia: **+0.0114104**, p=**0.7332633**.

Interpretación: **resultado nulo bajo el protocolo probado**. El organismo adquirió y persistió correctamente el segundo orden, pero la lesión no produjo un cambio estadísticamente significativo en acción o ganancia y el rescate tampoco produjo recuperación significativa respecto de LESION.

C0.18, por tanto, no demuestra necesidad causal ni rescate funcional del segundo orden adquirido bajo este arnés. La adquisición/persistencia de C0.17 permanece como resultado separado.




<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Organism Experimental Result Ledger — V47 → V80 + I4/I5

## Strong positive results

### V51 — Self-Prediction
104 post-warmup transitions: MAE 0.0424 versus persistence baseline 0.2211; mean prediction gain 0.1787; 84.6% positive-gain transitions; paired sign-flip p = 0.00005.

### V57 — Self-Model-Guided Trajectory Selection
24 paired replicates: self-model regret 0.0231 versus 0.1369 random; oracle-hit rate 70.83% versus 45.83%; paired sign-flip p = 0.00435.

### V58 — Semantic → Dynamic Coupling
Paired 2×2 intervention. Bridge OFF: A/B dynamic-state delta 0.0 and signal delta 0.0. Bridge ON: Omega A -1.52, Omega B +0.68, signal delta 1.5002170539, dynamic-state delta 0.4558697583.
The deterministic harness supports causal transduction of the organism semantic-memory output into numerical internal dynamics when the bridge is enabled.

### V60 — Self-Model Selection inside a Recurrent Semantic Loop
24 paired replicates, 24 evaluation cycles.
- self-model mean regret: -0.0842091465;
- random-control mean regret: 0.3028308773;
- mean regret advantage (random - self-model): 0.3870400237;
- cumulative regret advantage: 9.2889605698;
- median regret advantage: 0.3858317486;
- paired sign-flip p for mean and cumulative advantage: 0.00005;
- self-model oracle-hit rate: 96.1806%;
- random oracle-hit rate: 45.3125%.
Interpretation: the self-model retained strong functional selection advantage in the deterministic closed-loop protocol, under a provider whose next semantic memory depends on the previously selected action. However, the self-model arm selected +1 in all 24 replicates, so the within-run action-conditioned feedback endpoint never observed both action branches. The recurrent circuit was exercised, but branch coverage for action-conditioned feedback is incomplete and must not be presented as a fully demonstrated bidirectional feedback effect.

### V62 — Causal Semantic Self-Model Bridge
24 paired replicates crossing self-model content A/B with bridge OFF/ON.
- mean state delta bridge OFF: 0.0;
- mean signal delta bridge OFF: 0.0;
- mean state delta bridge ON: 0.0567495528;
- mean signal delta bridge ON: 0.1844584720;
- bridge OFF isolated the textual intervention in every execution;
- bridge ON transduced the self-model difference into signal and state in every execution;
- persistence and versioning of the self-model were recorded in all ON executions.
Interpretation: in this deterministic intervention, changing only the organism semantic self-model altered numerical internal state only when the explicit self-model bridge was enabled. This is computational causal coupling, not evidence of subjective experience.

### V63 — Causal Self-Model Loop
24 paired replicates × 32 evaluation cycles crossing self-model/random selection with self-model bridge OFF/ON.
- mean regret bridge ON + self-model: 0.1422226601;
- mean regret bridge ON + random: 0.2666042539;
- random - self-model regret advantage: 0.1243815939;
- paired sign-flip p: 0.00005;
- self-model regret bridge OFF: 0.2876865581;
- self-model regret bridge ON: 0.1422226601;
- bridge OFF - ON regret improvement: 0.1454638980;
- paired sign-flip p for bridge effect: 0.00005;
- self-model oracle-hit rate: 10.0260% OFF → 60.6771% ON;
- paired sign-flip p for hit-rate change: 0.00005;
- regret difference-in-differences between self-model and random arms: 0.2837493367;
- paired sign-flip p for interaction: 0.00005;
- branch coverage bridge ON + self-model: 100%;
- action-conditioned bridge signal difference in bridge ON + self-model: 0.7405 across 243 negative-branch and 501 positive-branch observations.
Interpretation: the deterministic harness supports a recurrent computational loop in which prior trajectory conditions the next semantic self-model, that self-model is transduced into internal dynamics, and the resulting state participates in future trajectory selection. The action-conditioned signal comparison is an within-loop association, not an isolated causal estimate.

### V65 — SLEEP Consolidation and Future Selection
24 paired replicates × 24 evaluation cycles across no_dream, dream_no_bridge, and dream_bridge.
- no_dream mean regret: 0.3258519211;
- dream_no_bridge mean regret: 0.2109500171;
- dream_bridge mean regret: 0.1779272005;
- dream_bridge versus dream_no_bridge regret advantage: 0.0330228167;
- paired sign-flip p: 0.00005;
- dream_bridge oracle-hit rate: 25.3472%;
- dream_no_bridge oracle-hit rate: 13.3681%;
- hit-rate advantage: 0.1197916667;
- paired sign-flip p for hit-rate advantage: 0.00005;
- dream_no_bridge versus no_dream regret change: -0.1149019040;
- paired sign-flip p for SLEEP versus no_dream: 0.00005.
Interpretation: the deterministic harness supports a computational wake/sleep mechanism in which semantic consolidation generated during SLEEP changes internal state and produces a measurable later effect on trajectory selection. This does not establish subjective sleep or phenomenal consciousness.

## Negative / null results / limitations

### V53
The original three-candidate selector chose the neutral signal in all 12 replicates and produced no causal divergence relative to zero-input control. Treated as a failed discriminative protocol, not positive evidence.

### V54
Self-forecast accuracy over 80 cycles with a fake provider was 43.75%, with 40 TOWARD and 40 AWAY transitions. Chance for the balanced binary task is 50%; V54 did not provide favorable evidence.

### V55
12 replicates × two perturbation signs × selection ON/OFF retained the identity trace in 100% of executions and recovered within horizon in 100%, mean recovery time 2.5 cycles. ON and OFF both recovered at 100%, so V55 demonstrates resilience under the tested harness but no selective self-model benefit.

### V59 — Semantic Bridge × Self-Model Selection
24 paired factorial replicates crossing semantic bridge OFF/ON with self-model/random policy.
- self-model mean regret OFF: 0.0000;
- random mean regret OFF: 0.23233;
- self-model mean regret ON: 0.0000;
- random mean regret ON: 0.24022;
- self-model oracle-hit rate: 100% in both bridge conditions;
- random oracle-hit rate: 50% in both;
- bridge changed post-WAKE internal state by mean absolute 0.94273 and dynamic signal by 0.55376;
- bridge × selection interaction: +0.00789;
- interaction sign-flip p = 0.83941.
Interpretation: the protocol reproduces prior self-model selection advantage and separately shows substantial semantic-to-dynamic transduction. The factorial interaction did not separate from zero in this deterministic harness; V59 therefore does not support a claim that the semantic bridge itself increases self-model selection utility. It remains a null interaction/compositionality result.

### V61 — Metacognitive Self-Model
24 paired replicates × 32 evaluation cycles.
- metacognitive self-model mean regret: 0.0888081147;
- first-order self-model mean regret: 0.0787785152;
- random-control mean regret: 0.1929241942;
- metacognitive oracle-hit rate: 41.2760%;
- first-order oracle-hit rate: 45.3125%;
- random oracle-hit rate: 46.4844%;
- metacognitive regret advantage versus first order: -0.0100295995;
- paired sign-flip p: 0.00005;
- metacognitive hit-rate advantage versus first order: -0.0403645833;
- paired sign-flip p: 0.0008999550;
- metacognitive prediction MAE: 0.1277240710;
- constant-baseline MAE: 0.0849867822;
- metacognitive model outperformed constant baseline in 0% of replicates.
Interpretation: the implemented second-order metacognitive model did not improve trajectory selection or predict first-order error better than a constant baseline under this harness. Preserved as a negative finding pointing to redesign.

### V64 — Identity Persistence under Self-Model Perturbation
24 paired replicates tested whether identity-specific dynamic signatures remained decodable after a common semantic self-model overwrite, explicit removal of self-model text, and autonomous continuation without semantic input.
- post-ablation accuracy bridge OFF: 50.0%;
- post-ablation accuracy bridge ON: 50.0%;
- ON - OFF accuracy: 0.0;
- paired sign-flip p: 1.0;
- above-chance folds: 0% in both conditions.
Interpretation: V64 produced a null result. Under the tested perturbation, feature set, classifier, and horizon, original identity was not decodable after semantic self-model overwrite and textual ablation. This is preserved as a real limitation, not evidence against all possible identity persistence.

### V66 — SLEEP Consolidation after Episodic-Memory Ablation
24 paired replicates tested whether keeping only the consolidated lesson after SLEEP was sufficient to change later trajectory selection once original episodic memories were removed.
- retained_lesson mean regret: -0.1086777912;
- ablated_lesson mean regret: -0.1086777912;
- retained_lesson oracle-hit rate: 85.0694%;
- ablated_lesson oracle-hit rate: 85.0694%;
- regret difference (ablation - retained): 0.0;
- paired sign-flip p for regret: 1.0;
- hit-rate advantage (retained - ablated): 0.0;
- paired sign-flip p for hit rate: 1.0;
- all retained executions produced a recovery-bridge signal.
Interpretation: V66 is a null result. The retained lesson was present and generated a semantic recovery signal, but preserving it produced no measurable behavioral difference in regret or oracle hit rate under this deterministic pathway.

### V67 — Numerical Trace Generated During SLEEP after Total Semantic Ablation
V67 underwent a methodological correction before interpretation. The first implementation mutated stable_state in the stable_swap arm and then reused that already-mutated object as the source for frontier_swap. That exchange was contaminated and is not treated as evidence.
The corrected implementation captures both dynamic cores before any mutation and adds an integrity control.
24 replicates, 12 continuation steps:
- mean stable − frontier SLEEP signal difference: -0.3092749945;
- mean stable − frontier dynamic-state difference: -0.0682840349;
- post-ablation own-continuation classification accuracy: 50.0%;
- paired sign-flip p: 1.0;
- transferred-state tracking accuracy: 50.0%;
- paired sign-flip p: 1.0;
- exact source-core reproduction: 100%;
- memories removed before probe: yes;
- self-model removed before probe: yes;
- textual input during probe: no.
Interpretation: null result. SLEEP produced a measurable proximal state/signal difference, but that difference did not remain as a classifiable signature after semantic ablation and did not transfer causally by dynamic-core exchange.

### V68 — Temporal Persistence of the SLEEP-Generated Dynamic Trace
24 replicates, total semantic ablation, horizons 0, 1, 2, 4, 8, 16, 32.
- proximal SLEEP signal difference: -0.3092749945;
- proximal dynamic-state difference: -0.0675162088;
- horizon 0 final mean delta: -0.0675162, p=0.00005;
- horizon 1: -0.0003984, p=0.13279;
- horizon 2: 0.0152969, p=0.14059;
- horizon 4: -0.0336304, p=0.00070;
- horizon 8: 0.0065469, p=0.00005;
- horizon 16: 0.0095700, p=0.00005;
- horizon 32: 0.0067923, p=0.00045;
- mean trajectory RMSE: 0.06729 → 0.02006 between horizons 0 and 32;
- causal exchange integrity: 100% exact source-core trajectory match.
Interpretation: SLEEP writes an immediate numerical difference and transferred cores reproduce source trajectories causally, but separation from the original semantic condition falls sharply after the first step and remains small/non-monotonic. Evidence favors a transient/attenuated dynamic trace, not demonstrated persistent semantic memory.

### V69 — Reading Own State after Semantic Ablation
24 replicates and one shared SelfObserver trained on 512 generic dynamics transitions, independent of stable/frontier conditions.
- mean stable vs frontier prediction difference: 0.04035657;
- prediction difference after exchange: 0.0;
- decision sensitivity with readable state: 66.6667% (16/24);
- decision sensitivity with blinded state: 0.0%;
- paired p for ON − OFF: 0.000099995;
- decision change after state exchange with readout ON: 66.6667%;
- decision change after exchange with readout OFF: 0.0%;
- paired p for decision change ON − OFF: 0.000099995;
- memory, events, snapshots, and self-model text removed before probe;
- no semantic input during probe.
Interpretation: V69 supports a computational **self-readout → prediction → selection** mechanism. The same dynamic state difference written during SLEEP is read by a learned dynamic model and used to select a signal. State exchange changes the decision in the same state-sensitive replicates. This is operationalized self-reference within the deterministic harness, not phenomenal consciousness.

### V70 — Persistent Self-Reader across Restarts
24 replicates and 256 generic training samples.
- reader persisted separately from semantic memory: yes;
- reader survived restart: yes;
- samples before/after restart: 256 / 256;
- maximum absolute prediction error before/after: 0.0;
- exact model load: 100%;
- decision sensitivity with readout ON: 29.1667%;
- blinded-state sensitivity OFF: 0.0%;
- paired ON − OFF p: 0.0143493;
- decision change after dynamic-core exchange with readout ON: 29.1667%;
- memories removed before probe: yes;
- self-model text removed: yes;
- no semantic input during probe.
Interpretation: V70 shows that the numerical self-reader can persist in SQLite, survive restart, and be reused after semantic surfaces are removed. Decision sensitivity is lower than V69 but remains separated from blinded control.

### V69 — Reading Own State through a Self-Model
24 replicates, 48 identical calibration cycles before SLEEP, numerical self-model frozen before SLEEP, and total semantic ablation.
- post-SLEEP state difference stable − frontier: -0.0963430681;
- mean absolute self-model score difference: 0.0344099851, p=0.00005;
- mean absolute prediction difference: 0.0365052134, p=0.00005;
- identical numerical self-models between conditions: 100%;
- action change from real versus control-state readout: 0%;
- action diversity: one distinct action across all reads;
- memories and self-model text removed before probe;
- no textual input during probe.
Interpretation: V69 separates state reading from behavioral use. Numerical self-state readout is positive, but action selection is null under the current selector because it collapsed to one action.

### V70 — Self-Model → Action after Semantic Ablation
24 replicates, 48 identical calibration cycles, numerical self-model frozen before intervention.
- mean difference in self-model-derived action: 0.1224593696, p=0.00005;
- state-prediction difference: 0.0257983935, p=0.00005;
- mean difference between action from real readout and clamped state: 0.0456327609, p=0.00005;
- clamped-control action difference: 0.0311938478;
- post-exchange mean action error: 0.0;
- mean absolute post-action state difference: 0.0136089447;
- numerical self-models identical: 100%;
- memories and self-model text removed;
- no semantic input during probe.
Interpretation: V70 extends V69 from reading to action. A self-model frozen before SLEEP turns the post-SLEEP internal state into a continuous action signal; actions differ between conditions and alter the next state after semantic ablation. This establishes computational self-model → action coupling, while the mapping from prediction to action was externally fixed by the protocol.

### V77 — Generalization to unseen causal structures
64 replicates per condition; training only on single_impulse; OOD split_impulse, reversal_pulse, delayed_impulse.
- learned mean gain: 0.2377583;
- blinded: -0.1917033;
- fixed: -0.1566228;
- random: 0.0632567;
- learned − blinded p: 0.00005;
- learned − fixed p: 0.00005;
- learned − random p: 0.00005;
- learned − random advantage in-domain: 0.1715437;
- learned − random advantage OOD: 0.1754876;
- OOD/in-domain retention: 1.0230;
- learned continuity: 0.7926861 vs random 0.7950760, p=0.48033;
- state-dependent first action under reversal_pulse: 100% vs 0% blinded;
- maximum immediate intervention-target error: 0.0.
Interpretation: V77 supports computational generalization of the self-prediction policy to unseen temporal/causal structures. Continuity, as a secondary endpoint, did not separate from random.

### V78 — Active Continuity under Repeated Perturbations
64 replicates per condition; training only on single_impulse; OOD double_same_sign, double_alternating, triple_alternating.
- learned mean gain: 0.2422976;
- blinded: -0.2408441;
- fixed: -0.1844678;
- random: 0.0518725;
- learned − blinded p: 0.00005;
- learned − fixed p: 0.00005;
- learned − random p: 0.00005;
- learned − random advantage in-domain: 0.1897230;
- learned − random advantage OOD: 0.1906591;
- OOD/in-domain retention: 1.0049;
- OOD second-event change from first: -0.0173461;
- learned continuity: 0.7905914 vs random 0.7922640, p=0.58767;
- OOD state-dependent first action first event: 100% vs 0% blinded;
- OOD state-dependent first action second event: 100% vs 0% blinded;
- maximum target-match error after each intervention: 0.0.
Interpretation: V78 supports temporal/compositional reuse of the self-prediction policy under repeated unseen perturbation sequences without retraining. A small degradation appears between the first and second event, but overall OOD advantage over random remains. Continuity did not separate from random.

### V79 — Online Self-Policy Adaptation
64 replicates per condition; single_impulse training; in-domain and modified-regime evaluation including OOD triple_alternating.
- frozen in-domain gain: 0.2109118;
- adaptive in-domain gain: 0.2109118;
- shifted-single frozen: 0.3792665;
- shifted-single adaptive: 0.3792665;
- shifted-repeated frozen: 0.3799345;
- shifted-repeated adaptive: 0.3798509;
- adaptive advantage at third OOD event: -0.0002509;
- paired p: 1.0;
- adaptive − frozen difference-in-differences: -0.0002509, p=1.0;
- OOD adaptive continuity: 0.7270149 vs frozen 0.7268716, p=1.0;
- maximum target error: 0.0.
Interpretation: null result for online adaptation under the tested protocol. The adaptive copy incorporated observed gains but did not separate from frozen. The dynamic shift did not degrade frozen enough to reveal an adaptive advantage.

### V80 — Online Adaptation under Reversible Regime Changes
64 replicates per condition; single_impulse training; evaluation base → shift_a → shift_b → base_return; matched policy snapshot.
- primary base_return event 3 adaptive − frozen: -0.0103649267, p=0.0504475;
- shift_a event 3 adaptive − frozen: -0.0062218940, p=0.00114994;
- shift_b event 3 adaptive − frozen: +0.0000024599, p=0.9976001;
- adaptive base_return event 3 − event 1: -0.0021765106;
- frozen base_return event 3 − event 1: -0.0004681112;
- differential recovery adaptive − frozen: -0.0017083995;
- maximum intervention error: 0.0.
Interpretation: **null result for adaptive advantage under the tested protocol**. Adaptive policy, which incorporated only observed self-prediction gain online, did not outperform frozen after two regime shifts and return to base. The base_return difference was slightly negative and shift_a also numerically favored frozen; shift_b showed no appreciable separation. This does not invalidate all online adaptation; it constrains one policy, dynamics, and horizon.

## I5 — Global workspace

### I5.1 — Workspace integration into PersistentOrganism — null behavioral result

Verified workflow: **36984060538**; artifact **11216653205**; experimental commit **993ba8184c1536c7e781bde1fe9797c6b20a38dccd8269f03d3f13da2ebd48cd**.

- 24 paired replicates;
- workspace-state persistence after restart: **100%**;
- NO_BROADCAST − FULL, regret: **+0.0212423**, p=**0.4928254**;
- NO_WORKSPACE − FULL, regret: **+0.0212423**, p=**0.5026749**;
- LESION − FULL, regret: **0.0**, p=**1.0**;
- FULL vs NO_BROADCAST action-change rate: **25%**;
- FULL vs LESION action-change rate: **0%**.

Interpretation: **null result under the tested broadcast→trajectory mapping**. Workspace integration and persistence are operational, but the implemented broadcast did not produce a detectable behavioral separation on the prespecified endpoints. This does not invalidate the isolated I5.0 mechanism.

### I5.2 — State-dependent workspace query — verified result

Verified workflow: **36984675391**; artifact **11216743506**; experimental commit **0b857f7c93e5a7112b184840f36994712aed2967**.

- seed **20261002**;
- **512** episodes;
- FULL accuracy: **1.0**;
- FULL − SHUFFLED: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL − ZERO: **+0.771484375**, p=**4.99975×10⁻⁵**;
- FULL − RANDOM: **+0.7421875**, p=**4.99975×10⁻⁵**;
- LESION accuracy: **0.236328125**;
- FULL − LESION: **+0.763671875**, p=**4.99975×10⁻⁵**;
- state-dependent query-change rate: **1.0**.

Interpretation: **positive result for the tested computational mechanism**. The implemented global state controlled selection of the next module, and lesioning the selected source sharply reduced query accuracy. This remains a standalone GWT-4 mechanism result under a synthetic harness; it does not demonstrate consciousness or subjective experience and does not replace causal integration into PersistentOrganism.

## I5.3 — Causal attention allocation — verified result

Verified workflow: **36985957522**; artifact **11218020500**; experimental commit **60263ada3a28af29c3f1fa29246355bb434242fc**.

- seed **20261003**;
- **512** episodes;
- FULL target attention mass: **0.9845638420**;
- FULL − SHUFFLED target mass: **+0.9768188958**, p=**4.99975×10⁻⁵**;
- FULL − UNIFORM target mass: **+0.7345638420**, p=**4.99975×10⁻⁵**;
- FULL − RANDOM target mass: **+0.7429394202**, p=**4.99975×10⁻⁵**;
- FULL − LESION target mass: **+0.7345638420**, p=**4.99975×10⁻⁵**;
- attention selection-change rate: **1.0**.

Interpretation: **positive result for the tested computational mechanism**. The attention model reproducibly concentrated resources on the target module and the controls removed that concentration. The LESION condition is an operational loss-of-concentration control, not an anatomical lesion.

## I5.4 — Persistent query + attention integration — null/mixed result

Verified workflow: **36986823516**; artifact **11217906875**; experimental commit **27f08ab3d84633986a609a7981429cf6f3fe0cf5**.

- seed **20261004**;
- **24** replicates;
- **24** warmup cycles;
- SHUFFLED_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- SHUFFLED_ATTENTION regret cost: **+0.0280384**, p=**0.5022**; action-change **20.83%**;
- ZERO_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- RANDOM_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- LESION_QUERY regret cost: **0.0**, p=**1.0**; action-change **0%**;
- FULL mean attention mass: **0.69550**;
- FULL mean selective-access strength: **0.30500**;
- exact persistence: **100%**.

Interpretation: **null/mixed result under the tested protocol**. The integrated chain is operational and its observables persist, but query controls did not change action or regret. Attention reassignment changed the action in 20.83% of replicates, but regret cost was not significant. The integration therefore does not establish functional necessity of selective access under this mapping.

## I5.5 — Causal query bottleneck — verified result

Verified workflow: **36987408988**; artifact **11218415785**; experimental commit **906f67544517add411f1c97176042a253a3caa19**.

- seed **20261005**;
- **512** episodes;
- FULL action accuracy: **1.0**;
- FULL query accuracy: **1.0**;
- FULL target attention mass: **0.98549**;
- FULL−SHUFFLED_QUERY: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−ZERO_QUERY: **+0.7578125**, p=**4.99975×10⁻⁵**;
- FULL−RANDOM_QUERY: **+0.736328125**, p=**4.99975×10⁻⁵**;
- FULL−SHUFFLED_ATTENTION: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−LESION_TARGET: **+1.0**, p=**4.99975×10⁻⁵**;
- FULL−NO_BOTTLENECK: **0.0**, p=**1.0**.

Interpretation: **positive result for the combined query+attention mechanism under this synthetic harness**. Query, attention, and target-content perturbations eliminated accuracy. NO_BOTTLENECK was null, so bottleneck necessity is not established when attention already concentrates resources on the target.

### I5.6 — Persistent query-task integration — verified result

Workflow: **36988020361**; artifact **11217989623**; seed **20261006**; **24** replicates; **24** warmup cycles.

- FULL actual action accuracy: **1.0**;
- FULL internal prediction accuracy: **1.0**;
- FULL query accuracy: **1.0**;
- FULL attention mass: **0.98630**;
- exact persistence: **100%**;
- FULL−SHUFFLED_QUERY action: **+1.0**, p **4.99975×10⁻⁵**;
- FULL−ZERO_QUERY: **+1.0**, p **4.99975×10⁻⁵**;
- FULL−RANDOM_QUERY: **+0.8333333**, p **4.99975×10⁻⁵**;
- FULL−SHUFFLED_ATTENTION: **+0.75**, p **4.99975×10⁻⁵**;
- FULL−LESION_TARGET: **+0.75**, p **4.99975×10⁻⁵**;
- FULL−NO_BOTTLENECK: **0.0**, p **1.0**.

Interpretation: **positive result for task-level query + attention integration in PersistentOrganism under the declared harness**. NO_BOTTLENECK was null, so functional bottleneck necessity remains unestablished.

### I5.7 — Recurrent self-access and re-entry — null/inconclusive result

Workflow: **37035390086**; artifact **11240100197**; seed **20261007**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- PULSE_SHUFFLED_QUERY: signed state delta at t+1 **+0.1510**, p **0.14199**;
- PULSE_ZERO_QUERY: signed state delta at t+1 **+0.1510**, p **0.14114**;
- PERSISTENT_SHUFFLED_QUERY: signed state delta at t+1 **+0.00383**, p **0.9630**;
- PULSE_SHUFFLED_QUERY absolute divergence at t+1: **0.4424**;
- maximum later absolute divergence: **0.7267**;
- mean re-entry amplification: **2.1276**;
- mean persistence: **7.0** cycles;
- mean divergence AUC: **2.5792**;
- post-pulse action change: **45.83%**;
- post-pulse query change: **74.40%**;
- post-pulse target change: **82.14%**.

Interpretation: persistent trajectory divergence was descriptive, but the primary signed endpoint did not separate significantly. I5.7 **does not yet establish a causal re-entry effect**. The identical aggregate profiles of PULSE_SHUFFLED_QUERY and PULSE_ZERO_QUERY suggest that the current query perturbation is too coarse to discriminate the transmission pathway.

## C0 campaign and causal controls

### C0.2 — Operational instantiation of TCF candidate properties
64 episodes per condition; 64 training episodes; 512 self-observation samples; 12 recovery steps; full/state_blind/no_persistence/open_loop; same policy snapshot; no semantic input or external retraining during the probe.
Artifact: GitHub Actions run 36838186533, artifact 11149578956; experimental commit 78bf3000739b1711ce01873cc4ab058e334c5881.
Predefined FULL − control contrasts:
- C1 persistent own state: +0.716560, p=4.99975e-05;
- C2 self/environment differentiation: +2.000000, p=4.99975e-05;
- C3 causal self-reference: +1.000000, p=4.99975e-05;
- C4 trajectory continuity: +0.287204, p=4.99975e-05;
- C5 endogenous dynamics: +0.042818, p=4.99975e-05;
- C6 reorganization: +0.468787, p=4.99975e-05;
- C7 recurrent closure: +1.250000, p=4.99975e-05;
- maximum intervention error: 0.0.
Interpretation: C0.2 produced positive separation on all seven operational observables under the tested implementation. This documents computational properties under the tested conditions; **it does not demonstrate phenomenal consciousness or subjective experience**. C7 was corrected before this final record to measure action → own state → action rather than only action effect on next state.

### C0.3 — Information-matched causal self-reference control
64 episodes; 8 fixed-point-free permutations per episode; same policy snapshot; control states sampled from the empirical FULL trajectory distribution.
Artifact: GitHub Actions run 36838675864, artifact 11150238362; commit 413e70499977d759e9effb50505c4db6174925c8.
- own-state to mixed-state gap: 1.06640625;
- gap between two mixed states: 1.00000000;
- contrast: +0.06640625;
- sign-permutation p: 0.3140343;
- real-action versus mixed-state discrepancy: 0.5332031.
Interpretation: null/inconclusive under the information-matched C3 specificity control. The FULL − STATE_BLIND difference from C0.2 did not separate from a control preserving the state distribution while breaking episode correspondence.

### C0.4 — Information-matched action-replay control
64 episodes; 8 replay sequences per episode; 64 training episodes; 512 self-observer samples; same initial context and dynamic seed; replay action sequence donated by another episode.
Artifact: GitHub Actions run 36838953166; artifact 11150575990; commit 7e8adcfd8aed0df514662912ded4482c6bda7ad0.
- FULL autonomous variance: 0.0531008831;
- action-replay variance: 0.0543576360;
- FULL − replay: -0.0012567529;
- sign-permutation p: 0.4364282.
Interpretation: null under the information-matched C5 control. FULL autonomous variance did not exceed replayed action sequences from the same organism when online state/action correspondence was broken. The C0.2 OPEN_LOOP separation is therefore interpretation-limited because that control fixed action to zero.

### C0.5 — Information-matched recurrent-closure control
64 episodes; 8 donor-action rearrangements per episode; same policy snapshot; donor actions drawn from the same empirical action distribution.
Artifact: GitHub Actions run 36938229171; artifact 11199385083; SHA256 ee3d1260692ba7aa2ba683e7caefba46a0662ca3c887aea0ca0bf3e872e6adf8; commit ce62945a3ae2c1642a9450e30e81e6ef094b523e.
- real action-chain gap: 0.99609375;
- matched donor-action gap: 0.99218750;
- contrast: +0.00390625;
- p: 1.0;
- no semantic input;
- no external retraining.
Interpretation: null under the information-matched C7 control. The action → own state → action chain did not separate from the chain constructed from donor actions drawn from the same empirical distribution. The positive C0.2 C7 contrast is therefore not confirmed under this stronger control.

### C0.6 — Causal lesion/rescue of self-observer and self-policy
64 episodes; 64 training episodes; 512 self-observer samples; one shared trained snapshot across conditions, followed by post-training lesions and rescue.
Artifact: GitHub Actions run 36939000398; artifact 11198659986; SHA256 cf3442ec57c49b803ae1514aad6c5f4a727651f61dc45864cc803a1c4c35a198; commit 07943dd5ea979e6d78ed3cd01e0135e35e6de58c.
- observer necessity FULL − OBSERVER_LESION gain: +0.2273943, p=0.00005;
- policy necessity FULL − POLICY_LESION gain: +0.3555158, p=0.00005;
- joint necessity FULL − BOTH_LESION: +0.2273943, p=0.00005;
- observer lesion final-distance effect: +0.5125025, p=0.00005;
- policy lesion final-distance effect: +0.1065877, p=0.00005;
- observer rescue: +0.2076185, p=0.00005;
- policy rescue: +0.2875335, p=0.00005;
- maximum intervention error: 0.0;
- no semantic input during probe;
- no external retraining during probe.
Interpretation: C0.6 shows causal dependence of the trained components under the tested lesion/rescue protocol. Post-training removal of learned self-observer or self-policy changes recovery/trajectory metrics, and restoring them in the same experimental trajectory produces significant rescue. This is evidence of computational component necessity/recovery under the test; it is not by itself evidence of phenomenal consciousness.

### C0.7 — Target-permutation specificity control for the self-model
64 episodes; 64 training episodes; 512 self-observer samples; fixed target permutation preserving feature matrix and target multiset; same evaluation dynamics/seeds between arms.
Artifact: GitHub Actions run 36939278865; experimental commit 5e0e1f52eea76c73b5e9e8273b63bd3d810ed7ff.
- FULL − target-permuted gain: +0.0286062, p=0.0019999;
- target-permuted − FULL final distance: -0.0113629, p=0.7047648;
- FULL − target-permuted state variance: +0.0198325, p=0.00005;
- FULL − target-permuted mean action magnitude: 0.0, p=1.0;
- FULL gain: 0.2128723;
- target-permuted gain: 0.1842661;
- FULL variance: 0.0811531;
- target-permuted variance: 0.0613206;
- maximum intervention error: 0.0.
Interpretation: C0.7 shows specificity toward the feature → target assignment for self-prediction gain and internal variance under the tested control, while final distance and action magnitude do not separate. This supports a narrower interpretation that part of behavior depends on the learned mapping rather than only model size or marginal target distribution. It is not evidence of phenomenal consciousness.

### C0.8 — Crossed observer/policy coupling — corrected statistics
The initial execution completed four conditions with matched seeds, but the implementation incorrectly treated one scalar interaction contrast as 64 repeated pseudo-replicates for p-value calculation. Those p-values are not used as evidence.
Descriptive first-execution means:
- TT: gain 0.21888936; final distance 0.15996548; variance 0.06848248;
- TP: gain -0.12484394; final distance 0.67765194; variance 0.07943683;
- PT: gain -0.31516985; final distance 0.67765194; variance 0.07943683;
- PP: gain 0.20488969; final distance 0.14799625; variance 0.06747759.
The final-distance interaction initially used the opposite sign from the declared contrast. The implementation was corrected to compute TT − TP − PT + PP elementwise by shared episode seed, using the same sign convention for final distance.

### C0.8 — Confirmatory verified result
Artifact: GitHub Actions run 36946477790; artifact 11202930418; SHA256 e8ce5229e0f41a31a3923cc802b18a19c98c4d61ffa68eda601e18ac80c26987.
- observer effect on gain TT − PT: +0.5340592, p=4.99975e-05;
- policy effect on gain TT − TP: +0.3437333, p=4.99975e-05;
- observer × policy interaction on gain: +0.8637928, p=4.99975e-05;
- observer × policy interaction on variance: -0.0229136, p=0.0022999;
- observer × policy interaction on final distance: -1.0473422, p=4.99975e-05;
- maximum intervention error: 0.0;
- no semantic input or external retraining during probe.
Interpretation: the confirmatory execution supports separable observer, policy, and matched observer/policy coupling effects under the protocol. This is a computational organization result, not evidence of subjective experience.

### C0.9 — Causal observer → policy interface
Verified artifact run 36944916227, artifact 11200913836, SHA256 287f52b0074a8599be74ae0d36bfbbc930cdb892cb48d0cde96a5e649af5f3d6.
- donor-shuffle readout gap: 0.1975998565;
- NORMAL − DONOR action: 0.0, p=1.0;
- NORMAL − DONOR gain: 0.0, p=1.0;
- NORMAL − DONOR next state: 0.0, p=1.0;
- maximum intervention error: 0.0.
Interpretation: null for behavioral dependence on the observer → policy correspondence under the tested protocol. Observer readout changed, but policy behavior did not.

### C0.10 — Temporal observer → policy alignment
Verified artifact run 36944920225, artifact 11201258435, SHA256 7d24c622c02a331e2d3844037abccbd93365ea9de54149da77e68fc2ac631e75.
- current-versus-lagged observer prediction gap: 0.1624331804;
- NORMAL − LAG action: 0.0, p=1.0;
- NORMAL − LAG gain: 0.0, p=1.0;
- NORMAL − LAG next state: 0.0, p=1.0;
- maximum intervention error: 0.0.
Interpretation: null for behavioral sensitivity to temporal observer → policy alignment.

### C0.11 — Causal action mediation
Verified artifact run 36944924071, artifact 11200748887, SHA256 d6f496ebe49b494a8af30932a30c73880a26981da079932d9ff8a9348b2d56cd.
- next action FACTUAL − FORCED: +1.78125, p=4.99975e-05;
- next state FACTUAL − FORCED: -0.5770045054, p=4.99975e-05;
- gain FACTUAL − FORCED: +0.5278692817, p=4.99975e-05;
- mean absolute next-action discrepancy: 1.78125;
- mean absolute state discrepancy: 0.5770045054;
- maximum intervention error: 0.0.
Interpretation: positive computational causal mediation under the tested protocol. Changing only the first action produced later state and next-action differences using the same self-observer and policy. This supports the operational action → internal state → readout/policy → next action chain. It does not establish subjective experience.

### C0.12 — Second-order self-monitoring
Verified artifact run 36945173829, artifact 11201243817, SHA256 6fa8bdf64401a96d79f1d47b03dc4ac242c6456fba9c8e6957e44d52aa2448f4.
- TRUE − PERMUTED action: 0.0, p=1.0;
- TRUE − PERMUTED gain: 0.0, p=1.0;
- TRUE − BLIND action: -1.0, p=4.99975e-05;
- TRUE − BLIND gain: +0.2733195, p=4.99975e-05;
- held-out second-order MAE advantage over constant baseline: +0.00697175, p=0.00079996;
- second-order MAE: 0.04131592;
- constant-baseline MAE: 0.04828767;
- maximum intervention error: 0.0.
Interpretation: second-order model learned predictive information about first-order model error and changes action versus the blind baseline, but target permutation leaves action and gain unchanged. C0.12 therefore supports second-order prediction but not causal specificity of the second-order mapping into action.

### C0.13 — Action-conditioned second-order self-model
Verified artifact run 36945340705, artifact 11201464566, SHA256 971e0b39360eaa25828abc0162e1cf70b5c54ae4916611d7a8e06413165b7b56.
- TRUE − PERMUTED action: -1.71875, p=4.99975e-05;
- TRUE − PERMUTED gain: +0.4850290, p=4.99975e-05;
- TRUE − BLIND action: -1.0, p=4.99975e-05;
- TRUE − BLIND gain: +0.2590892, p=4.99975e-05;
- held-out MAE advantage: +0.00740228, p=4.99975e-05;
- meta MAE: 0.03489674;
- constant-baseline MAE: 0.04229902;
- intervention target error: 0.0.
Interpretation: C0.13 produced separation between the trained action-conditioned second-order model and target-permuted control under the tested protocol. The model also predicts first-order error better than the constant baseline on held-out transitions. Computational result only.

### C0.14 — Persistent second-order
Verified artifact run 36945659490, artifact 11201664192, SHA256 8a01bef161939ba7d72f3d225a73e7e5f8b2fe014e5d7a4b82856e140d44a831.
- post-restart action mismatch: 0.0, p=1.0;
- post-restart gain mismatch: 0.0, p=1.0;
- exact checkpoint model-digest recovery: 100%;
- post-restart mean gain: 0.08710124;
- maximum action mismatch: 0.0;
- maximum gain mismatch: 0.0.
Interpretation: first- and action-conditioned second-order models were serialized, restored, and reused after rebuilding dynamic context and bridge, matching the continuous arm under the tested protocol. This supports computational persistence across restart.

### C0.15 — Persistent second-order lesion/rescue
Verified artifact run 36945882211, artifact 11202160302, SHA256 5c297e25f01036b87f63ab0355555faf80dc4a2462199f5c7e115b62cbadcd6f.
- FULL − LESION late action: +0.271484375, p=0.00064997;
- FULL − LESION late gain: +0.03751679, p=0.08415;
- FULL − RESCUE post-restore action: +0.02734375, p=0.68607;
- FULL − RESCUE post-restore gain: -0.03525716, p=0.03860;
- exact checkpoint fraction: 100%;
- maximum absolute action difference FULL/LESION: 1.0.
Interpretation: disabling only the second-order selector changes later action distribution, but the gain endpoint is not significant. Restoration brings action contrast near zero but does not reproduce FULL-arm gain; rescue is therefore not a clean functional rescue. C0.15 supports action-level dependence while leaving performance-level necessity/rescue unresolved.

### C0.16 — Second-order integrated into PersistentOrganism
Verified artifact run 36946260825, artifact 11201973015, SHA256 52e60a8bb92b0c4520e1f2cc94cd138daf81bceef9138e009b6dbee635d0833e.
- post-restart action mismatch: 0.0, p=1.0;
- post-restart gain mismatch: 0.0, p=1.0;
- exact SQLite model-digest recovery: 100%;
- pre-restart action match: 100%;
- all post-restart selections reported action_conditioned_second_order;
- maximum action mismatch: 0.0;
- maximum gain mismatch: 0.0.
Interpretation: C0.16 moves action-conditioned second order from isolated laboratory component into the real PersistentOrganism lifecycle. Both models are persisted in SQLite, automatically restored after restart, and continue autonomous selection without external input or retraining. This demonstrates computational integration/persistence, not subjective experience.

### C0.17 — Autonomous second-order acquisition
Verified artifact run 36946964601, artifact 11201784892, SHA256 bf4aed2caaaff14e3aac2dca54e584cc0c10d38f9dde13c0f4720db8eacc9ea8.
- second-order model started empty;
- 48 learned second-order samples per replicate;
- exact model recovery at evaluation-pair construction: 100%;
- first TRUE − PERMUTED action: +0.2916667, p=0.3417829;
- first TRUE − PERMUTED gain: -0.0141513, p=0.7728114;
- mean TRUE − PERMUTED action: +0.0833333, p=0.6331683;
- mean TRUE − PERMUTED gain: +0.0256299, p=0.4691765;
- no semantic input during acquisition/evaluation;
- no external retraining during evaluation.
Interpretation: mixed/null result. The organism did autonomously acquire a second-order model from counterfactual prediction errors, but frozen TRUE versus target-permuted comparisons did not produce significant action/gain separation. Autonomous model acquisition/persistence is demonstrated; causal behavioral specificity is not.

## C0 campaign status
The original 32-execution campaign is archived as historical evidence with an artifact-archival technical failure. The campaign was restarted with four-replicate waves and explicit file validation before artifact publication.
**Current documented status:** the new execution window is defined in [C0 Campaign](../docs/C0_CAMPAIGN_32_RUNS.md). A first validated wave exists: **G1, 4/32 replicates**, workflow run **36955261246**. All four artifacts were produced correctly and their summary.json, policy_snapshot.json, and slot metadata were validated. G2–G8 have no scientific results recorded yet. Infrastructure failure is not converted into an experimental null.

### C0 Campaign — G1 completed (4/32)
GitHub Actions workflow: **36955261246** (run #33), commit **0587915bf90d44872fa950bdbd62ffaaae6d7ec7**.
Criterion: **C3 causal self-reference**. Control: **information-matched state shuffle**.
| Replicate | Artifact | Effect | p | Own gap | Matched gap |
|---|---:|---:|---:|---:|---:|
| G1-R1 | 11205791665 | 0.0625 | 0.38498075096 | 0.9921875 | 0.9296875 |
| G1-R2 | 11205378393 | 0.046875 | 0.49912504375 | 0.9921875 | 0.9453125 |
| G1-R3 | 11206041359 | 0.01953125 | 0.84995750212 | 0.94140625 | 0.921875 |
| G1-R4 | 11205626944 | 0.08984375 | 0.13454327284 | 1.04296875 | 0.953125 |
Descriptive G1 means: effect **0.0546875**, own gap **0.9921875**, matched gap **0.9375**. All four replicates have p > 0.05.
Interpretation: G1 is a **validated partial wave**, not the result of the full campaign. No composite inference over 32 executions is recorded. G2–G8 remain pending.

## C0.18 — Autonomous second-order acquisition and lesion/rescue — verified result
GitHub Actions artifact:
- workflow run: **36960952961**;
- artifact: **11208100038**;
- SHA-256: **a7aa0554a81a3449175e37363e6fcd95ec6d5bc7d1354198f047ef888c1dbf98**;
- experimental commit: **434b3a02ab64c9294c8113171ccbac1745caa053**;
- 24 replicates;
- 12 autonomous acquisition cycles per replicate;
- mean 48 learned second-order samples;
- exact persisted-model recovery: **100%**.
Primary contrasts:
- FULL − LESION, action: **-0.2916667**, p=**0.1177441**;
- FULL − LESION, gain: **+0.0114104**, p=**0.7404130**;
- RESCUE − LESION, action: **-0.2916667**, p=**0.1183441**;
- RESCUE − LESION, gain: **+0.0114104**, p=**0.7332633**.
Interpretation: **null result under the tested protocol**. The organism acquired and persisted second order correctly, but lesion did not produce significant action/gain change and rescue did not produce significant recovery relative to LESION. C0.18 therefore does not demonstrate causal necessity or functional rescue of the acquired second-order mechanism under this harness. C0.17 acquisition/persistence remains a separate result.

</details>