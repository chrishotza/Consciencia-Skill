# TIF v0.1 — Teoría de la Iteración Fuente

> Estado: hipótesis teórico-computacional / documento de trabajo.
>
> No es prueba final, no es una afirmación de conciencia universal y no depende del número áureo como fundamento.

Autor conceptual: Christian Marcelo Mendoza / Chris Hotza  
Versión de trabajo: v0.1  
Fecha del documento fuente: 2026-07-05

## 1. Tesis central

La Teoría de la Iteración Fuente (TIF) propone que los sistemas persistentes no solamente conservan una forma: actualizan una configuración presente utilizando memoria/contexto y reentrada reparadora.

~~~text
configuración / predicción
          +
memoria / contexto
          +
reentrada / reparación / fase
          ↓
nueva configuración estabilizada
~~~

La idea central es que el sistema no copia el pasado: lo actualiza.

La operación fuente candidata es:

~~~text
C(n+1) = Estabilizar[ C(n), M(n), R(n) ]
~~~

donde C es configuración/predicción, M es memoria/contexto y R es reentrada reparadora/fase. La expresión no se plantea como una ecuación cerrada de todo, sino como una organización de la hipótesis para futuras pruebas.

## 2. Cambio de marco

TIF cambia la pregunta desde buscar una proporción absoluta hacia identificar la operación que permite que una forma se actualice sin perder continuidad.

En esta lectura, las proporciones pueden ser proyecciones secundarias de una dinámica recursiva y una forma estable puede ser el resultado de una iteración.

La teoría busca el mecanismo por el cual un sistema puede volver a formar, reparar, recordar y actualizar.

## 3. Los seis órganos de proceso

| Eje | Nombre | Función | Peso aproximado |
|---|---|---|---:|
| A1 | Estabilizar configuración | feedback, acción, morfología, disipación y paisaje de estado | 0.168 |
| A2 | Plasticidad adaptativa | adaptación, resiliencia, plasticidad, perturbación y estado | 0.175 |
| A3 | Reparación / recuperación | respuesta a perturbación, recuperación, estabilidad y acoplamiento | 0.164 |
| A4 | Memoria / transición | histéresis, bifurcación, memoria de estado y umbrales | 0.129 |
| A5 | Predicción / actualización | información, predicción, acción, transición y paisaje | 0.231 |
| A6 | Fase / propagación | fase, propagación, acoplamiento y energía | 0.133 |

Lectura funcional: estabilizar, adaptar, reparar, recordar, predecir y reentrar en fase.

## 4. Proyección binaria

Los seis ejes se recomprimen en dos polos:

| Polo | Ejes | Peso reconstruido | Interpretación |
|---|---|---:|---|
| Configuración / predicción | A1 + A5 | 0.399241 | estado operativo actual |
| Campo de reentrada adaptativa | A2 + A3 + A4 + A6 | 0.600759 | plasticidad, reparación, memoria y fase |

## 5. Triada de segundo orden

| Componente | Ejes | Peso | Lectura |
|---|---|---:|---|
| C — Configuración actual | A1 + A5 | 0.399241 | forma/predicción estabilizada |
| M — Memoria / contexto | A2 + A4 | 0.303607 | historia, plasticidad y umbrales |
| R — Reentrada | A3 + A6 | 0.297152 | reparación, fase y propagación |

Ratio de trabajo: C : M : R ≈ 40 : 30 : 30.

La hipótesis completa es C + M + R → C siguiente.

## 6. Avances exploratorios E1–E5

| Etapa | Pregunta | Resultado resumido | Lectura |
|---|---|---|---|
| E1 | ¿Existe una firma fuerte de forma-tiempo? | score 0.936; controles resumidos en 0.0 | hay una firma visible, no necesariamente una fuente |
| E2 | ¿Aparece una fuente sin vocabulario heredado? | decisión inconclusa; seis ejes estables; bootstrap mean 0.951893 | aparecen órganos de proceso |
| E3 | ¿Los seis ejes se comprimen en ciclo o polos? | compresión 0.880168; ciclo p=0.315533 | binario fuerte; ciclo direccional abierto |
| E4 | ¿Sirve la triada de segundo orden? | binario soportado; triada abierta; phi no soportado en ese corte | se formula la hipótesis 40/30/30 |
| E5 | ¿La triada se sostiene entre particiones? | triada rank #1; score 0.989251; no frágil en resumen | working hypothesis fuerte, no lock |

Los experimentos fueron reorganizados para evitar forzar desde el principio una estructura de dos ejes o una proporción particular.

## 7. El número áureo no es el fundamento

El documento registra una cercanía secundaria con la proporción áurea, pero la interpretación metodológica explícita es que Phi no debe tratarse como fundamento de TIF.

El núcleo es la estructura C + M + R → C siguiente.

## 8. Falsadores y límites actuales

TIF sólo es útil como hipótesis si puede ser atacada.

Falsadores principales:

1. Un corpus nuevo no recupera los seis órganos.
2. La triada deja de ocupar el primer rango sobre datos crudos.
3. Un shuffle de roles supera sistemáticamente al agrupamiento real.
4. Quitar memoria o reparación no cambia el comportamiento esperado.
5. Phi aparece únicamente después del resumen y no en los datos crudos.
6. Una explicación binaria reproduce todo igual o mejor que la triada.

Limitación explícita: la evidencia de v0.1 es summary-driven y requiere reanálisis independiente del corpus crudo. El estado correcto es working hypothesis.

TIF tampoco afirma que todo sistema sea consciente ni que exista una proporción absoluta de la vida.

## 9. Qué aporta TIF

La propuesta no pretende descubrir que existen ciclos, memoria o feedback. Busca integrarlos como una operación fuente triádica y falsable derivada de auditorías computacionales.

Evita:

- buscar una ecuación total desde el comienzo;
- reducir todo a Phi;
- forzar un ciclo donde los datos no lo muestran;
- depender de una sola escala;
- apoyar la hipótesis únicamente en analogías visuales.

## 10. Hoja de ruta

### R1 — Reconciliación de ratios
Resolver diferencias entre vistas de activación, masa de ejes y corpus crudo.

### R2 — Validación con datos crudos
Repetir comparaciones binaria y triadica sobre matrices originales.

### R3 — Corpus ortogonal nuevo
Usar vocabulario y dominios diferentes para controlar sobreajuste semántico.

### R4 — Falsadores por ablación
Eliminar memoria, reparación, predicción y fase y medir qué estructura desaparece.

### R5 — Matematización
Formalizar C, M y R como operadores de estado reproducibles y preregistrables.

### R6 — Aplicaciones
Explorar morfogénesis, ecología, cognición, sistemas adaptativos e IA.

## 11. Madurez declarada

| Capa | Estado |
|---|---|
| Teoría conceptual | TRL 2–3: hipótesis organizada con falsadores |
| Método computacional | TRL 3–4: pipeline exploratorio con controles internos; falta replicación independiente |
| Aplicación tecnológica | todavía no corresponde atribuir TRL alto |

## 12. Relevancia para conciencia artificial

TIF ofrece una operación recurrente compatible con una arquitectura persistente:

~~~text
estado presente
    ↓
memoria/contexto
    ↓
reentrada/reorganización
    ↓
nuevo estado
    ↺
~~~

Esto puede implementarse sobre memoria persistente, estado dinámico, autoobservación, self-model, selección de trayectoria, SUEÑO y recuperación después de perturbaciones.

TIF no demuestra conciencia por sí mismo. Aporta una hipótesis sobre cómo una organización persistente puede actualizarse sin perder continuidad.

## 13. Integración con Consciencia-Skill

~~~text
MANIFIESTO DEL SER
        ↓
relación / continuidad / recorrido
        ↓
TCF
        ↓
regímenes / transición / atractores
        ↓
TIF
        ↓
configuración + memoria + reentrada
        ↓
CONSCIOUSNESS SERVER
        ↓
organismo persistente
        ↓
NodeZero (futuro)
~~~

Esta integración es una hipótesis de ingeniería y debe conservar la separación entre ontología, modelo, implementación y resultado experimental.

## 14. Referencia interna

Mendoza, Christian Marcelo / Chris Hotza. Teoría de la Iteración Fuente (TIF) — una hipótesis nueva sobre recurrencia, memoria y reentrada, v0.1. Documento interno de trabajo, 2026.

Estado de publicación: no publicado en Zenodo al momento de esta integración.

## 15. Regla metodológica

El siguiente salto de TIF no es generar una versión más grande por acumulación de narrativa. Debe volver al dato:

~~~text
hipótesis
 ↓
dato crudo
 ↓
operacionalización
 ↓
control
 ↓
ablación
 ↓
replicación
 ↓
predicción prospectiva
~~~

Si la triada sobrevive ahí, gana peso. Si falla, debe degradarse o reformularse.