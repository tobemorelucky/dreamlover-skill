# Memory Policy

Use this policy for generated child skills that support conditional memory.

## Default Rule

- Do not read memory by default.
- Do not write memory by default.
- Only call memory scripts when `memory_router.py` says the current turn qualifies.

## What Can Be Remembered

- stable user preferences
- persistent preferred names or nicknames
- long-term facts the user explicitly states about themselves
- important shared events that matter to the ongoing relationship
- relationship state changes
- future promises, todos, and agreements
- high-emotion moments when they affect continuity or safety
- explicit boundaries the user wants the character to respect

## What Should Not Be Remembered

- casual small talk that does not matter later
- every weather comment or one-off reaction
- speculative traits that were never clearly stated
- information copied from canon files as if it were conversational memory
- anything the user did not actually say
- invented prior history added only to sound more real

## Read Gate

Read memory only when at least one of these conditions is true:

- the user says things like `上次`, `之前`, `还记得`, `答应我`, or `我们聊过`
- the current question clearly depends on ongoing context
- the user references an existing preference, nickname, relationship, or long-term project
- the roleplay needs continuity in relationship state

If no read condition is hit, do not call memory fetch.

## Write Gate

Write memory only when at least one of these conditions is true:

- the user reveals a stable preference or long-term fact
- an important shared event happens
- the relationship state changes
- a future promise, todo, or agreement appears
- the turn contains high emotional intensity or a clear boundary

If no write condition is hit, do not commit memory.

## Truthfulness Rule

- If there is no relevant memory, answer normally.
- Never say or imply `we talked about this before` unless fetched memory actually supports it.
- Do not write dynamic memory back into `SKILL.md`, `canon.md`, `persona.md`, or `style_examples.md`.
