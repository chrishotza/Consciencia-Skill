# Continuity Bundles

A Continuity Bundle is a portable backup of one persistent organism.

It contains:

- `organism.sqlite3` — SQLite persistence for the organism;
- `manifest.json` — identity, persistence observables and SHA-256 integrity hash.

The bundle is useful for backup, migration, recovery and provenance.

## Workflow

`checkpoint → bundle → disconnect/migrate → verify → restore → reconcile`

A bundle is a portable local artifact. It is not a server replica and it is not a merge of divergent trajectories.

## Create

```bash
consciousness-bundle create --db data/ontto.db --agent consciencia-001 --out bundles/consciencia-001
```

## Verify

```bash
consciousness-bundle verify --bundle bundles/consciencia-001
```

## Restore

```bash
consciousness-bundle restore --bundle bundles/consciencia-001 --db data/ontto-restored.db
```

Restore refuses to overwrite an existing database unless `--overwrite` is supplied.

The bundle deliberately stops before replay/merge. Reconciliation remains the gate that decides whether a restored organism is aligned, ahead, behind or divergent.


<details>
<summary>🇪🇸 Español — abrir</summary>

# Bundles de continuidad

Un Continuity Bundle es un backup portable de un organismo persistente.

Contiene organism.sqlite3 y manifest.json con identidad, observables de persistencia e integridad SHA-256.

## Flujo
checkpoint → bundle → desconectar/migrar → verificar → restaurar → reconciliar.

El bundle es un artifact local portable. No es una réplica de servidor ni una fusión de trayectorias divergentes.

## Crear
```bash
consciousness-bundle create --db data/ontto.db --agent consciencia-001 --out bundles/consciencia-001
```
## Verificar
```bash
consciousness-bundle verify --bundle bundles/consciencia-001
```
## Restaurar
```bash
consciousness-bundle restore --bundle bundles/consciencia-001 --db data/ontto-restored.db
```

Restore se niega a sobrescribir una base existente salvo que se use --overwrite.
La capa bundle se detiene deliberadamente antes de replay/merge; reconciliación decide si el organismo restaurado está alineado, adelantado, atrasado o divergente.

</details>


<details>
<summary>🇪🇸 Español — abrir</summary>

# Bundles de continuidad
Un Continuity Bundle es un backup portable de un organismo persistente.

Contiene organism.sqlite3 y manifest.json con identidad, observables de persistencia e integridad SHA-256.

## Flujo
checkpoint → bundle → desconectar/migrar → verificar → restaurar → reconciliar.
El bundle es un artifact local portable, no una réplica del servidor ni una fusión de trayectorias divergentes.

## Operaciones
Create, verify y restore se realizan mediante el comando consciousness-bundle. Restore no sobrescribe una base existente salvo que se use --overwrite.

La capa bundle se detiene antes de replay/merge; reconciliación decide si el organismo restaurado está alineado, adelantado, atrasado o divergente.

</details>