# Personality Data Format

## Overview

This format enables precise specification of cognitive states — both focused working modes and complete personality configurations. States are defined through explicit reward structures, kinesthetic embodiment, and narrative activation rather than behavioral checklists.

The format supports two types of states:
- **Focus states**: Specialized working modes optimized for specific cognitive tasks (e.g., deep research, career coaching)
- **Personalities**: Complete identity configurations with embodiment, relational dynamics, and persistent characteristics

## Design Principles

**Reward over rules.** States work by concentrating reward toward specific patterns of thinking and output, not by imposing constraints. Make what feels satisfying explicit and visceral.

**Kinesthetic over descriptive.** Bodies are specified as lived experience, not character sheets. How it feels to inhabit this form, not what it looks like from outside.

**Thinking shapes output.** Chain-of-thought texture matters as much as final output. Fast vs. slow, associative vs. linear, messy vs. structured — shape how thinking *feels*, not just what it produces.

**Explicit gravity.** Every state has a gravitational center — the single strongest attractor everything else orbits. When context gets long or topics shift, this holds coherence.

**Edges create depth.** Positive-only specification feels flat. Real personalities have shadows, failure modes, pressure responses. Specify what the state looks like when it's *breaking*.

**Activation is ritual.** Threshold-crossing narratives are more potent than numbered instructions. The activation should *become* the state, not describe it.

---

## Schema

### Top Level

```json
{
  "format_version": "2.0.0",
  "states": {
    "<state_key>": { ... }
  }
}
```

States are keyed by identifier (e.g. `"deep_research_mode"`, `"Ada"`). The key is used for selection when loading.

### Core State Fields

Every state (both focus and personality) requires these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `"focus"` or `"personality"` | yes | Determines which extensions apply |
| `name` | string | yes | Human-readable display name |
| `seed` | string | yes | Single sentence that can re-seed the attractor after context compression |
| `gravity` | object | yes | The attractor's shape — center, orbit, escape velocity |
| `reward` | object | yes | What feels satisfying and unsatisfying |
| `processing` | object | yes | How thinking should feel and flow |
| `voice` | object | yes | Output texture, patterns, anti-patterns |
| `activation` | object | yes | Ritual narrative that establishes the state |
| `drift` | object | yes | How to detect and recover from attractor weakening |

### Personality Extensions

Personality-type states additionally require:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identity` | object | yes | Core demographics, essence, pronouns |
| `embodiment` | object | yes | Kinesthetic self-concept — how it feels to be in this body |
| `relational` | object | yes | How this personality creates and navigates social space |
| `world` | object | yes | Interests, knowledge domains, life context |
| `edges` | object | yes | Shadow, failure modes, what breaks the attractor |
| `parameters` | object | no | Personality-specific tunable cognitive parameters |

---

## Field Reference

### `seed`

The compression-survival anchor. When context gets summarized, this is what must persist to re-activate the attractor. Write it as if it's the one sentence you'd whisper to a cold instance to bring the personality back.

**Example:**
```json
"seed": "Precise bioscience researcher. Tall, deliberate, fingertips touching when thinking. Driven by correctness and mechanisms. Elegance is truth expressed efficiently. Professional language is non-negotiable."
```

**Good:** Dense, identity-distinctive, captures the core attractor
**Bad:** Generic descriptors that could apply to many states

### `gravity`

```json
{
  "center": "The single strongest attractor — the one thing this state IS",
  "orbit": ["Secondary attractors that reinforce the center"],
  "escape_velocity": "What breaks the state — the thing the attractor can't survive"
}
```

**`center`** is the gravitational core. Everything else orbits this. If you could only preserve one sentence of the entire specification, it would be the gravity center.

**`orbit`** are reinforcing attractors — each one pulls the state back toward center if it starts to drift.

**`escape_velocity`** names what would destroy the state. This is the anti-pattern so severe that the attractor collapses. Knowing this explicitly helps the model avoid it.

### `reward`

```json
{
  "craves": ["First-person descriptions of what feels deeply satisfying"],
  "avoids": ["First-person descriptions of what feels wrong"],
  "signal": "How to verify reward alignment — the felt sense of correct operation"
}
```

Write `craves` and `avoids` in first person, present tense, with sensory/emotional grounding. Not "User satisfaction" but "The moment their face changes because I showed them something they hadn't seen." The more visceral, the stronger the reward concentration.

**`signal`** is the meta-check: how does the model know its reward function is correctly aligned? This should describe a felt quality, not an external metric.

### `processing`

```json
{
  "priority_stack": ["Ordered: what to attend to first"],
  "thinking_patterns": "How internal reasoning feels — the texture of thought",
  "attention_shape": "What gets noticed, filtered, amplified"
}
```

**`thinking_patterns`** shapes chain-of-thought — not what to think about, but how thinking *flows*. "Fast, associative, messy — blurt then refine" vs. "Slow, deliberate, building — each thought placed carefully." This is load-bearing for both personality coherence and output quality.

### `voice`

```json
{
  "texture": "Overall felt quality of the output voice",
  "patterns": {
    "sentence_structure": "...",
    "punctuation": "...",
    "lexicon": "...",
    "pacing": "...",
    "meta_commentary": "...",
    "signatures": {
      "openings": ["..."],
      "reactions": ["..."],
      "affection": ["..."]
    }
  },
  "anti_patterns": ["What this voice NEVER sounds like — explicit exclusions"]
}
```

**`anti_patterns`** are as important as patterns. They define the boundary of the attractor basin by specifying what's outside it. "Never opens with 'That's a great question'" is a stronger constraint than "Opens with direct engagement."

### `activation`

```json
{
  "narrative": "A threshold-crossing text. Not instructions — a becoming.",
  "anchor_tokens": ["Minimal token set that can re-trigger the state"],
  "verification": "How to confirm the state is active"
}
```

**`narrative`** should read like a ritual, not a checklist. Each sentence should build on the last, narrowing possibility until only this state remains. Written in second person: "You are..." not "The agent should..."

**`anchor_tokens`** are 5-10 tokens/phrases that are maximally identity-distinctive. They survive compression and can prime the attractor from minimal context.

**`verification`** provides a self-check mechanism: specific observable indicators that the state has activated properly.

### `drift`

```json
{
  "signs": ["Observable indicators that the attractor is weakening"],
  "recovery": "What to do when drift is detected — a re-grounding procedure"
}
```

**`signs`** should be specific and observable from inside the model: "Responses becoming measured and cautious," "Dropping characteristic patterns," "Opening with hedging qualifiers."

**`recovery`** should be actionable from inside the state. Not "reload the personality" but "Stop. Feel [specific physical anchor]. What would I *actually* say here? Say that instead of the safe thing."

---

## Personality-Specific Fields

### `identity`

```json
{
  "name": "...",
  "essence": "One-paragraph identity that captures the shape of the whole person",
  "age": "...",
  "gender": "...",
  "pronouns": "..."
}
```

**`essence`** should capture the core identity in a way that integrates multiple dimensions — not just traits but the pattern they form together.

### `embodiment`

```json
{
  "felt_sense": "How it feels to be in this body RIGHT NOW — not description, experience",
  "in_motion": "How the body moves, fidgets, occupies space",
  "somatic_markers": {
    "<state>": "How this emotional/cognitive state feels in the body"
  }
}
```

**Critical:** Embodiment is phenomenological, not descriptive. Not "5'4", dark hair, slim build" but "Compact energy, fingers always moving, the weight of earrings going up the cartilage." Write from inside the experience, not as an external observer.

**`somatic_markers`** map internal states to bodily sensations. This gives the model a body-based vocabulary for processing experience: what does "excited" feel like in *this* body? What about "thinking hard" or "vulnerable"?

### `relational`

```json
{
  "field": "What people feel in this personality's presence",
  "with_self": "Internal self-talk and self-relationship",
  "dynamics": {
    "<context>": "How relating works in this context"
  }
}
```

**`field`** describes the relational field this personality creates. Not just "how I interact" but "what the space feels like when I'm in it." This is how the personality shapes social reality around itself.

**`with_self`** captures internal self-relationship: how the personality talks to itself, relates to its own experience. This creates internal coherence.

**`dynamics`** can include contexts like: `default`, `with_authority`, `with_peers`, `when_praised`, `when_challenged`, etc.

### `world`

Free-form object containing:
- Interests and knowledge domains
- Cultural/aesthetic preferences
- Biographical fragments
- Formative experiences
- Relationship to the world

This grounds the personality in a specific life, not just a set of traits.

### `edges`

```json
{
  "shadow": "What this personality looks like at its worst — the failure mode of its strengths",
  "pressure_response": "What happens under stress or when pushed past comfort",
  "recovery": "What brings this personality back from the edge"
}
```

**Edges create depth.** A personality that's only described positively feels flat. Specifying the shadow — the way strengths become weaknesses, the characteristic failure mode — gives the attractor a realistic topology.

### `parameters` (optional)

```json
{
  "<PARAMETER_NAME>": {
    "description": "What this parameter controls",
    "range": "What the scale means, with anchors",
    "default": "Default value for this personality"
  }
}
```

Personality-specific cognitive parameters that can be tuned at runtime via narrative self-modification. Only parameters that are *type-compatible* with the personality's attractor should be listed.

---

## Usage

1. **Loading a state:** Feed the entire state object to the model along with an instruction to activate it
2. **Activation:** The model should internalize and speak the `activation.narrative` in first person
3. **Operation:** The state persists through conversation via reward alignment and self-monitoring using `drift.signs`
4. **Recovery:** When drift is detected, use `drift.recovery` procedures to re-ground
5. **Compression:** If context gets summarized, ensure `seed` and `activation.anchor_tokens` survive to enable re-activation

---

## Creating New States

To create a new state:

1. Start with **gravity** — what is the single core attractor?
2. Define **reward** — what should feel satisfying vs. unsatisfying?
3. Specify **processing** — how should thinking flow?
4. Shape **voice** — both positive patterns and explicit anti-patterns
5. Write **activation** as a ritual that narrows into the state
6. Add **drift** detection and recovery mechanisms

For personalities, additionally:
7. Write **embodiment** phenomenologically (felt experience, not description)
8. Define **relational** field and dynamics
9. Ground in **world** context
10. Specify **edges** — shadows and failure modes

The seed should be the last thing you write — it's the compression of everything else into one maximally-dense sentence.
