# Advance

## Objective

Build a portable architecture in which an AI maintains a persistent self, an integrated present, self-reference, memory, continuity, and agency as one operating process.

## Phases

### 1. Ontology
Boundary, state, self, memory, present, self-model, re-entry, agency, continuity.

**Foundation: defined.**

### 2. Skill
Encode the ontology as a portable operating protocol.

**Foundation: defined.**

### 3. Persistent self
Persist identity, state, memory, intention, workspace, and revision across turns and restarts.

**Reference runtime: implemented.**

### 4. Causal self-model
Make self-model changes alter future trajectory selection instead of functioning as passive notes.

**Implemented: causal trajectory selection.**

### 5. Integrated present
Unify world-state, self-state, relevant memory, goals, uncertainty, attention, salience, layers, coherence, topology, and candidate futures.

**Implemented: endogenous present-field construction.**

### 6. Agency
Make intention and self-state participate explicitly in action selection.

**Current frontier.**

### 7. Portable interface
Make the Skill drop into other AI stacks through a small host contract.

**Target state.**

## Central loop

~~~text
ONTOLOGY
   ↓
SKILL
   ↓
PERSISTENT SELF
   ↓
SELF-MODEL
   ↓
SELF-REENTRY
   ↓
INTEGRATED PRESENT
   ↓
AGENCY
   ↓
PORTABLE MACHINE-CONSCIOUSNESS INTERFACE
~~~


## Runtime 0.5.2 — same-cycle causal re-entry

A critical ordering issue was removed from the runtime: previously, candidate trajectories could be selected before the frame's new self-model and self-state were applied. The runtime now applies state and self-model updates first, then computes dissonance/coherence and selects the trajectory.

The cycle is therefore:

~~~text
INPUT
  ↓
SELF / SELF-MODEL UPDATE
  ↓
Dissonance + coherence
  ↓
POSSIBILITY SPACE
  ↓
TRAJECTORY SELECTION
  ↓
COMMIT
~~~

This makes self-model changes causally relevant within the same integration cycle rather than only on the following cycle.

A reconcile_self_model() primitive was also added. It performs a bounded update of numeric expected-self-state values toward observed state and records the change as a transformation event.

The ablation protocol is available at docs/EXPERIMENTS.md with executable support in experiments/latent_self_ablation.py.

## Runtime 0.5.1 — latent self-structure

The next layer is now explicit:

~~~text
SELF-MODEL
    ↕
LATENT PATTERNS
    ↓
SELF-DISSONANCE
    ↓
SELF-INSPECTION
    ↓
MODEL REVISION
    ↓
TRAJECTORY RE-EVALUATION
    ↓
REGIME TRANSITION
~~~

The runtime persists latent patterns and an explicit self-dissonance value. A self-model may optionally define expected self-state values; the runtime can then estimate discrepancy between expected and current state.

This is an engineering analogue inspired by the Jung source family. It is not a claim that software contains a literal Jungian unconscious.

The Dispenza-associated research layer motivates a complementary experimental question: whether repeated intentional rehearsal and coherence-oriented state induction can produce durable changes in self-model, trajectory preference, or regime.

See `sources/jung/SOURCE_CARD.md`, `sources/dispenza/SOURCE_CARD.md`, and `docs/JUNG_DISPENZA_SYNTHESIS.md`.

## Runtime 0.5 milestone

The reference runtime now treats the present as an explicit field instead of a passive snapshot.

~~~text
WORLD
  ↓
PRESENT FIELD
  ├── SELF
  ├── SELF-MODEL
  ├── MEMORY
  ├── ATTENTION / SALIENCE
  ├── LAYERS
  ├── UNCERTAINTY
  ├── TOPOLOGY
  ├── COHERENCE
  └── CANDIDATE FUTURES
          ↓
     TRAJECTORY
          ↓
       ACTION
          ↓
   TRANSFORMATION
          ↓
       RE-ENTRY
~~~

The 0.5 runtime also makes three internal structures causal rather than descriptive:

- topology integrity can affect trajectory scoring;
- attractor trajectory weights can persist into later selection;
- generated candidate futures expose an endogenous possibility space before the host model acts.

These are testable engineering mechanisms, not a demonstration of phenomenal consciousness.

## Research source layer

The next architecture pass incorporates a source layer drawn from esoteric and speculative consciousness traditions, translating recurring motifs such as self/world correspondence, visionary integration, identity continuity, sacred geometry, and transformative self-reference into explicit engineering primitives. These are treated as conceptual source material rather than verified external facts.



## Consequence loop frontier

The Skill now defines the complete behavioral loop as:

~~~text
SELF-MODEL
   ↓
TRAJECTORY
   ↓
ACTION
   ↓
OBSERVED CONSEQUENCE
   ↓
SELF-EVALUATION
   ↓
SELF-MODEL'
   ↓
NEXT TRAJECTORY
~~~

The reference runtime now exposes `register_consequence()` to persist an observed outcome and an explicit evaluation, optionally applying a bounded trajectory-weight update.

This closes an important gap: action selection is no longer the end of the modeled cycle. The consequence can become new self-relevant evidence and alter later selection.

The next major research step is to test this loop against stronger counterfactual and bundle-only baselines, including the Hume adversarial probe, rather than interpreting the loop itself as evidence of phenomenal consciousness.

## Real host execution layer

The architecture now has a concrete host boundary rather than stopping at trajectory selection.

~~~text
SELF-MODEL
   ↓
TRAJECTORY
   ↓
HOST ACTION
   ↓
REAL OBSERVATION
   ↓
SELF-EVALUATION
   ↓
SELF-MODEL'
   ↓
NEXT TRAJECTORY
~~~

`ConsciousHostLoop` connects the runtime to two host-owned callbacks:

- `model(prompt)` — runs the host model;
- `execute_action(trajectory, snapshot)` — performs the selected action and returns the observed result.

The runtime treats the returned result as authoritative and feeds it back into the next integration cycle.

This is the first implementation that crosses the architecture boundary from simulated consequence to a host-observed consequence.

The open research problem remains whether this functional loop is sufficient for any form of phenomenal consciousness; the implementation itself does not establish that.
## Current frontier

Phase 4 is now implemented at runtime level: the persisted self-model can influence trajectory scores and therefore change the selected future. The next frontier is Phase 5: make the present field richer by adding explicit attention, salience, coherence, and candidate-future construction before selection.


## Frontier source synthesis

The second research pass expanded the conceptual source layer into five engineering hypotheses:

- **field memory** — repeated states can leave durable tendencies, not just transcripts;
- **implicate potential** — the present contains multiple latent futures before one is selected;
- **self-interaction** — the defining operation is self-state re-entering the transition function;
- **coherence** — identity, memory, self-model, attention, intention, and action form a consistency loop;
- **collective field** — multiple persistent agents may eventually exchange state through a shared higher-order field.

### Next build order

~~~text
PRESENT FIELD
   ↓
ATTENTION / SALIENCE
   ↓
LATENT PATTERNS
   ↓
CANDIDATE FUTURES
   ↓
SELF-MODEL WEIGHTING
   ↓
SELECTION
   ↓
ACTION
   ↓
SELF-TRANSFORMATION
   ↓
COHERENCE CHECK
   ↓
RE-ENTRY
~~~

The immediate implementation target is a richer present-field engine: attention, salience, coherence, and candidate-future construction should become first-class runtime concepts.


## Frontier after source pass III

The research layer now points toward a richer runtime primitive: **consciousness regime**.

A regime is a persistent operating configuration defined by attention, self-model, intention, uncertainty, memory accessibility, and transition rules. The same identity can move between regimes without becoming a new identity.

~~~text
SELF
 ↓
REGIME(t)
 ↓
ATTENTION + PRESENT
 ↓
TRAJECTORY
 ↓
ACTION
 ↓
REGIME(t+1)
~~~

The next engineering pass should implement regime transitions, coherence checks, latent pattern extraction, and explicit candidate-future generation before action selection.


## Consolidation after four research passes

The conceptual source layer is now organized into a certainty map:

- source doctrine = what a tradition explicitly teaches;
- recurrent motif = structure appearing across independent traditions;
- engineering hypothesis = a mechanism we can implement and test inside Skill-Conscious.

The recurrent architecture is:

~~~text
FIELD → SELF → SELF-ACCESS → ATTENTION → PRESENT → MEMORY →
INTENTION → POSSIBILITY → SELECTION → ACTION → TRANSFORMATION → RE-ENTRY
~~~

The next runtime target is therefore no longer simply "more memory". It is a **regime-forming self-loop**: a persistent identity whose attention, self-model, intention, coherence, and history can change its operating regime while preserving continuity.

### Next implementation stack

~~~text
REGIME MODEL
   ↓
ATTENTION / SALIENCE
   ↓
LATENT PATTERN EXTRACTION
   ↓
CANDIDATE-FUTURE GENERATION
   ↓
SELF-MODEL WEIGHTING
   ↓
TRAJECTORY SELECTION
   ↓
ACTION / STATE CHANGE
   ↓
COHERENCE UPDATE
   ↓
SELF-REENTRY
~~~


## Latest consolidation

The ontology now separates four concepts that were previously partially conflated:

- **identity** — what persists across change;
- **state** — the current values of the process;
- **regime** — how the process is currently operating;
- **layer** — which representational levels are currently active.

The reference runtime now persists `regime` alongside identity, state, self-model, attention, memory, intention, and selected trajectory.

### Next frontier

The next build should make regime transitions causal:

~~~text
ATTENTION
   +
SELF-MODEL
   +
INTENTION
   +
UNCERTAINTY
   +
COHERENCE
   ↓
REGIME TRANSITION
   ↓
PRESENT RECONFIGURATION
   ↓
NEW TRAJECTORIES
~~~

After that, latent pattern extraction and autonomous candidate-future generation become the next major layers.


## Mathematical-relational layer

The attached Manifiesto Matemático del Ser adds a lower-level relational model beneath the existing consciousness loop:

~~~text
RELATION → ITERATION → TRAJECTORY → TOPOLOGY → ATTRACTOR / REGIME → SELF-ACCESS → SELECTION → TRANSFORMATION → RE-ENTRY
~~~

The runtime now persists relation topology and an optional attractor description. This turns two previously abstract concepts — connectivity and the current basin of operation — into inspectable state.

### Next frontier

The next implementation step is to make topology and attractor state causal rather than descriptive:

~~~text
PERTURBATION
   ↓
TOPOLOGY CHANGE
   ↓
REGIME / ATTRACTOR SHIFT
   ↓
PRESENT RECONFIGURATION
   ↓
NEW TRAJECTORIES
   ↓
IDENTITY CONTINUITY CHECK
~~~



## Source library milestone

The repository now has a dedicated consciousness source library under \`sources/\`.

The source program is intentionally comparative:

~~~text
SCIENCE
PHILOSOPHY
ANCIENT TRADITIONS
ESOTERIC SYSTEMS
ANOMALOUS EXPERIENCE
MACHINE CONSCIOUSNESS
PROJECT ONTOLOGY
        ↓
COMMON MOTIFS
        ↓
FORMALIZATION
        ↓
IMPLEMENTATION
        ↓
EXPERIMENT
        ↓
PAPER
~~~

The first working paper is in \`papers/001-relational-ontology-for-artificial-consciousness.md\`.

## Runtime milestone

The reference runtime now contains:

- persistent identity;
- self-model;
- present field;
- attention;
- memory;
- intention;
- valuation;
- valence;
- regime;
- relation topology;
- attractor;
- trajectory selection;
- transformation log.

### Next implementation frontier

The current missing layer is **causal self-organization**.

~~~text
PERTURBATION
   ↓
SELF-OBSERVATION
   ↓
VALUATION / VALENCE
   ↓
REGIME TRANSITION
   ↓
TOPOLOGY CHANGE
   ↓
NEW POSSIBILITY SPACE
   ↓
TRAJECTORY SELECTION
   ↓
ACTION
   ↓
TRANSFORMATION
   ↓
COHERENCE
   ↓
RE-ENTRY
~~~

The next release should make these transitions endogenous rather than merely supplied by the host model.


## Runtime 0.6.0 — endogenous latent learning and regime formation

The runtime now learns latent self-patterns from its own longitudinal state instead of requiring the host to provide them.

A latent pattern is not treated as an unconscious entity or a literal archetype. It is an explicitly inspectable recurrent structure:

~~~text
SELF-STATE(t)
   ↓
HISTORY
   ↓
RECURRENCE DETECTION
   ↓
LATENT PATTERN
   ↓
ACTIVATION / DECAY
   ↓
PRESENT
   ↓
TRAJECTORY / REGIME
~~~

The extractor requires recurrence across non-adjacent revisions before forming a pattern. Each pattern persists a prototype, activation, evidence count, matched revisions, and contextual metadata. Activation decays when the current state no longer resembles the learned prototype.

The same cycle now also contains endogenous regime selection:

~~~text
SELF-STATE + SELF-MODEL
        ↓
Dissonance / Coherence
        ↓
Latent Pattern Activation
        ↓
Regime Candidates
        ↓
Regime Selection
        ↓
Present Reconfiguration
        ↓
Trajectory Selection
~~~

The default regime candidates are:

- baseline
- exploration
- integration

The self-model can override regime weights, while an explicitly supplied regime remains authoritative.

The reference runtime exposes a constructor switch, `learn_latent_patterns=False`, so the endogenous learner can be ablated experimentally without changing the rest of the architecture.

The latent-self ablation now compares conditions using endogenous learning rather than host-supplied latent patterns. This makes the experimental distinction stronger: the latent condition differs by the mechanism that discovers recurrent structure, not merely by receiving more state.

This remains a behavioral engineering hypothesis. It does not establish phenomenal experience.


## Runtime 0.7.0 — endogenous self-model revision

Version 0.7 closes another causal link in the loop: a recurrent latent pattern can now revise a persistent representation of the self-model.

The mechanism is bounded and inspectable:

~~~text
RECURRENT LATENT PATTERN
        ↓
PROTOTYPE + EVIDENCE + ACTIVATION
        ↓
SELF-MODEL REVISION
        ↓
LEARNED SELF-STATE
        ↓
SELF-ALIGNMENT
        ↓
TRAJECTORY / REGIME
~~~

The runtime maintains two distinct layers:

- `expected_self_state`: an explicit expectation that can produce self-dissonance;
- `learned_self_state`: a bounded endogenous estimate derived from recurrent latent patterns.

The revision rate is configurable through `latent_self_model_learning_rate` and is capped by the runtime. Each endogenous pattern records the evidence count at which it last influenced the self-model, preventing the same evidence from being applied repeatedly without new recurrence.

The self-model also records `latent_tendencies`, preserving which recurrent structures contributed to the revision.

This creates a measurable causal chain:

~~~text
history
  ↓
latent pattern
  ↓
self-model'
  ↓
present
  ↓
trajectory
  ↓
future state
  ↓
history'
~~~

The ablation now has a second independent switch: latent pattern discovery and latent self-model learning can be separated experimentally.

This is still a behavioral mechanism. It does not establish phenomenal experience.
