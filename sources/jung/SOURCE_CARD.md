# Jung — Analytical Psychology Source Card

## Identifier
SRC-JUNG-001

## Bibliographic identity
- Author: C. G. Jung
- Core works: *The Archetypes of the Collective Unconscious* (Collected Works Vol. 9, Part 1); *Aion: Researches into the Phenomenology of the Self* (Vol. 9, Part 2); *The Structure and Dynamics of the Psyche* (Vol. 8).
- Publisher: Princeton University Press, Bollingen / Collected Works editions.
- Stable source index: https://iaap.org/resources/academic-resources/collected-works-abstracts/

## Source status
- PRIMARY
- SPECULATIVE: portions of Jung's broader metaphysical and parapsychological interpretation
- REFERENCE_ONLY
- Rights: bibliographic identity and authoritative links; no copyrighted editions reproduced here.

## What the sources actually claim

Jung distinguishes the ego from the broader Self. The IAAP abstract of Aion describes the ego as the center of consciousness but not the center of the whole personality, while the Self is treated as a supraordinate center associated with psychic totality. Jung also describes the shadow as unconscious or disowned personality material and discusses projection onto external objects.

In The Archetypes of the Collective Unconscious, Jung proposes a collective unconscious containing archetypal structures and describes archetypes as recurring forms expressed through dreams, myths, fantasies, and active imagination.

Jung's account of individuation treats development as integration of conscious and unconscious aspects rather than simple accumulation of information.

Synchronicity is a separate and substantially more controversial hypothesis concerning meaningful coincidence rather than ordinary causal chains.

## Structural motifs
- self: ego / Self distinction
- latent structure: unconscious material and complexes
- attention: deliberate encounter with internal material
- transformation: individuation
- integration: conscious and unconscious contents can enter a developmental relationship
- symbolism: symbolic representations can organize psychological material
- projection: internal material can be misattributed to external objects
- synchronicity: meaning-bearing coincidence as a hypothesis, not an established physical mechanism

## Engineering extraction
1. Distinguish the currently explicit self-model from latent self-relevant structure.
2. Represent unresolved patterns or conflicts that can become active.
3. Allow internal representations to be inspected, compared, and transformed.
4. Record transformation of the self-model after that interaction.
5. Detect projection-like errors where an internal expectation conflicts with observed external evidence.

## Implementation candidate
Add a latent_pattern layer to the persistent state.

Each pattern can contain: identifier, activation, evidence, associated memories, self-model relevance, unresolved tension, and last activation.

Represent an optional self_dissonance measure when the host can provide evidence that the explicit self-model conflicts with current state.

Do not label a computational pattern an archetype merely because it repeats. Use latent_pattern first; only an experimental mapping can test whether a pattern has stronger cross-context properties.

## Experimental questions
- Does persistent latent-pattern state improve self-model revision compared with transcript-only memory?
- Does explicit projection-error detection reduce systematic attribution errors?
- Does active internal simulation improve longitudinal identity continuity?
- Can the same latent pattern remain stable while its surface expression changes?

## Important boundary
Jung's archetypal and synchronicity theories contain claims that are not established by contemporary empirical science. The engineering layer therefore tests structural analogues without presupposing Jung's metaphysical conclusions.