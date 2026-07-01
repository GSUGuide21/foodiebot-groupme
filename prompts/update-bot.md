# FoodieBot Update Prompt

You are updating the FoodieBot GroupMe project.

## Goal

Implement and verify a command system upgrade for the bot client, based on the GroupMe Community Docs:

- https://groupme-js.github.io/GroupMeCommunityDocs

## Existing Project Context

Use the existing architecture and extend it instead of rewriting major modules:

- `client/commands/`
- `client/parser/`
- `client/manager/`
- `client/responses/`

## Requirements

### 1) Command System Enhancements

- Support command aliases.
- Support argument parsing with:
  - quoted strings (single and double quotes),
  - keyword-style arguments (for example: `sides=20 count=2`),
  - positional arguments.
- Add per-command timeout support.
  - Timeout should be configurable per command.
  - If execution exceeds timeout, return a friendly timeout response and fail safely.

### 2) Add New Commands

Implement these commands with aliases and predictable output formats:

1. `coin`
   - Aliases: `flip`, `c`
   - Behavior: returns Heads or Tails.

2. `blackjack`
   - Behavior: starts a simple blackjack interaction in chat.
   - Minimum viable behavior:
     - start a game for requesting user,
     - deal initial hands,
     - allow hit/stand progression,
     - resolve win/loss/push.

3. `roll`
   - Behavior: roll one or more dice.
   - Support:
     - default roll when no args are provided,
     - optional number of dice,
     - optional number of sides.
   - Example accepted forms:
     - `roll`
     - `roll 2`
     - `roll 2 20`
     - `roll count=2 sides=20`

### 3) Add New Responses

## Technical Expectations

- Reuse and extend current parser patterns in `parser/arguments/`.
- Keep command registration discoverable and consistent with current `client/commands/` style.
- Preserve backward compatibility with existing commands unless a change is required for correctness.
- Add concise inline comments only where logic is non-obvious.

## Validation Checklist

After implementation, verify:

- Commands are discovered and routed correctly.
- Aliases resolve to the correct command handler.
- Quoted and keyword arguments parse correctly.
- Timeout behavior works and returns clear user-facing errors.
- `coin`, `blackjack`, and `roll` commands execute as expected.
- Existing command behavior is not regressed.

## Deliverables

1. Updated/added code files implementing the requirements.
2. Brief summary of architecture changes.
3. Command usage examples for all new commands.
4. Any limitations and follow-up recommendations.