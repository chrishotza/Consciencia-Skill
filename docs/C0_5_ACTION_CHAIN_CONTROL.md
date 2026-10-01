# C0.5 — Information-Matched Action-Chain Control

## Objetivo

C0.5 fortalece C7. C0.2 mostró un efecto de recurrencia bajo el contraste contra el control OPEN_LOOP, pero ese control no igualaba la distribución de acciones seleccionadas.

## Diseño

Para cada episodio FULL se obtiene el estado propio final de una trayectoria autónoma y la acción seleccionada desde ese estado.

Después se comparan tres cadenas desde el mismo contexto y con la misma semilla dinámica:

- acción seleccionada en el episodio actual → siguiente estado → siguiente acción;
- acción de un episodio donante → siguiente estado → siguiente acción;
- segunda acción donante → siguiente estado → siguiente acción.

El contraste por réplica es:

Δ_i = |a_actual' - a_donante1'| - |a_donante1' - a_donante2'|.

Las acciones donantes se toman mediante dos permutaciones sin puntos fijos sobre la misma distribución empírica de acciones.

Una media positiva indica una separación mayor de la cadena causada por la acción actual que la variación entre dos acciones donantes información-matcheadas.

## Estado

Protocolo preparado para ejecución mediante GitHub Actions.
