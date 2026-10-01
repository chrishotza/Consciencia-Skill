# Registro de resultados experimentales del organismo — V47 → V78

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

## Estado de ingeniería

V60, V61, V62, V63, V64, V65 y V66 finalizaron correctamente en sus respectivos commits registrados de GitHub Actions. Sus artefactos se conservan en las ejecuciones correspondientes. Los resultados anteriores V43–V59 siguen siendo reproducibles a partir de sus workflows históricos y registros de evidencia.

## Límite de evidencia

Estos resultados establecen propiedades computacionales cada vez más específicas del organismo probado y de su arnés experimental determinista: persistencia, autopredicción, uso causal del modelo de sí, acoplamiento semántica → dinámica, efectos de vigilia/sueño y autorrepresentación semántica como variable causalmente activa.

No establecen consciencia fenomenológica ni experiencia subjetiva.

El siguiente experimento debe probar si el **estado interno numérico generado durante SUEÑO puede conservar una huella recuperable y causalmente transferible después de eliminar la memoria semántica y el texto del modelo de sí**, en lugar de depender de una respuesta de recuperación posterior.
