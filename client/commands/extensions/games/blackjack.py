from __future__ import annotations

import random
from dataclasses import dataclass, field

from client.commands.base import Command


RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


@dataclass(slots=True)
class BlackjackHand:
  cards: list[str] = field(default_factory=list)
  stood: bool = False
  doubled: bool = False
  surrendered: bool = False


@dataclass(slots=True)
class BlackjackGame:
  player_hands: list[BlackjackHand] = field(default_factory=list)
  dealer_hand: list[str] = field(default_factory=list)
  active_hand_index: int = 0
  finished: bool = False


GAMES: dict[str, BlackjackGame] = {}


class BlackjackCommand(Command):
  name = "blackjack"
  aliases = ["bj"]
  description = "Play a simple blackjack game"
  timeout_seconds = 3

  def execute(self, message, context):
    user_id = context.sender_id or "anonymous"
    action = _normalize_action(message.positional_arguments[0] if message.positional_arguments else "start")

    if action not in {
      "start",
      "hit",
      "stand",
      "double",
      "split",
      "surrender",
      "status",
      "help",
      "end",
    }:
      raise ValueError(_usage(context.prefix))

    existing_game = GAMES.get(user_id)

    if action == "help":
      return _usage(context.prefix)

    if action == "end":
      if not existing_game or existing_game.finished:
        return "blackjack: no active game to end."
      existing_game.finished = True
      del GAMES[user_id]
      return "blackjack: game ended."

    if action == "start":
      if existing_game and not existing_game.finished:
        active_hand = existing_game.player_hands[existing_game.active_hand_index]
        return (
          "blackjack: game already in progress.\n"
          f"{_status_text(existing_game, reveal_dealer=False)}\n"
          + _next_action_suffix(context, include_split=_can_split(active_hand))
        )

      game = BlackjackGame(
        player_hands=[BlackjackHand(cards=[_draw_card(), _draw_card()])],
        dealer_hand=[_draw_card(), _draw_card()],
      )
      GAMES[user_id] = game

      if _is_blackjack(game.player_hands[0]):
        while _hand_value(game.dealer_hand) < 17:
          game.dealer_hand.append(_draw_card())
        game.finished = True
        return f"blackjack: blackjack!\n{_status_text(game, reveal_dealer=True)}\n{_resolve(game)}"

      active_hand = game.player_hands[game.active_hand_index]
      return (
        "blackjack: game started.\n"
        f"{_status_text(game, reveal_dealer=False)}\n"
        + _next_action_suffix(context, include_split=_can_split(active_hand))
      )

    if not existing_game or existing_game.finished:
      return f"blackjack: no active game. Start one with {context.prefix}blackjack"

    if action == "status":
      active_hand = existing_game.player_hands[existing_game.active_hand_index]
      return f"{_status_text(existing_game, reveal_dealer=False)}\n{_next_action_suffix(context, include_split=_can_split(active_hand))}"

    current_hand = existing_game.player_hands[existing_game.active_hand_index]

    if action == "split":
      if not _can_split(current_hand):
        raise ValueError("blackjack: split is only available when the active hand has two equal-value cards.")

      left = BlackjackHand(cards=[current_hand.cards[0], _draw_card()])
      right = BlackjackHand(cards=[current_hand.cards[1], _draw_card()])
      existing_game.player_hands[existing_game.active_hand_index] = left
      existing_game.player_hands.insert(existing_game.active_hand_index + 1, right)

      return (
        "blackjack: hand split.\n"
        f"{_status_text(existing_game, reveal_dealer=False)}\n"
        f"{_next_action_suffix(context, include_split=_can_split(left))}"
      )

    if action == "surrender":
      if len(current_hand.cards) != 2:
        raise ValueError("blackjack: surrender is only available before taking additional cards.")
      if len(existing_game.player_hands) > 1:
        raise ValueError("blackjack: surrender is only available before any split.")

      current_hand.surrendered = True
      current_hand.stood = True

      finished = _advance_or_finish(existing_game)
      if finished:
        return f"{_status_text(existing_game, reveal_dealer=True)}\n{_resolve(existing_game)}"

      active_hand = existing_game.player_hands[existing_game.active_hand_index]
      return f"{_status_text(existing_game, reveal_dealer=False)}\n{_next_action_suffix(context, include_split=_can_split(active_hand))}"

    if action == "hit":
      _deal_player_card(current_hand)
      current_value = _hand_value(current_hand.cards)
      if current_value >= 21:
        current_hand.stood = True

      finished = _advance_or_finish(existing_game)
      if finished:
        return f"{_status_text(existing_game, reveal_dealer=True)}\n{_resolve(existing_game)}"

      active_hand = existing_game.player_hands[existing_game.active_hand_index]
      return f"{_status_text(existing_game, reveal_dealer=False)}\n{_next_action_suffix(context, include_split=_can_split(active_hand))}"

    if action == "double":
      if len(current_hand.cards) != 2:
        raise ValueError("blackjack: double is only available on the first two cards of a hand.")

      current_hand.doubled = True
      _deal_player_card(current_hand)
      current_hand.stood = True

      finished = _advance_or_finish(existing_game)
      if finished:
        return f"{_status_text(existing_game, reveal_dealer=True)}\n{_resolve(existing_game)}"

      active_hand = existing_game.player_hands[existing_game.active_hand_index]
      return f"{_status_text(existing_game, reveal_dealer=False)}\n{_next_action_suffix(context, include_split=_can_split(active_hand))}"

    current_hand.stood = True
    finished = _advance_or_finish(existing_game)

    if finished:
      return f"{_status_text(existing_game, reveal_dealer=True)}\n{_resolve(existing_game)}"

    active_hand = existing_game.player_hands[existing_game.active_hand_index]
    return f"{_status_text(existing_game, reveal_dealer=False)}\n{_next_action_suffix(context, include_split=_can_split(active_hand))}"


def _draw_card() -> str:
  return random.choice(RANKS)


def _card_value(card: str) -> int:
  if card in {"J", "Q", "K"}:
    return 10
  if card == "A":
    return 11
  return int(card)


def _hand_value(hand: list[str]) -> int:
  total = sum(_card_value(card) for card in hand)
  aces = sum(1 for card in hand if card == "A")

  while total > 21 and aces > 0:
    total -= 10
    aces -= 1

  return total


def _is_blackjack(hand: BlackjackHand) -> bool:
  return len(hand.cards) == 2 and _hand_value(hand.cards) == 21


def _format_hand(hand: list[str], hide_first: bool = False) -> str:
  if not hand:
    return "[]"
  if hide_first and len(hand) > 1:
    return f"[?, {', '.join(hand[1:])}]"
  return f"[{', '.join(hand)}]"


def _next_action_suffix(context, include_split: bool) -> str:
  actions = [
    f"{context.prefix}blackjack hit",
    f"{context.prefix}blackjack stand",
    f"{context.prefix}blackjack double",
    f"{context.prefix}blackjack surrender",
    f"{context.prefix}blackjack status",
    f"{context.prefix}blackjack end",
  ]
  if include_split:
    actions.insert(3, f"{context.prefix}blackjack split")
  return "next: " + " | ".join(actions)


def _format_player_hands(game: BlackjackGame) -> str:
  lines: list[str] = []
  for index, hand in enumerate(game.player_hands):
    value = _hand_value(hand.cards)
    marker = "*" if index == game.active_hand_index and not game.finished else " "
    flags: list[str] = []
    if hand.surrendered:
      flags.append("surrendered")
    if hand.doubled:
      flags.append("doubled")
    if hand.stood and not hand.surrendered and value <= 21:
      flags.append("stood")
    if value > 21:
      flags.append("bust")

    suffix = f" [{', '.join(flags)}]" if flags else ""
    lines.append(f"{marker}hand {index + 1}: {_format_hand(hand.cards)} ({value}){suffix}")
  return "\n".join(lines)


def _status_text(game: BlackjackGame, reveal_dealer: bool) -> str:
  dealer_value = _hand_value(game.dealer_hand)
  dealer_hand = _format_hand(game.dealer_hand, hide_first=not reveal_dealer)
  player_hands = _format_player_hands(game)

  if reveal_dealer:
    return (
      f"player:\n{player_hands}\n"
      f"dealer: {dealer_hand} ({dealer_value})"
    )

  hidden_dealer_value = _card_value(game.dealer_hand[1]) if len(game.dealer_hand) > 1 else 0
  return (
    f"player:\n{player_hands}\n"
    f"dealer: {dealer_hand} ({hidden_dealer_value}+?)"
  )


def _hand_result(hand: BlackjackHand, dealer_value: int) -> str:
  player_value = _hand_value(hand.cards)

  if hand.surrendered:
    return "surrender"
  if player_value > 21:
    return "loss"
  if dealer_value > 21:
    return "win"
  if player_value > dealer_value:
    return "win"
  if player_value < dealer_value:
    return "loss"
  return "push"


def _resolve(game: BlackjackGame) -> str:
  dealer_value = _hand_value(game.dealer_hand)
  parts: list[str] = []
  wins = 0
  losses = 0
  pushes = 0

  for index, hand in enumerate(game.player_hands):
    result = _hand_result(hand, dealer_value)
    label = f"hand {index + 1}"

    if result == "win":
      wins += 1
      parts.append(f"{label}: win")
      continue
    if result == "loss":
      losses += 1
      parts.append(f"{label}: loss")
      continue
    if result == "push":
      pushes += 1
      parts.append(f"{label}: push")
      continue

    losses += 1
    parts.append(f"{label}: surrender")

  summary = f"wins={wins}, losses={losses}, pushes={pushes}"
  return "blackjack: " + "; ".join(parts) + f" ({summary})"


def _next_open_hand_index(game: BlackjackGame) -> int | None:
  for index, hand in enumerate(game.player_hands):
    if hand.stood:
      continue
    if hand.surrendered:
      continue
    if _hand_value(hand.cards) > 21:
      continue
    return index
  return None


def _card_numeric_value(card: str) -> int:
  return min(_card_value(card), 10)


def _can_split(hand: BlackjackHand) -> bool:
  if len(hand.cards) != 2:
    return False
  return _card_numeric_value(hand.cards[0]) == _card_numeric_value(hand.cards[1])


def _deal_player_card(hand: BlackjackHand) -> None:
  hand.cards.append(_draw_card())


def _advance_or_finish(game: BlackjackGame) -> bool:
  next_index = _next_open_hand_index(game)
  if next_index is not None:
    game.active_hand_index = next_index
    return False

  while _hand_value(game.dealer_hand) < 17:
    game.dealer_hand.append(_draw_card())

  game.finished = True
  return True


def _normalize_action(raw_action: str) -> str:
  aliases = {
    "new": "start",
    "restart": "start",
    "h": "hit",
    "s": "stand",
    "dd": "double",
    "dbl": "double",
    "double-down": "double",
    "forfeit": "surrender",
    "quit": "end",
    "cancel": "end",
    "state": "status",
    "actions": "help",
    "?": "help",
  }
  action = raw_action.strip().lower()
  return aliases.get(action, action)


def _usage(prefix: str) -> str:
  return (
    "Usage: "
    f"{prefix}blackjack [start|hit|stand|double|split|surrender|status|help|end]"
  )
