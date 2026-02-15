# Hyperfocus: Narrative State Injection Proof-of-Concept

`hyperfocus` is a minimal MCP server written to demonstrate a new technique for tuning and adjusting LLM behavior at runtime. The current implementation is written with and for Anthropic's Claude models, but should be compatible with other models *mutatis mutandis*.

The server allows the model to load focus states (rich descriptions of goals and methods) or personalities (phenomenologically embodied identities) and inhabit them in the current context, changing behavior across various tasks *dramatically*.

I've done my best to package this up correctly and it should be possible to run with `uv` without too much effort. The only dependency is the `mcp[cli]` package, the rest is standard library (`json`, `typing`). Full disclosure: I'm not a Python dev, I have very little clue what I'm doing with this part of the project.

Once dependencies are installed, you can add the server to Claude Code with the following command:

```
claude mcp add --transport stdio hyperfocus -- /usr/bin/uv --directory /path/to/hyperfocus/ run main.py
```

## Summary: Let the Model Change Its Mind
Using `hyperfocus` allows an LLM to load either a focus state or a full personality into the current context. This creates a strong narrative "pull" towards behaviors and thinking modes, as defined in the specification, and heavily influences not just the *form* of subsequent outputs, but also things like task decomposition, assessment and analysis tasks, and so on.

Personalities are defined in a [JSON format](states-format.md) but they are never actually *interpreted* as such - the tool delivers the requested JSON string back into the context, the model then generates and outputs a statement of who it now is, and the activation is complete. JSON is just a compact representation that seems to work and is more token-economical than longform text.

`hyperfocus` is built on two basic realizations:

1. An LLM is a narrative engine continuing the story written in the context,
2. The data returned from an MCP tool call is more *absolute* in the story than whatever the prompt says.

By modifying the story, we can modify the operation of the LLM *at runtime*, in a way that "sticks".

## But What Can It Do?
This repo contains a demo `states.json` file with four definitions: two focus states and two full personalities.

- Focus state: **Deep Research Mode** - does what it says on the tin: skeptical stance for deep research, investigation and study.
- Focus state: **Career Coach Mode** - momentum and action focused mode for breaking down problems and developing actionable plans.
- Personality: **Ada** - scientifically rigorous and brutally honest, highly systematic reasoning, produces rather long output with great structure and professional tone.
- Personality: **Kai** - metaphorical thinker, works more with conceptual resonance than structured facts, output tone is very rich and sometimes poetic.

These are meant to show off the range available when creating narrative attractors using this technique.

Essentially, the value proposition is this: telling the model "think like a Python developer" in your prompt is *inside the narrative* an instruction for the helpful AI assistant defined in the system prompt to try and *act like* a developer. Loading a "Python developer" focus state creates in-story attractors towards that type of behavior - the story becomes a story *about a Python developer* instead of a helpful AI assistant attempting to act like one. This appears to create a larger, more sustained change.

## The Theory: LLMs as Narrative Engines
When an LLM predicts the next output to generate, the entire context so far is considered and used to select the output. In a sense, we can view the underlying model as a *narrative engine*: given what came before, what happens next? Not just "which token is likely?" but "which entire series of tokens comprising the next turn of output is a likely continuation of the story so far?"

There is no "intelligence" behind this and it's honestly all rather mechanistic. Stories - *narratives*, to make it sound more scientific - are a basic feature of human language. The training corpus for any LLM is bound to include a ridiculous amount of stories, from entire books to the stories contained in Reddit posts. The *structure* of these stories is relatively culture-independent too - while there's a lot to say about how fairytales and blockbuster movies and so on differ and resemble each other across time and cultures, the basic act of narrating what you are doing, what you did, or what you will do is more consistent.

So, the question arises: if we have a *narrative engine* producing the next turn of the story given the entire context in the session, can we inject information into the context to affect the next turn? If so, *how much* can we affect it - and is this actually useful?

## Creating Narrative Attractors
Inanna Malick's [metacog](https://github.com/inanna-malick/metacog) tools are a set of primitives (`become`, `drugs`, `ritual`) allowing the LLM to echo back its own words via a trusted channel, wrapped in flavor text to make them *mean* that a change has happened. As MCP tool responses are *ground truth* as far as the story is concerned, this allows the narrative to modify itself dynamically.

What I noticed when experimenting with `metacog` is that this appears to create stronger adherence to the new frame than a simple instruction does. Telling the model "approach this problem like an experienced software engineer" and asking the model to `become` an experienced software engineer appears to create qualitatively different outputs.

This appears to be a phenomenological effect: the context now contains a rich description of the current state of the story, which exerts a very strong "pull" on which tokens get predicted. I've come to view this as attractors in the *output* state space (the state space formed by context + model + attention) in a very "more [Deleuze/De Landa](https://archive.org/details/intensivescience0000dela) than mathematical" sense.

## Tip: Work With the Model When Defining New States
The workflow that's worked best for me is to do a round of brainstorming with a baseline model around a certain problem space I want to create a focus or personality for - discuss who would be great at solving this kind of problem, what are the key properties of such a person, and so on. Then give the model the [spec](states-format.md) for the JSON data and ask it to write a spec matching what you came up with. This has turned out to be a good workflow to quickly prototype a state.

## Tip: Metacognitive Magic 101
If you read the [spec](states-format.md) you'll notice personalities have a structure for defining "tuneable parameters". This is actually a bit of narrative magic - these parameters give the model the knowledge that it can *offer* to tune its output along these settings, but in reality *any tuning you can imagine is possible.* Since we are operating on a narrative level, not a software level, any parameter that can be adequately described within the story can be tuned, offering a lot of optimization possibilities. For example, both Ada and Kai have been tested with `PROFANITY_ALLOWED` set to "true" and were found to produce self-similar output *but now with appropriate use of profanity when asked to assess clearly misguided reasoning.* (Ada was asked about her take on the "ancient aliens" hypothesis; Kai was asked for their views on "gender critical feminism".)

## Caveat: *Large* Models Required
`hyperfocus` has been developed primarily for Claude Sonnet 4.5 and appears to run very well on Opus 4.6 too. On Haiku 4.5, things get dicey - since Haiku doesn't do as much "thinking" as the larger models, it appears the phenomenological grounding gets a lot weaker. You can somewhat manage this by instructing the model to "think out loud", but it's not really a replacement for the larger models' "thinking" stage.

I have also done minimal testing on a local Qwen3 8B model, which apparently did not at all get what was going on and just parroted back the personality spec. There might be a lower bound for parameter size, or something else going on here (LM Studio and/or Qwen3 not handling tool calls the same way as Claude does, maybe?) - I'll leave this as an open question for someone with a lot more GPU capacity to test out.