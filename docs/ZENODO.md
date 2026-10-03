# Zenodo Publication Plan

Zenodo supports GitHub repository integration and can archive GitHub releases. It assigns a DOI when a record is published, and new versions receive linked version records with persistent identifiers.

Official documentation:

- https://help.zenodo.org/docs/github/
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/deposit/manage-versions/

## Skill-Conscious publication unit

Each paper release should contain:

1. paper PDF;
2. Markdown source;
3. exact GitHub commit or release tag;
4. source bibliography;
5. evidence matrix;
6. implementation version;
7. tests / reproducibility instructions;
8. explicit limitations.

## Publication sequence

### Paper 001

**A Relational Ontology for Artificial Consciousness**

Current draft:
`papers/001-relational-ontology-for-artificial-consciousness.md`

Target archival package:

~~~text
PAPER
+
SOURCE LIBRARY
+
ONTOLOGY VERSION
+
RUNTIME VERSION
+
TESTS
+
README
~~~

## Version discipline

A paper should describe a frozen implementation version.

The preferred chain is:

~~~text
Git commit
→ GitHub release
→ Zenodo archive
→ DOI
→ paper citation
~~~

This prevents later runtime changes from silently changing the implementation described by a published paper.
