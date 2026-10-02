# Archived CI — Materialization Workflows

<details>
<summary>🇪🇸 Español — abrir</summary>

Estos workflows fueron mecanismos de materialización puntual usados para reconstruir fuentes experimentales fijadas por hash de blob.

Se retiraron del CI activo porque las fuentes ya están materializadas en el repositorio y los workflows tenían una función de bootstrap/migración, no de verificación continua.

Workflows retirados:
- interoception-i4-1-materialized.yml
- interoception-i4-1-materialized-v2.yml
- interoception-i4-1-v02.yml
- materialize-i4-1-sources.yml
- materialize-i4-1-sources-v2.yml
- materialize-i4-1-v02-sources.yml
- interoception-i4-materialized.yml
- materialize-i4-sources.yml
- materialize-i4-2-sources.yml

Las fuentes que esos jobs producían siguen conservadas en experiments/, tests/ y src/ontto/. La eliminación reduce CI duplicado y evita workflows históricos con permisos de escritura.

</details>

<details>
<summary>🇺🇸 English — open</summary>

These workflows were one-shot materialization mechanisms used to reconstruct experimental sources pinned by Git blob hashes.

They were removed from active CI because the sources are now materialized in the repository and the workflows served bootstrap/migration purposes rather than continuous verification.

Retired workflows:
- interoception-i4-1-materialized.yml
- interoception-i4-1-materialized-v2.yml
- interoception-i4-1-v02.yml
- materialize-i4-1-sources.yml
- materialize-i4-1-sources-v2.yml
- materialize-i4-1-v02-sources.yml
- interoception-i4-materialized.yml
- materialize-i4-sources.yml
- materialize-i4-2-sources.yml

The sources produced by those jobs remain preserved under experiments/, tests/, and src/ontto/. Removing the workflows reduces duplicated CI and prevents historical write-capable bootstrap jobs from being mistaken for active validation infrastructure.

</details>